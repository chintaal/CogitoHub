<script lang="ts">
  // Props for customization
  export let src: string = '/src/assets/Logos/timetunes-full.png';
  export let alt: string = 'TimeTunes Logo';
  export let size: number = 40;
  export let showText: boolean = false;
  export let textColor: string = 'text-white';
</script>

<!-- Use a simple anchor tag for the most reliable browser navigation behavior -->
<a 
  href="/timetunes" 
  class="no-underline cursor-pointer flex items-center gap-2 select-none transition-transform hover:scale-105 duration-300"
  aria-label={alt}
>
  <img src={src} alt={alt} width={size} height={size} class="object-contain" />
  {#if showText}
    <span class={`text-xl font-semibold ${textColor} hidden sm:block`}>
      TimeTunes
    </span>
  {/if}
</a>