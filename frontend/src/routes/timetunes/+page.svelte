<script lang="ts">
  import { onMount } from 'svelte';
  import TimetunesLogo from '../../components/logos/timetunesLogo.svelte';
  import TimetunesIcon from '../../components/icons/timetunesIcon.svelte';
  
  // State management
  let timerRunning = false;
  let startTime: Date | null = null;
  let currentTime = new Date();
  let elapsedTime = 0;
  let description = '';
  let selectedProjectId: string | null = null;
  let selectedTags: string[] = [];
  let timerInterval: number | null = null;
  
  // Example data - in a real app, this would be stored in a database
  let projects = [
    { id: 'proj1', name: 'Personal', color: '#FF5733' },
    { id: 'proj2', name: 'Work', color: '#33A8FF' },
    { id: 'proj3', name: 'Learning', color: '#A233FF' },
    { id: 'proj4', name: 'Side Project', color: '#33FF57' }
  ];
  
  let tags = [
    { id: 'tag1', name: 'Important' },
    { id: 'tag2', name: 'Meeting' },
    { id: 'tag3', name: 'Research' },
    { id: 'tag4', name: 'Planning' },
    { id: 'tag5', name: 'Coding' },
    { id: 'tag6', name: 'Reading' }
  ];
  
  let timeEntries = [
    {
      id: 'entry1',
      description: 'Project planning',
      projectId: 'proj2',
      tags: ['tag2', 'tag4'],
      startTime: new Date(new Date().getTime() - 3600000 * 4),
      endTime: new Date(new Date().getTime() - 3600000 * 2),
      duration: 7200000 // 2 hours
    },
    {
      id: 'entry2',
      description: 'Reading documentation',
      projectId: 'proj3',
      tags: ['tag3', 'tag6'],
      startTime: new Date(new Date().setHours(0, 0, 0, 0)), // Today at midnight
      endTime: new Date(new Date().setHours(0, 45, 0, 0)), // 45 minutes later
      duration: 2700000 // 45 minutes
    },
    {
      id: 'entry3',
      description: 'Coding new features',
      projectId: 'proj4',
      tags: ['tag5'],
      startTime: new Date(new Date().getTime() - 86400000), // Yesterday
      endTime: new Date(new Date().getTime() - 86400000 + 10800000), // 3 hours later
      duration: 10800000 // 3 hours
    }
  ];
  
  // Format time as HH:MM:SS
  function formatTime(ms: number) {
    const seconds = Math.floor((ms / 1000) % 60);
    const minutes = Math.floor((ms / 1000 / 60) % 60);
    const hours = Math.floor(ms / 1000 / 60 / 60);
    
    return [
      hours.toString().padStart(2, '0'),
      minutes.toString().padStart(2, '0'),
      seconds.toString().padStart(2, '0')
    ].join(':');
  }
  
  // Format date for display
  function formatDate(date: Date) {
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric'
    });
  }
  
  // Start the timer
  function startTimer() {
    if (timerRunning) return;
    
    startTime = new Date();
    timerRunning = true;
    
    timerInterval = setInterval(() => {
      currentTime = new Date();
      elapsedTime = startTime ? currentTime.getTime() - startTime.getTime() : 0;
    }, 1000) as unknown as number;
  }
  
  // Stop the timer and save the time entry
  function stopTimer() {
    if (!timerRunning || !startTime) return;
    
    timerRunning = false;
    if (timerInterval) clearInterval(timerInterval);
    
    const endTime = new Date();
    const duration = endTime.getTime() - startTime.getTime();
    
    // Create a new time entry
    const newEntry = {
      id: `entry${timeEntries.length + 1}`,
      description: description || 'Untitled',
      projectId: selectedProjectId,
      tags: [...selectedTags],
      startTime,
      endTime,
      duration
    };
    
    timeEntries = [newEntry, ...timeEntries];
    
    // Reset the timer
    resetTimer();
  }
  
  // Reset the timer and form without saving
  function resetTimer() {
    startTime = null;
    elapsedTime = 0;
    description = '';
    selectedProjectId = null;
    selectedTags = [];
    if (timerInterval) clearInterval(timerInterval);
    timerRunning = false;
  }
  
  // Delete a time entry
  function deleteEntry(entryId: string) {
    timeEntries = timeEntries.filter(entry => entry.id !== entryId);
  }
  
  // Find project name by ID
  function getProjectById(projectId: string | null) {
    if (!projectId) return null;
    return projects.find(p => p.id === projectId);
  }
  
  // Group entries by date
  $: entriesByDate = timeEntries.reduce((groups: Record<string, typeof timeEntries>, entry) => {
    const dateKey = entry.startTime.toLocaleDateString();
    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }
    groups[dateKey].push(entry);
    return groups;
  }, {});
  
  // Calculate total time tracked today
  $: todayKey = new Date().toLocaleDateString();
  $: todayEntries = entriesByDate[todayKey] || [];
  $: todayTotal = todayEntries.reduce((total, entry) => total + entry.duration, 0);
  
  // Calculate total time tracked this week
  $: thisWeekTotal = timeEntries
    .filter(entry => {
      const now = new Date();
      const weekStart = new Date(now.setDate(now.getDate() - now.getDay()));
      weekStart.setHours(0, 0, 0, 0);
      return entry.startTime >= weekStart;
    })
    .reduce((total, entry) => total + entry.duration, 0);
  
  // Clean up on unmount
  onMount(() => {
    return () => {
      if (timerInterval) clearInterval(timerInterval);
    };
  });
