<script>
  import { user } from '../../lib/stores/authStore';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  
  let dropdownOpen = false;
  
  function toggleDropdown() {
    dropdownOpen = !dropdownOpen;
  }
  
  async function handleLogout() {
    try {
      await logout();
      goto('/login');
    } catch (error) {
      console.error('Error during logout:', error);
    }
  }
</script>

<nav class="bg-white shadow-lg">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex justify-between h-16">
      <div class="flex">
        <div class="flex-shrink-0 flex items-center">
          <a href="/" class="text-xl font-bold text-gray-800">CogitoHub</a>
        </div>
      </div>

      {#if $user}
        <div class="flex items-center">
          <div class="relative">
            <button 
              on:click={toggleDropdown}
              class="flex items-center space-x-3 focus:outline-none"
            >
              <img
                src={$user.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent($user.displayName || 'User')}`}
                alt="Profile"
                class="h-8 w-8 rounded-full"
              />
              <span class="text-gray-700">{$user.displayName || 'User'}</span>
            </button>

            {#if dropdownOpen}
              <div 
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1"
                on:click={() => dropdownOpen = false}
              >
                <a 
                  href="/profile" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Profile
                </a>
                <a 
                  href="/settings"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Settings
                </a>
                <button
                  on:click={handleLogout}
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Sign out
                </button>
              </div>
            {/if}
          </div>
        </div>
      {:else}
        <div class="flex items-center">
          <a
            href="/login"
            class="ml-4 px-4 py-2 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
          >
            Sign in
          </a>
        </div>
      {/if}
    </div>
  </div>
</nav>