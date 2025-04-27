<script>
  import { onMount, onDestroy } from 'svelte';
  import { user, getUserProfile } from '../../lib/stores/authStore';
  import { 
    trackCourseActivity,
    initializeFirebase
  } from '../../lib/firebase/realtimeDb';
  import { browser } from '$app/environment';

  export let courseId;
  export let courseTitle = '';
  export let userType = 'student';
  
  let loading = true;
  let error = '';
  let activityData = {};
  let recentActivity = [];
  
  // Track which part of the course the user is viewing
  export let currentSection = 'overview'; // 'overview', 'materials', 'assignments', 'discussions'
  
  // Initialize activity tracking
  onMount(async () => {
    if (!browser || !$user || !courseId) return;
    
    try {
      // First, track the user's activity
      await trackCourseActivity(courseId, $user.uid, 'viewing-' + currentSection);
      
      // Set up listener for course activity
      const { rtdb } = await initializeFirebase();
      if (!rtdb) throw new Error('Realtime Database not initialized');
      
      activityRef = ref(rtdb, `courses/${courseId}/activity`);
      logRef = ref(rtdb, `courses/${courseId}/activityLog`);
      
      // Listen for active users
      onValue(activityRef, (snapshot) => {
        activityData = snapshot.val() || {};
        loading = false;
      });
      
      // Listen for recent activity, limited to last 10 events
      onValue(logRef, (snapshot) => {
        const logData = snapshot.val() || {};
        
        // Convert to array and sort by timestamp (newest first)
        recentActivity = Object.entries(logData)
          .map(([id, data]) => ({ id, ...data }))
          .sort((a, b) => {
            // Handle missing timestamp values
            const timeA = a.timestamp || 0;
            const timeB = b.timestamp || 0;
            return timeB - timeA;
          })
          .slice(0, 10); // Get only latest 10
      });
    } catch (err) {
      console.error('Error setting up activity tracking:', err);
      error = err.message || 'Failed to load activity data';
      loading = false;
    }
  });
  
  // Clean up listeners
  onDestroy(() => {
    if (activityRef) off(activityRef);
    if (logRef) off(logRef);
  });
  
  // Track when user switches sections
  $: if (browser && $user && courseId && currentSection) {
    trackCourseActivity(courseId, $user.uid, 'viewing-' + currentSection)
      .catch(err => console.error('Error tracking section change:', err));
  }
  
  // Format activity time
  function formatActivity(timestamp) {
    if (!timestamp) return 'Recently';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffSeconds = Math.floor((now - date) / 1000);
    
    if (diffSeconds < 60) {
      return 'Just now';
    } else if (diffSeconds < 3600) {
      return `${Math.floor(diffSeconds / 60)} min ago`;
    } else if (diffSeconds < 86400) {
      return `${Math.floor(diffSeconds / 3600)} hr ago`;
    } else {
      return date.toLocaleDateString();
    }
  }
  
  // Format activity type for display
  function formatActivityType(type) {
    if (!type) return 'Active';
    
    // Replace hyphens with spaces and capitalize
    return type
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  
  // Get only active users (interacted within the last hour)
  $: activeUsers = Object.entries(activityData)
    .filter(([_, data]) => {
      if (!data.lastActive) return true;
      
      const lastActive = new Date(data.lastActive);
      const oneHourAgo = new Date();
      oneHourAgo.setHours(oneHourAgo.getHours() - 1);
      
      return lastActive >= oneHourAgo;
    })
    .map(([uid, data]) => ({
      uid,
      ...data
    }));
  
  // Active students and professors
  $: activeStudents = activeUsers.filter(user => user.userType === 'student');
  $: activeProfessors = activeUsers.filter(user => user.userType === 'professor');
</script>

<div class="bg-white rounded-lg shadow p-4">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-medium">{courseTitle} Activity</h3>
    
    {#if userType === 'professor'}
      <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
        Instructor View
      </span>
    {/if}
  </div>
  
  {#if error}
    <div class="bg-red-50 text-red-700 p-3 rounded mb-4 text-sm">
      {error}
    </div>
  {:else if loading}
    <div class="flex justify-center py-4">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
    </div>
  {:else}
    <!-- Active Users -->
    <div class="mb-5">
      <h4 class="font-medium text-sm text-gray-700 mb-2">Currently Active</h4>
      
      {#if activeUsers.length === 0}
        <p class="text-sm text-gray-500">No one is currently active</p>
      {:else}
        <div class="flex flex-wrap -ml-1 -mt-1">
          {#each activeUsers as user}
            <div class="ml-1 mt-1 relative group">
              <div class="w-8 h-8 rounded-full overflow-hidden border-2 relative
                {user.userType === 'professor' ? 'border-blue-400' : 'border-green-400'}">
                <img
                  src={user.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.displayName || 'User')}`}
                  alt={user.displayName}
                  class="w-full h-full object-cover"
                />
              </div>
              
              <!-- Tooltip -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 -translate-y-1 
                  bg-gray-800 text-white text-xs rounded py-1 px-2 hidden group-hover:block 
                  whitespace-nowrap z-10">
                <div class="font-medium">{user.displayName || 'Anonymous'}</div>
                <div class="text-gray-300">
                  {formatActivityType(user.lastActivityType)}
                </div>
                <div class="text-gray-400 text-xs">
                  {formatActivity(user.lastActive)}
                </div>
                <!-- Arrow -->
                <div class="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
              </div>
            </div>
          {/each}
        </div>
        
        <!-- Activity counts -->
        <div class="mt-2 text-xs text-gray-500">
          {activeStudents.length} student{activeStudents.length !== 1 ? 's' : ''}
          {activeProfessors.length > 0 ? `, ${activeProfessors.length} instructor${activeProfessors.length !== 1 ? 's' : ''}` : ''}
          active
        </div>
      {/if}
    </div>
    
    <!-- Recent Activity Log (visible only to professors) -->
    {#if userType === 'professor' && recentActivity.length > 0}
      <div>
        <h4 class="font-medium text-sm text-gray-700 mb-2">Recent Activity</h4>
        
        <div class="space-y-2 max-h-40 overflow-y-auto pr-1">
          {#each recentActivity as activity}
            <div class="flex items-center text-sm border-l-2 border-gray-200 pl-2">
              <img
                src={activity.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(activity.displayName || 'User')}`}
                alt={activity.displayName}
                class="w-6 h-6 rounded-full mr-2"
              />
              <div class="flex-1 min-w-0">
                <div class="text-gray-800 truncate">
                  <span class="font-medium">{activity.displayName || 'Anonymous'}</span>
                  <span class="text-gray-500">
                    {formatActivityType(activity.activityType)}
                  </span>
                </div>
              </div>
              <div class="text-xs text-gray-500 whitespace-nowrap ml-2">
                {formatActivity(activity.timestamp)}
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  {/if}
</div>