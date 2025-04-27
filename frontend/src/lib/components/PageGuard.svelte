<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '../stores/authStore';

  export let requireAuth = true;

  onMount(() => {
    const unsubscribe = user.subscribe(value => {
      if (requireAuth && !value) {
        goto('/login');
      } else if (!requireAuth && value) {
        goto('/cogitohub');
      }
    });

    return unsubscribe;
  });
</script>

<slot></slot>