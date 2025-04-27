<script>
  import { signUp, authError } from '../../lib/stores/authStore';
  import { onMount } from 'svelte';
  import UserTypeSelection from '../cogitohub/UserTypeSelection.svelte';
  
  export let onSuccess = () => {};
  export let showLogin = () => {};
  
  let displayName = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let tenantId = 'personal';
  let loading = false;
  let errorMessage = '';
  let showTenantField = false;
  let showUserTypeSelection = false;
  let tempUserData = null;
  
  onMount(() => {
    const unsubscribe = authError.subscribe((error) => {
      errorMessage = error;
      loading = false;
    });
    
    return () => {
      unsubscribe();
    };
  });
  
  async function handleSubmit() {
    loading = true;
    errorMessage = '';
    
    // Basic validation
    if (!displayName || !email || !password || !confirmPassword) {
      errorMessage = 'Please fill in all fields';
      loading = false;
      return;
    }
    
    if (password !== confirmPassword) {
      errorMessage = 'Passwords do not match';
      loading = false;
      return;
    }
    
    if (password.length < 6) {
      errorMessage = 'Password must be at least 6 characters';
      loading = false;
      return;
    }
    
    // Register user with Firebase but don't complete onboarding yet
    const user = await signUp(email, password, displayName, tenantId);
    if (user) {
      tempUserData = user;
      showUserTypeSelection = true;
      loading = false;
    }
  }
  
  function toggleTenantField() {
    showTenantField = !showTenantField;
  }

  async function handleUserTypeSelection(event) {
    const { userType, additionalInfo } = event.detail;
    loading = true;

    try {
      // Update the user's profile with type and additional info
      const updateResult = await updateUserProfile(tempUserData.uid, {
        userType,
        ...additionalInfo,
        onboardingCompleted: true
      });

      if (updateResult.success) {
        onSuccess();
      }
    } catch (error) {
      console.error('Error updating user profile:', error);
      errorMessage = 'Failed to complete setup: ' + error.message;
    } finally {
      loading = false;
    }
  }
</script>

{#if !showUserTypeSelection}
  <div class="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
    <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Create Account</h2>
    
    {#if errorMessage}
      <div class="bg-red-50 text-red-700 p-3 rounded-md mb-4 text-sm">
        {errorMessage}
      </div>
    {/if}
    
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      <div>
        <label for="displayName" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
        <input 
          type="text" 
          id="displayName" 
          bind:value={displayName} 
          class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
          placeholder="John Doe"
          required 
        />
      </div>
      
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input 
          type="email" 
          id="email" 
          bind:value={email} 
          class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
          placeholder="your@email.com"
          required 
        />
      </div>
      
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <input 
          type="password" 
          id="password" 
          bind:value={password} 
          class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
          placeholder="••••••••"
          required 
        />
      </div>
      
      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
        <input 
          type="password" 
          id="confirmPassword" 
          bind:value={confirmPassword} 
          class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
          placeholder="••••••••"
          required 
        />
      </div>
      
      <div class="flex items-center">
        <input 
          type="checkbox" 
          id="advancedOptions" 
          on:change={toggleTenantField} 
          class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" 
        />
        <label for="advancedOptions" class="ml-2 block text-sm text-gray-700">
          I'm joining an organization/team
        </label>
      </div>
      
      {#if showTenantField}
        <div>
          <label for="tenantId" class="block text-sm font-medium text-gray-700 mb-1">Organization ID</label>
          <input 
            type="text" 
            id="tenantId" 
            bind:value={tenantId} 
            class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
            placeholder="organization-id"
          />
          <p class="mt-1 text-xs text-gray-500">
            Enter your organization ID or leave as "personal" for individual use
          </p>
        </div>
      {/if}
      
      <button 
        type="submit" 
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50" 
        disabled={loading}
      >
        {#if loading}
          <span class="inline-block animate-spin mr-2">⟳</span>
        {/if}
        Create Account
      </button>
    </form>

    <div class="mt-6 text-center text-sm">
      <span>Already have an account?</span>
      <button 
        on:click={showLogin} 
        class="text-blue-600 hover:text-blue-800 font-medium ml-2"
      >
        Sign in
      </button>
    </div>
  </div>
{:else}
  <UserTypeSelection on:userTypeSelected={handleUserTypeSelection} />
{/if}