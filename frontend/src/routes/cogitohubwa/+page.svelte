<script>
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, getUserProfile, updateUserProfile } from '../../lib/stores/authStore.js';
  import { writable } from 'svelte/store';
  import { initializeFirebase } from '../../lib/firebase/firebase.js';
  import { cleanupUserData } from '../../lib/firebase/realtimeDb.js';
  
  // Components for different user dashboards
  import StudentDashboard from '../../components/cogitohub/StudentDashboard.svelte';
  import ProfessorDashboard from '../../components/cogitohub/ProfessorDashboard.svelte';
  import RecruiterDashboard from '../../components/cogitohub/RecruiterDashboard.svelte';
  import UserTypeSelection from '../../components/cogitohub/UserTypeSelection.svelte';
  import CogitoHubNav from '../../components/cogitohub/CogitoHubNav.svelte';
  
  let userProfile = null;
  let loading = true;
  let displayOnboarding = false;
  let firebaseInitialized = false;
  let initializationRetries = 0;
  let maxRetries = 3;

  const activeSection = writable('projects');

  // Initialize Firebase with retry mechanism
  async function initializeServices() {
    if (initializationRetries >= maxRetries) {
      console.error('Failed to initialize Firebase services after multiple attempts');
      return false;
    }
    
    try {
      initializationRetries++;
      console.log(`Initializing Firebase (attempt ${initializationRetries}/${maxRetries})`);
      
      const { auth, db, rtdb } = await initializeFirebase();
      if (!auth || !db || !rtdb) {
        console.warn('Some Firebase services failed to initialize, retrying...');
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait before retry
        return initializeServices();
      }
      
      firebaseInitialized = true;
      console.log('All Firebase services initialized successfully');
      return true;
    } catch (error) {
      console.error('Failed to initialize Firebase services:', error);
      
      if (initializationRetries < maxRetries) {
        console.log(`Retrying in ${initializationRetries * 1000}ms...`);
        await new Promise(resolve => setTimeout(resolve, initializationRetries * 1000));
        return initializeServices();
      }
      
      return false;
    }
  }

  // Load user profile after Firebase initialization with enhanced error recovery
  async function loadUserProfile() {
    if (!$user) {
      goto('/login');
      return;
    }
    
    loading = true;
    let profileLoadAttempt = 0;
    const maxProfileAttempts = 3;
    
    while (profileLoadAttempt < maxProfileAttempts) {
      try {
        profileLoadAttempt++;
        console.log(`Attempting to load profile (attempt ${profileLoadAttempt}/${maxProfileAttempts})`);
        
        // Make sure Firebase is initialized before proceeding
        if (!firebaseInitialized) {
          const success = await initializeServices();
          if (!success) {
            console.error('Firebase initialization failed, retrying...');
            // Wait before retry with exponential backoff
            await new Promise(resolve => setTimeout(resolve, 1000 * profileLoadAttempt));
            continue;
          }
        }
        
        console.log("Fetching user profile data...");
        
        const profileData = await getUserProfile($user.uid).catch(err => {
          console.error('Profile fetch error:', err);
          throw new Error('Failed to load profile: ' + (err.message || 'Unknown error'));
        });
        
        if (profileData) {
          console.log("Profile loaded successfully");
          userProfile = profileData;
          
          // Check if onboarding is needed
          if (!profileData.userType) {
            console.log("User type not set, showing onboarding");
            displayOnboarding = true;
          }
          
          // Successfully loaded, exit retry loop
          break;
        } else {
          console.log("No profile found - new user detected");
          
          // This is a new user without a profile - create default profile template
          // This helps handle the case where authentication succeeded but profile creation failed
          if (profileLoadAttempt === maxProfileAttempts) {
            console.log("Creating fallback profile for new user");
            userProfile = {
              uid: $user.uid,
              email: $user.email,
              displayName: $user.displayName || '',
              photoURL: $user.photoURL || '',
              onboardingCompleted: false,
              createdAt: new Date().toISOString()
            };
            
            // Show onboarding for new user
            displayOnboarding = true;
            break;
          }
          
          // Wait before retry
          await new Promise(resolve => setTimeout(resolve, 1000 * profileLoadAttempt));
        }
      } catch (error) {
        console.error(`Error loading profile (attempt ${profileLoadAttempt}/${maxProfileAttempts}):`, error);
        
        if (profileLoadAttempt < maxProfileAttempts) {
          // Wait before retry with exponential backoff
          const backoffTime = Math.min(2000 * (2 ** (profileLoadAttempt - 1)), 8000);
          console.log(`Retrying profile load in ${backoffTime}ms...`);
          await new Promise(resolve => setTimeout(resolve, backoffTime));
        } else {
          // Last attempt failed, but we can try to provide a minimal default profile
          // based on authentication data to avoid complete failure
          try {
            console.log("Creating emergency fallback profile from auth data");
            if ($user) {
              userProfile = {
                uid: $user.uid,
                email: $user.email,
                displayName: $user.displayName || 'User',
                photoURL: $user.photoURL || '',
                onboardingCompleted: false,
                createdAt: new Date().toISOString(),
                isEmergencyProfile: true // Flag to indicate this is a recovery profile
              };
              
              displayOnboarding = true;
              console.log("Emergency profile created to avoid complete failure");
            }
          } catch (emergencyError) {
            console.error("Even emergency profile creation failed:", emergencyError);
            // At this point we'll just show the error UI
          }
        }
      } finally {
        if (profileLoadAttempt === maxProfileAttempts) {
          loading = false;
        }
      }
    }
    
    loading = false;
  }
  
  // Handle user type selection during onboarding with improved error handling
  async function handleUserTypeSelection(event) {
    const { userType, additionalInfo } = event.detail;
    
    try {
      loading = true;
      
      // Prepare profile update data
      const profileUpdateData = {
        userType,
        ...additionalInfo,
        onboardingCompleted: true,
        updatedAt: new Date().toISOString()
      };
      
      // If this was an emergency profile, add necessary fields
      if (userProfile && userProfile.isEmergencyProfile) {
        profileUpdateData.isEmergencyProfile = false; // Clear emergency flag
      }
      
      // Multiple attempts for profile update
      let updateAttempt = 0;
      const maxUpdateAttempts = 3;
      let updateSuccess = false;
      
      while (updateAttempt < maxUpdateAttempts && !updateSuccess) {
        try {
          updateAttempt++;
          console.log(`Attempting profile update (attempt ${updateAttempt}/${maxUpdateAttempts})`);
          
          // Try to update the user profile
          const updateResult = await updateUserProfile($user.uid, profileUpdateData);
          
          if (updateResult.success) {
            console.log("Profile updated successfully");
            updateSuccess = true;
            
            // Try to reload profile
            try {
              userProfile = await getUserProfile($user.uid);
              displayOnboarding = false;
            } catch (profileLoadError) {
              console.error("Error reloading profile after update:", profileLoadError);
              
              // Fall back to local update if profile reload fails
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
            
            break; // Exit retry loop on success
          } else {
            console.error(`Failed to update profile (attempt ${updateAttempt}):`, updateResult.error);
            
            // Only retry if not the last attempt
            if (updateAttempt < maxUpdateAttempts) {
              const backoffTime = Math.min(1000 * (2 ** (updateAttempt - 1)), 5000);
              console.log(`Retrying update in ${backoffTime}ms...`);
              await new Promise(resolve => setTimeout(resolve, backoffTime));
            }
          }
        } catch (retryError) {
          console.error(`Error during profile update retry ${updateAttempt}:`, retryError);
          
          if (updateAttempt < maxUpdateAttempts) {
            const backoffTime = Math.min(1000 * (2 ** (updateAttempt - 1)), 5000);
            await new Promise(resolve => setTimeout(resolve, backoffTime));
          }
        }
      }
      
      // If all update attempts failed
      if (!updateSuccess) {
        console.error("All profile update attempts failed");
        
        // Apply changes locally for better UX
        userProfile = {
          ...(userProfile || {}),
          ...profileUpdateData,
          uid: $user.uid,
          email: $user.email || '',
          displayName: $user.displayName || '',
          photoURL: $user.photoURL || '',
          pendingSync: true // Flag to indicate changes need to be synced
        };
        
        // Show the user interface anyway
        displayOnboarding = false;
        
        // Schedule a background retry
        setTimeout(() => {
          updateUserProfile($user.uid, profileUpdateData)
            .then(result => {
              if (result.success) {
                console.log("Background profile sync successful");
                if (userProfile) userProfile.pendingSync = false;
              }
            })
            .catch(err => console.error("Background profile sync failed:", err));
        }, 10000);
      }
    } catch (error) {
      console.error('Error in user type selection:', error);
      
      // Apply changes locally even if there was an error
      userProfile = {
        ...(userProfile || {}),
        userType,
        ...additionalInfo,
        onboardingCompleted: true,
        updatedAt: new Date().toISOString(),
        uid: $user.uid,
        email: $user.email || '',
        displayName: $user.displayName || '',
        photoURL: $user.photoURL || '',
        pendingSync: true
      };
      
      displayOnboarding = false;
    } finally {
      loading = false;
    }
  }
  
  // Handle tab/section changes
  function changeSection(section) {
    activeSection.set(section);
  }
  
  // Initialize
  onMount(async () => {
    // Initialize Firebase first
    await initializeServices();
    
    // Watch for auth state changes
    const unsubscribe = user.subscribe(userData => {
      if (userData) {
        loadUserProfile();
      } else {
        // Redirect to login if not authenticated
        goto('/login');
      }
    });
    
    return unsubscribe;
  });
  
  // Clean up when component is destroyed
  onDestroy(() => {
    if (firebaseInitialized) {
      cleanupUserData().catch(err => {
        console.warn('Error during Firebase cleanup:', err);
      });
    }
  });
</script>

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
        <button 
          class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          on:click={loadUserProfile}
        >
          Retry
        </button>
      </div>
    </div>
  {/if}
</div>