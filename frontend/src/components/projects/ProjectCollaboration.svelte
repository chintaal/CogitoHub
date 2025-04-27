<script>
  import { onMount, onDestroy } from 'svelte';
  import { user, getUserProfile } from '../../lib/stores/authStore';
  import { 
    initProjectCollaboration, 
    updateCollaboratorStatus, 
    getProjectCollaborators 
  } from '../../lib/firebase/realtimeDb';
  
  export let projectId;
  export let projectName = '';
  export let isEditable = false;
  
  let error = '';
  let userStatus = 'viewing'; // 'viewing', 'editing', 'away'
  let statusUpdateInterval;
  let lastActivity = Date.now();
  
  // Get collaborators from store
  $: collaborators = getProjectCollaborators(projectId);
  
  // Update status when user is idle
  function checkActivity() {
    const now = Date.now();
    if (now - lastActivity > 60000) { // 1 minute
      if (userStatus !== 'away') {
        userStatus = 'away';
        updateStatus('away');
      }
    }
  }
  
  // Track user activity
  function trackActivity() {
    lastActivity = Date.now();
    if (userStatus === 'away') {
      userStatus = 'viewing';
      updateStatus('viewing');
    }
  }
  
  // Update user status on the project
  async function updateStatus(status) {
    if (!$user) return;
    
    try {
      await updateCollaboratorStatus(projectId, $user.uid, status);
    } catch (err) {
      console.error('Error updating status:', err);
      error = err.message || 'Failed to update status';
    }
  }
  
  // Handle edit mode toggle
  function toggleEditMode() {
    if (!isEditable) return;
    
    userStatus = userStatus === 'editing' ? 'viewing' : 'editing';
    updateStatus(userStatus);
  }

  // Initialize collaboration features
  onMount(async () => {
    try {
      // Set up real-time collaboration
      await initProjectCollaboration(projectId);
      
      // Set initial status
      await updateStatus(userStatus);
      
      // Set up activity tracking
      document.addEventListener('mousemove', trackActivity);
      document.addEventListener('keydown', trackActivity);
      document.addEventListener('click', trackActivity);
      
      // Check for inactivity periodically
      statusUpdateInterval = setInterval(checkActivity, 10000);
    } catch (err) {
      console.error('Error initializing collaboration:', err);
      error = err.message || 'Failed to initialize collaboration';
    }
  });
  
  // Clean up on component destruction
  onDestroy(() => {
    clearInterval(statusUpdateInterval);
    document.removeEventListener('mousemove', trackActivity);
    document.removeEventListener('keydown', trackActivity);
    document.removeEventListener('click', trackActivity);
    
    // Update status to away when leaving
    if ($user) {
      updateStatus('away');
    }
  });
  
  // Format time since last active
  function formatLastActive(timestamp) {
    if (!timestamp) return 'Unknown';
    
    const lastActive = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now - lastActive) / 1000);
    
    if (seconds < 60) {
      return 'Just now';
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    } else if (seconds < 86400) {
      const hours = Math.floor(seconds / 3600);
      return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else {
      const days = Math.floor(seconds / 86400);
      return `${days} day${days !== 1 ? 's' : ''} ago`;
    }
  }
</script>

<div class="bg-white rounded-lg shadow p-4">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-medium">
      {projectName || 'Project'} Collaboration
    </h3>
    
    {#if isEditable}
      <button
        on:click={toggleEditMode}
        class={`px-3 py-1 rounded text-sm ${
          userStatus === 'editing'
            ? 'bg-green-100 text-green-800'
            : 'bg-gray-100 text-gray-800'
        }`}
      >
        {userStatus === 'editing' ? 'Currently Editing' : 'Start Editing'}
      </button>
    {/if}
  </div>
  
  {#if error}
    <div class="mb-4 p-2 bg-red-50 text-red-700 rounded text-sm">
      {error}
    </div>
  {/if}
  
  <!-- Active Collaborators -->
  <div class="mb-4">
    <h4 class="text-sm font-medium text-gray-700 mb-2">
      Active Collaborators ({$collaborators.filter(c => c.status !== 'away').length})
    </h4>
    
    <div class="space-y-2">
      {#if $collaborators.filter(c => c.status !== 'away').length === 0}
        <p class="text-sm text-gray-500 italic">No active collaborators</p>
      {:else}
        {#each $collaborators.filter(c => c.status !== 'away') as collaborator}
          <div class="flex items-center p-2 border rounded bg-gray-50">
            <img
              src={collaborator.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(collaborator.displayName)}`}
              alt={collaborator.displayName}
              class="w-8 h-8 rounded-full mr-2"
            />
            <div class="flex-1">
              <div class="flex items-center">
                <span class="font-medium">{collaborator.displayName}</span>
                <span class="text-xs ml-2 capitalize text-gray-500">{collaborator.userType}</span>
              </div>
              <div class="text-xs text-gray-500">
                Last active: {formatLastActive(collaborator.lastActive)}
              </div>
            </div>
            <div class={`w-2 h-2 rounded-full ${
              collaborator.status === 'editing'
                ? 'bg-green-500'
                : 'bg-blue-500'
            }`}>
            </div>
            <span class="text-xs ml-1 capitalize">
              {collaborator.status}
            </span>
          </div>
        {/each}
      {/if}
    </div>
  </div>
  
  <!-- Away Collaborators -->
  {#if $collaborators.filter(c => c.status === 'away').length > 0}
    <div>
      <h4 class="text-sm font-medium text-gray-700 mb-2">
        Away ({$collaborators.filter(c => c.status === 'away').length})
      </h4>
      
      <div class="space-y-2">
        {#each $collaborators.filter(c => c.status === 'away') as collaborator}
          <div class="flex items-center p-2 border rounded bg-gray-50 opacity-60">
            <img
              src={collaborator.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(collaborator.displayName)}`}
              alt={collaborator.displayName}
              class="w-8 h-8 rounded-full mr-2 grayscale"
            />
            <div class="flex-1">
              <div class="flex items-center">
                <span class="font-medium">{collaborator.displayName}</span>
                <span class="text-xs ml-2 capitalize text-gray-500">{collaborator.userType}</span>
              </div>
              <div class="text-xs text-gray-500">
                Last active: {formatLastActive(collaborator.lastActive)}
              </div>
            </div>
            <div class="w-2 h-2 rounded-full bg-gray-400"></div>
            <span class="text-xs ml-1">Away</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>