</script>

<div class="min-h-screen bg-gradient-to-br from-amber-50 to-amber-100">
  <!-- Header -->
  <header class="bg-gradient-to-r from-amber-600 to-amber-800 text-white p-6 shadow-lg">
    <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
      <div class="flex items-center mb-4 md:mb-0">
        <TimetunesLogo size={200} />
        <h1 class="text-3xl font-bold ml-4"></h1>
      </div>
      <div class="flex items-center space-x-4">
        <a href="#dashboard" class="hover:text-amber-200 transition-colors"></a>
        <a href="#reports" class="hover:text-amber-200 transition-colors"></a>
        <a href="#projects" class="hover:text-amber-200 transition-colors"></a>
        <button class="bg-white text-amber-700 px-4 py-2 rounded-full font-semibold hover:bg-amber-100 transition-colors">
          Make Time
        </button>
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-6">
    <!-- Timer Section -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Timer Display -->
        <div class="flex flex-col items-center justify-center p-6 bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl">
          <h2 class="text-4xl font-bold font-mono text-amber-800">
            {formatTime(elapsedTime)}
          </h2>
          <div class="flex space-x-4 mt-6">
            {#if !timerRunning}
              <button 
                on:click={startTimer}
                class="bg-amber-600 hover:bg-amber-700 text-white px-8 py-3 rounded-full font-semibold transition-colors flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                </svg>
                Start
              </button>
            {:else}
              <button 
                on:click={stopTimer}
                class="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-full font-semibold transition-colors flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                </svg>
                Stop
              </button>
            {/if}
            
            <button 
              on:click={resetTimer}
              class="border-2 border-amber-600 text-amber-600 hover:bg-amber-50 px-6 py-3 rounded-full font-semibold transition-colors"
            >
              Reset
            </button>
          </div>
        </div>
        
        <!-- Entry Form -->
        <div class="col-span-2 p-6 border border-amber-200 rounded-xl">
          <div class="flex flex-col space-y-4">
            <input 
              type="text" 
              bind:value={description} 
              placeholder="What are you working on?" 
              class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            />
            
            <div class="flex flex-col sm:flex-row gap-4">
              <!-- Project Selector -->
              <div class="relative flex-1">
                <select 
                  bind:value={selectedProjectId}
                  class="w-full p-3 border border-gray-300 rounded-lg appearance-none bg-white focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                >
                  <option value={null}>Select Project</option>
                  {#each projects as project}
                    <option value={project.id}>{project.name}</option>
                  {/each}
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                  <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
                  </svg>
                </div>
                
                <button class="absolute right-12 top-1/2 transform -translate-y-1/2 text-amber-600 hover:text-amber-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" />
                  </svg>
                </button>
              </div>
              
              <!-- Tags Selector (Simplified) -->
              <div class="relative flex-1">
                <select 
                  multiple
                  bind:value={selectedTags}
                  class="w-full h-12 p-3 border border-gray-300 rounded-lg appearance-none bg-white focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                >
                  {#each tags as tag}
                    <option value={tag.id}>{tag.name}</option>
                  {/each}
                </select>
                
                <button class="absolute right-12 top-1/2 transform -translate-y-1/2 text-amber-600 hover:text-amber-800">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Dashboard Summary -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-xl shadow-md">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">Today</h3>
        <p class="text-3xl font-bold text-amber-700">{formatTime(todayTotal)}</p>
      </div>
      
      <div class="bg-white p-6 rounded-xl shadow-md">
        <h3 class="text-lg font-semibold text-gray-500 mb-2">This Week</h3>
        <p class="text-3xl font-bold text-amber-700">{formatTime(thisWeekTotal)}</p>
      </div>
      
      <div class="bg-white p-6 rounded-xl shadow-md flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-500 mb-2">Goal Progress</h3>
          <p class="text-3xl font-bold text-amber-700">65%</p>
        </div>
        <div class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center">
          <div class="relative w-12 h-12">
            <svg class="w-12 h-12" viewBox="0 0 36 36">
              <circle cx="18" cy="18" r="16" fill="none" stroke="#E0E0E0" stroke-width="3"></circle>
              <circle cx="18" cy="18" r="16" fill="none" stroke="#F59E0B" stroke-width="3" stroke-dasharray="100" stroke-dashoffset="35"></circle>
            </svg>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Time Entries -->
    <section class="bg-white rounded-2xl p-6 shadow-lg">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Recent Time Entries</h2>
      
      {#each Object.entries(entriesByDate) as [dateKey, entries]}
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-600 mb-3">{formatDate(new Date(dateKey))}</h3>
          
          <div class="space-y-3">
            {#each entries as entry}
              <div class="border border-gray-200 rounded-lg p-4 hover:bg-amber-50 transition-colors flex flex-col md:flex-row justify-between">
                <div class="flex-1">
                  <div class="flex items-center">
                    {#if entry.projectId}
                      {#if getProjectById(entry.projectId)}
                        <div class="w-3 h-3 rounded-full mr-2" style={`background-color: ${getProjectById(entry.projectId)?.color}`}></div>
                      {/if}
                      <span class="text-gray-600 text-sm">{getProjectById(entry.projectId)?.name || 'No Project'}</span>
                    {:else}
                      <span class="text-gray-600 text-sm">No Project</span>
                    {/if}
                  </div>
                  <div class="font-semibold">{entry.description}</div>
                  
                  <div class="flex flex-wrap gap-2 mt-2">
                    {#each entry.tags as tagId}
                      {#if tags.find(t => t.id === tagId)}
                        <span class="inline-block bg-amber-100 text-amber-800 text-xs px-2 py-1 rounded-full">
                          {tags.find(t => t.id === tagId)?.name}
                        </span>
                      {/if}
                    {/each}
                  </div>
                </div>
                
                <div class="flex items-center mt-3 md:mt-0">
                  <div class="text-gray-600 text-sm mr-4">
                    {entry.startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - 
                    {entry.endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                  <div class="font-mono font-semibold mr-4">
                    {formatTime(entry.duration)}
                  </div>
                  
                  <div class="flex">
                    <button class="text-gray-400 hover:text-amber-600 p-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button 
                      class="text-gray-400 hover:text-red-600 p-1" 
                      on:click={() => deleteEntry(entry.id)}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/each}
      
      {#if Object.keys(entriesByDate).length === 0}
        <div class="text-center py-8 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <p>No time entries yet. Start tracking your time!</p>
        </div>
      {/if}
    </section>
  </main>
  
  <!-- Footer -->
  <footer class="bg-gray-800 text-white py-8 mt-16">
    <div class="container mx-auto px-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <TimetunesLogo size={40} />
          <p class="mt-2 text-gray-400">Time tracking that works for you</p>
        </div>
        
        <div class="flex space-x-8">
          <div>
            <h4 class="font-semibold mb-3"></h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3"></h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3"></h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
              <li><a href="#" class="hover:text-white"></a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-400">© 2025 TimeTunes. All rights reserved.</p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd"></path>
            </svg>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
            </svg>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd"></path>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</div>

<style>
  /* Additional styles for TimeTunes */
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  
  /* Animation for timer progress */
  @keyframes dash {
    to {
      stroke-dashoffset: 0;
    }
  }
</style>