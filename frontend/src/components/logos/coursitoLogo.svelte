<script lang="ts">
    // Props for customization
    export let src: string = 'src/assets/Logos/coursito-full.png';
    export let alt: string = 'Coursito Logo';
    export let size: number = 40;
    export let showText: boolean = true;
    
    // Note: We're not using the route prop anymore - keeping it hardcoded for reliability
  </script>
  
  <!-- Use a simple anchor tag for the most reliable browser navigation behavior -->
  <a 
    href="/coursito" 
    class="no-underline cursor-pointer flex items-center gap-2 select-none transition-transform hover:scale-105 duration-300"
    aria-label={alt}
  >
    <img src={src} alt={alt} width={size} height={size} class="object-contain" />
    {#if showText}
      <span class="text-xl font-semibold text-white hidden sm:block">
        Coursito
      </span>
    {/if}
  </a>