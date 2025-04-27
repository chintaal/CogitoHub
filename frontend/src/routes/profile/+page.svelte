<script>
  import { onMount } from 'svelte';
  import { user, updateUserProfile } from '../../lib/stores/authStore';
  import PageGuard from '../../lib/components/PageGuard.svelte';
  
  let displayName = '';
  let loading = false;
  let success = false;
  let error = '';
  
  onMount(() => {
    if ($user) {
      displayName = $user.displayName || '';
    }
  });
  
  async function handleUpdateProfile(e) {
    e.preventDefault();
    
    if (!displayName.trim()) {
      error = 'Display name is required';
      return;
    }
    
    try {
      loading = true;
      error = '';
      success = false;
      
      // Update user data
      const updatedUser = {
        ...$user,
        displayName,
        photoURL: `https://ui-avatars.com/api/?name=${encodeURIComponent(displayName)}`
      };
      
      // Save to localStorage and update store
      localStorage.setItem('cogitohub_user', JSON.stringify(updatedUser));
      user.set(updatedUser);
      
      if ($user.uid) {
        await updateUserProfile($user.uid, {
          displayName,
          photoURL: updatedUser.photoURL
        });
      }
      
      success = true;
    } catch (err) {
      error = err.message || 'An error occurred while updating your profile';
    } finally {
      loading = false;
    }
  }
</script>

<PageGuard>
  <div class="min-h-screen bg-gradient-to-b from-white to-gray-50 py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
      <div class="max-w-3xl mx-auto">
        <div class="bg-white shadow-lg rounded-lg px-8 py-6">
          <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-900">Profile Settings</h2>
            <p class="mt-1 text-sm text-gray-600">
              Update your profile information
            </p>
          </div>
          
          <form onsubmit={handleUpdateProfile} class="space-y-6">
            {#if error}
              <div class="rounded-md bg-red-50 p-4">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-red-800">{error}</p>
                  </div>
                </div>
              </div>
            {/if}
            
            {#if success}
              <div class="rounded-md bg-green-50 p-4">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-green-800">Profile updated successfully</p>
                  </div>
                </div>
              </div>
            {/if}
            
            <div>
              <div class="flex items-center">
                <img 
                  src={$user?.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(displayName || 'User')}`}
                  alt="Profile" 
                  class="h-20 w-20 rounded-full"
                />
                <div class="ml-5">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">Profile Picture</h3>
                  <p class="mt-1 text-sm text-gray-500">
                    Your profile picture is automatically generated from your display name
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label for="display-name" class="block text-sm font-medium text-gray-700">
                Display Name
              </label>
              <div class="mt-1">
                <input
                  type="text"
                  name="display-name"
                  id="display-name"
                  bind:value={displayName}
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Your name"
                />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">
                Email Address
              </label>
              <div class="mt-1">
                <input
                  type="email"
                  disabled
                  value={$user?.email || ''}
                  class="shadow-sm bg-gray-50 block w-full sm:text-sm border-gray-300 rounded-md"
                />
              </div>
              <p class="mt-2 text-sm text-gray-500">
                Email address cannot be changed
              </p>
            </div>
            
            <div class="pt-5">
              <div class="flex justify-end">
                <button
                  type="submit"
                  disabled={loading}
                  class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {#if loading}
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  {/if}
                  Save Changes
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</PageGuard>