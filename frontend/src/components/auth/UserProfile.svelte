<script>
  import { onMount, onDestroy } from 'svelte';
  import { user, logOut, getUserProfile, isAuthenticated, isUserLoggedInSync } from '../../lib/stores/authStore';
  import { uploadFile } from '../../lib/firebase/storage';
  import { initializeFirebase } from '../../lib/firebase/firebase';
  import { doc, updateDoc, setDoc } from 'firebase/firestore';
  
  // Fast initial state check for instant rendering
  let initiallyLoggedIn = isUserLoggedInSync();
  
  let userProfile = null;
  let loading = initiallyLoggedIn; // Only show loading if we think the user is logged in
  let saving = false;
  let message = '';
  let messageType = '';
  let displayName = '';
  let photoFile = null;
  let photoURL = '';
  let showDropdown = false;
  let profileMenuRef;
  let profileButtonRef;
  let mobileView = false;
  let profileLoadTimeout;
  
  // Check viewport size
  function updateViewport() {
    mobileView = window.innerWidth < 768;
  }

  // Debounced profile loading for better UX
  async function loadUserProfile() {
    if (!$user) return;
    
    loading = true;
    
    // Cancel any previous timeout
    if (profileLoadTimeout) {
      clearTimeout(profileLoadTimeout);
    }
    
    try {
      userProfile = await getUserProfile($user.uid);
      
      // Update local copies for editing
      if (userProfile) {
        displayName = userProfile.displayName || '';
        photoURL = userProfile.photoURL || '';
      }
    } catch (error) {
      console.error("Error loading user profile:", error);
      message = "Couldn't load profile: " + error.message;
      messageType = 'error';
    } finally {
      loading = false;
    }
  }
  
  // Handle profile dropdown 
  function toggleDropdown() {
    showDropdown = !showDropdown;
  }
  
  // Close dropdown when clicked outside
  function handleClickOutside(event) {
    if (profileButtonRef && profileButtonRef.contains(event.target)) {
      return;
    }
    
    if (profileMenuRef && !profileMenuRef.contains(event.target)) {
      showDropdown = false;
    }
  }
  
  // Save profile changes
  async function saveProfile() {
    if (!$user) return;
    
    saving = true;
    message = '';
    
    try {
      // Initialize Firebase
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not available');
      
      let profileData = {
        displayName
      };
      
      // Handle photo upload if needed
      if (photoFile) {
        const result = await uploadFile(photoFile, `profile-photos/${$user.uid}`, $user.uid);
        
        if (result.success) {
          profileData.photoURL = result.url;
          photoURL = result.url; // Update local display right away
          photoFile = null; // Reset after successful upload
        } else {
          throw new Error('Failed to upload profile photo');
        }
      }
      
      // Update the profile
      await updateDoc(doc(db, 'users', $user.uid), profileData);
      
      message = 'Profile updated successfully';
      messageType = 'success';
      
    } catch (error) {
      console.error("Error saving profile:", error);
      message = "Couldn't save profile: " + error.message;
      messageType = 'error';
    } finally {
      saving = false;
    }
  }
  
  // Handle file selection for profile photo
  function handleFileChange(event) {
    const files = event.target.files;
    if (files && files.length > 0) {
      photoFile = files[0];
      
      // Preview the selected image
      const reader = new FileReader();
      reader.onload = (e) => {
        photoURL = e.target.result;
      };
      reader.readAsDataURL(photoFile);
    }
  }
  
  // Handle user logging out
  async function handleLogout() {
    await logOut();
  }
  
  // Mount with proper window event listeners
  onMount(() => {
    // Check viewport on initial load
    updateViewport();
    window.addEventListener('resize', updateViewport);
    document.addEventListener('click', handleClickOutside);
    
    // Load profile if user is logged in
    const unsubscribe = user.subscribe(userData => {
      if (userData) {
        loadUserProfile();
      } else {
        userProfile = null;
      }
    });
    
    return () => {
      window.removeEventListener('resize', updateViewport);
      document.removeEventListener('click', handleClickOutside);
      unsubscribe();
    };
  });
  
  // Clean up event listeners on component destroy
  onDestroy(() => {
    window.removeEventListener('resize', updateViewport);
    document.removeEventListener('click', handleClickOutside);
  });
</script>

<!-- Rest of the component remains the same -->
{#if $isAuthenticated}
  <div class="relative inline-block text-left">
    <button 
      bind:this={profileButtonRef}
      on:click={toggleDropdown}
      class="flex items-center space-x-2 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
      aria-expanded={showDropdown} 
      aria-haspopup="true"
    >
      {#if photoURL}
        <img src={photoURL} alt="Profile" class="w-8 h-8 rounded-full object-cover border border-gray-200" />
      {:else}
        <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-sm font-medium">
          {displayName ? displayName[0]?.toUpperCase() : ($user?.email?.[0]?.toUpperCase() || 'U')}
        </div>
      {/if}
      {#if !mobileView}
        <span class="text-sm font-medium text-gray-700">{displayName || ($user?.email?.split('@')[0] || 'User')}</span>
        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 011.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path>
        </svg>
      {/if}
    </button>
    
    {#if showDropdown}
      <div 
        bind:this={profileMenuRef}
        class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none z-50"
        role="menu" 
        aria-orientation="vertical" 
        aria-labelledby="options-menu"
      >
        <div class="py-1" role="none">
          <a href="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">
            Your Profile
          </a>
          <a href="/dashboard" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">
            Dashboard
          </a>
        </div>
        <div class="py-1" role="none">
          <button 
            on:click={handleLogout}
            class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" 
            role="menuitem"
          >
            Sign out
          </button>
        </div>
      </div>
    {/if}
  </div>
{:else}
  <div class="flex space-x-4">
    <a href="/login" class="text-sm font-medium text-blue-600 hover:text-blue-800">Sign in</a>
  </div>
{/if}