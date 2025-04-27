<script>
  import { signIn, signInWithGoogle, authError, resetPassword } from '../../lib/stores/authStore';
  import { onMount } from 'svelte';
  
  export let onSuccess = () => {};
  export let showSignUp = () => {};
  
  let email = '';
  let password = '';
  let loading = false;
  let errorMessage = '';
  let resetMode = false;
  let resetEmailSent = false;
  
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
    
    if (resetMode) {
      const success = await resetPassword(email);
      loading = false;
      if (success) {
        resetEmailSent = true;
      }
      return;
    }
    
    if (!email || !password) {
      errorMessage = 'Please enter both email and password';
      loading = false;
      return;
    }
    
    const user = await signIn(email, password);
    if (user) {
      onSuccess();
    }
  }
  
  async function handleGoogleSignIn() {
    loading = true;
    errorMessage = '';
    
    const user = await signInWithGoogle();
    if (user) {
      onSuccess();
    }
  }
  
  function toggleResetMode() {
    resetMode = !resetMode;
    errorMessage = '';
    resetEmailSent = false;
  }
</script>

<div class="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
  <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">
    {resetMode ? 'Reset Password' : 'Welcome Back'}
  </h2>
  
  {#if errorMessage}
    <div class="bg-red-50 text-red-700 p-3 rounded-md mb-4 text-sm">
      {errorMessage}
    </div>
  {/if}
  
  {#if resetEmailSent}
    <div class="bg-green-50 text-green-700 p-3 rounded-md mb-4 text-sm">
      Password reset email sent. Please check your inbox.
    </div>
  {/if}
  
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
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
    
    {#if !resetMode}
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
    {/if}
    
    <button 
      type="submit" 
      class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50" 
      disabled={loading}
    >
      {#if loading}
        <span class="inline-block animate-spin mr-2">⟳</span>
      {/if}
      {resetMode ? 'Send Reset Link' : 'Sign In'}
    </button>
  </form>
  
  {#if !resetMode}
    <div class="my-4 flex items-center">
      <div class="flex-grow border-t border-gray-200"></div>
      <span class="px-3 text-gray-500 text-sm">or</span>
      <div class="flex-grow border-t border-gray-200"></div>
    </div>
    
    <button 
      on:click={handleGoogleSignIn} 
      class="w-full py-2 px-4 bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center justify-center space-x-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50" 
      disabled={loading}
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="24" height="24">
        <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
        <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
        <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
        <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
      </svg>
      <span>Sign in with Google</span>
    </button>
  {/if}
  
  <div class="mt-6 text-center text-sm">
    {#if resetMode}
      <button 
        on:click={toggleResetMode} 
        class="text-blue-600 hover:text-blue-800 font-medium"
      >
        Back to login
      </button>
    {:else}
      <button 
        on:click={toggleResetMode} 
        class="text-blue-600 hover:text-blue-800 font-medium"
      >
        Forgot password?
      </button>
      <span class="mx-2 text-gray-500">|</span>
      <button 
        on:click={showSignUp} 
        class="text-blue-600 hover:text-blue-800 font-medium"
      >
        Create an account
      </button>
    {/if}
  </div>
</div>