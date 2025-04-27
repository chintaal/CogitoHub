<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, getUserProfile, updateUserProfile } from '../../lib/stores/authStore';
  import { writable } from 'svelte/store';
  import PageGuard from '../../lib/components/PageGuard.svelte';
  
  // Components for different user dashboards
  import StudentDashboard from '../../components/cogitohub/StudentDashboard.svelte';
  import ProfessorDashboard from '../../components/cogitohub/ProfessorDashboard.svelte';
  import RecruiterDashboard from '../../components/cogitohub/RecruiterDashboard.svelte';
  import UserTypeSelection from '../../components/cogitohub/UserTypeSelection.svelte';
  import CogitoHubNav from '../../components/cogitohub/CogitoHubNav.svelte';
  
  let userProfile = null;
  let loading = true;
  let displayOnboarding = false;
  const activeSection = writable('projects');

  // Load user profile
  async function loadUserProfile() {
    if (!$user) {
      goto('/login');
      return;
    }
    
    try {
      loading = true;
      const profileData = await getUserProfile($user.uid);
      
      if (profileData) {
        userProfile = profileData;
        displayOnboarding = !profileData.userType;
      } else {
        // Create default profile for new user
        userProfile = {
          uid: $user.uid,
          email: $user.email,
          displayName: $user.displayName || '',
          photoURL: $user.photoURL || '',
          onboardingCompleted: false,
          createdAt: new Date().toISOString()
        };
        displayOnboarding = true;
      }
    } catch (error) {
      console.error('Error loading profile:', error);
      userProfile = {
        uid: $user.uid,
        email: $user.email,
        displayName: $user.displayName || 'User',
        photoURL: $user.photoURL || '',
        onboardingCompleted: false,
        createdAt: new Date().toISOString()
      };
      displayOnboarding = true;
    } finally {
      loading = false;
    }
  }
  
  // Handle user type selection during onboarding
  async function handleUserTypeSelection(event) {
    const { userType, additionalInfo } = event.detail;
    
    try {
      loading = true;
      
      const profileUpdateData = {
        userType,
        ...additionalInfo,
        onboardingCompleted: true,
        updatedAt: new Date().toISOString()
      };
      
      const updateResult = await updateUserProfile($user.uid, profileUpdateData);
      
      if (updateResult.success) {
        userProfile = await getUserProfile($user.uid);
        displayOnboarding = false;
      } else {
        // Apply changes locally if update fails
        userProfile = {
          ...(userProfile || {}),
          ...profileUpdateData,
          uid: $user.uid,
          email: $user.email || '',
          displayName: $user.displayName || '',
          photoURL: $user.photoURL || ''
        };
        displayOnboarding = false;
      }
    } catch (error) {
      console.error('Error in user type selection:', error);
      // Apply changes locally
      userProfile = {
        ...(userProfile || {}),
        userType,
        ...additionalInfo,
        onboardingCompleted: true,
        updatedAt: new Date().toISOString(),
        uid: $user.uid,
        email: $user.email || '',
        displayName: $user.displayName || '',
        photoURL: $user.photoURL || ''
      };
      displayOnboarding = false;
    } finally {
      loading = false;
    }
  }
  
  // Handle section changes
  function changeSection(section) {
    activeSection.set(section);
  }
  
  // Initialize
  onMount(() => {
    const unsubscribe = user.subscribe(userData => {
      if (userData) {
        loadUserProfile();
      } else {
        goto('/login');
      }
    });
    
    return unsubscribe;
  });
</script>

<PageGuard>
  <div class="min-h-screen bg-gradient-to-b from-white to-gray-100">
    {#if loading}
      <div class="flex justify-center items-center h-screen">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    {:else if displayOnboarding}
      <UserTypeSelection on:userTypeSelected={handleUserTypeSelection} />
    {:else if userProfile}
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <!-- Common CogitoHub Header -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">CogitoHub</h1>
              <p class="text-gray-600 mt-1">
                {#if userProfile.userType === 'student'}
                  Explore projects, courses, and opportunities for students
                {:else if userProfile.userType === 'professor'}
                  Manage courses, research projects, and connect with students
                {:else if userProfile.userType === 'recruiter'}
                  Find talent, post opportunities, and engage with the academic community
                {/if}
              </p>
            </div>
            
            <div class="flex items-center space-x-2">
              <img 
                src={userProfile.photoURL || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(userProfile.displayName || 'User')}
                alt="Profile" 
                class="w-10 h-10 rounded-full"
              />
              <div>
                <p class="font-medium">{userProfile.displayName || 'User'}</p>
                <p class="text-sm text-gray-500 capitalize">{userProfile.userType}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- CogitoHub Navigation -->
        <CogitoHubNav 
          {userProfile} 
          {activeSection} 
          on:changeSection={(e) => changeSection(e.detail)}
        />
        
        <!-- User Type Specific Dashboard -->
        <div class="mt-6">
          {#if userProfile.userType === 'student'}
            <StudentDashboard {activeSection} {userProfile} />
          {:else if userProfile.userType === 'professor'}
            <ProfessorDashboard {activeSection} {userProfile} />
          {:else if userProfile.userType === 'recruiter'}
            <RecruiterDashboard {activeSection} {userProfile} />
          {:else}
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
              <p class="text-amber-700">User type not recognized. Please contact support.</p>
            </div>
          {/if}
        </div>
      </div>
    {:else}
      <div class="flex flex-col justify-center items-center h-screen">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center max-w-md w-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-red-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p class="text-red-700 font-medium text-lg">Failed to load profile</p>
          <p class="text-red-600 mt-2">There was an error loading your user profile. Please try again.</p>
          
          <div class="mt-4 p-3 bg-gray-50 rounded text-left text-sm text-gray-600">
            <p class="font-medium mb-1">Troubleshooting tips:</p>
            <ul class="list-disc pl-5 space-y-1">
              <li>Check your internet connection</li>
              <li>Try refreshing the page</li>
              <li>Try clearing your browser cache</li>
            </ul>
          </div>
          
          <div class="flex mt-4 space-x-3 justify-center">
            <button 
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors flex items-center"
              on:click={loadUserProfile}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Retry Loading
            </button>
            
            <button 
              class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors flex items-center"
              on:click={() => goto('/dashboard')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    {/if}
  </div>
</PageGuard>