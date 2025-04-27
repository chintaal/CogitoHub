<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { user } from '../lib/stores/authStore';
  import NavBar from '../components/navigation/NavBar.svelte';
  
  // Track app loading state
  let appReady = false;
  
  onMount(() => {
    // Check for saved auth state
    const savedUser = localStorage.getItem('cogitohub_user');
    if (savedUser) {
      user.set(JSON.parse(savedUser));
    }
    
    appReady = true;
  });
</script>

{#if appReady}
  <NavBar />
  <slot />
{:else}
  <div class="fixed inset-0 flex items-center justify-center bg-white">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
  </div>
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    min-height: 100vh;
  }
</style>
