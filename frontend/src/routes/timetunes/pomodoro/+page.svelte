<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import TimetunesLogo from '../../../components/logos/timetunesLogo.svelte';
  
  // Pomodoro states
  const WORK = 'work';
  const SHORT_BREAK = 'short-break';
  const LONG_BREAK = 'long-break';
  
  // Settings
  let workDuration = 25 * 60; // 25 minutes in seconds
  let shortBreakDuration = 5 * 60; // 5 minutes in seconds
  let longBreakDuration = 15 * 60; // 15 minutes in seconds
  let longBreakInterval = 4; // Long break after 4 work sessions
  
  // State variables
  let timerState = WORK;
  let timeLeft = workDuration;
  let isRunning = false;
  let completedSessions = 0;
  let timerInterval: number | null = null;
  let startTime: Date | null = null;
  let progress = 100;
  
  // Session history
  let sessions = [];
  
  // Sound effects
  let workCompleteSound: HTMLAudioElement;
  let breakCompleteSound: HTMLAudioElement;
  let notificationsEnabled = true;
  
  // Calculate current session total time
  $: currentSessionTotalTime = timerState === WORK 
    ? workDuration 
    : timerState === SHORT_BREAK 
      ? shortBreakDuration 
      : longBreakDuration;
  
  // Format time as MM:SS
  function formatTime(seconds: number) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  // Initialize audio on component mount
  onMount(() => {
    workCompleteSound = new Audio('/src/assets/sounds/complete.mp3');
    breakCompleteSound = new Audio('/src/assets/sounds/break-over.mp3');
    
    // Request notification permission
    if (Notification && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
    
    // Check if there's a saved state in localStorage
    const savedState = localStorage.getItem('pomodoroState');
    if (savedState) {
      const state = JSON.parse(savedState);
      workDuration = state.workDuration || workDuration;
      shortBreakDuration = state.shortBreakDuration || shortBreakDuration;
      longBreakDuration = state.longBreakDuration || longBreakDuration;
      longBreakInterval = state.longBreakInterval || longBreakInterval;
      completedSessions = state.completedSessions || 0;
      sessions = state.sessions || [];
    }
    
    return () => {
      if (timerInterval) clearInterval(timerInterval);
    };
  });
  
  // Save state when component is destroyed
  onDestroy(() => {
    if (timerInterval) clearInterval(timerInterval);
    
    // Save state to localStorage
    const state = {
      workDuration,
      shortBreakDuration,
      longBreakDuration,
      longBreakInterval,
      completedSessions,
      sessions
    };
    localStorage.setItem('pomodoroState', JSON.stringify(state));
  });
  
  // Start the timer
  function startTimer() {
    if (isRunning) return;
    
    isRunning = true;
    startTime = new Date();
    
    timerInterval = setInterval(() => {
      if (timeLeft > 0) {
        timeLeft--;
        progress = (timeLeft / currentSessionTotalTime) * 100;
      } else {
        completeSession();
      }
    }, 1000) as unknown as number;
  }
  
  // Pause the timer
  function pauseTimer() {
    if (!isRunning) return;
    
    isRunning = false;
    if (timerInterval) clearInterval(timerInterval);
  }
  
  // Reset the timer
  function resetTimer() {
    if (timerInterval) clearInterval(timerInterval);
    
    isRunning = false;
    timeLeft = getCurrentSessionDuration();
    progress = 100;
  }
  
  // Skip to next session
  function skipSession() {
    if (timerInterval) clearInterval(timerInterval);
    completeSession();
  }
  
  // Complete current session and move to next
  function completeSession() {
    if (timerInterval) clearInterval(timerInterval);
    isRunning = false;
    
    // Log completed session
    const endTime = new Date();
    const sessionDuration = timerState === WORK ? workDuration : timerState === SHORT_BREAK ? shortBreakDuration : longBreakDuration;
    
    if (startTime) {
      sessions = [...sessions, {
        type: timerState,
        duration: sessionDuration,
        startTime,
        endTime
      }];
    }
    
    // Determine next session type
    if (timerState === WORK) {
      completedSessions++;
      
      // Play sound
      if (notificationsEnabled) {
        workCompleteSound.play();
        showNotification('Work session complete', 'Take a break!');
      }
      
      // Determine if we need a short or long break
      if (completedSessions % longBreakInterval === 0) {
        timerState = LONG_BREAK;
      } else {
        timerState = SHORT_BREAK;
      }
    } else {
      // If it was a break, next is work
      timerState = WORK;
      
      // Play sound
      if (notificationsEnabled) {
        breakCompleteSound.play();
        showNotification('Break is over', 'Time to focus!');
      }
    }
    
    timeLeft = getCurrentSessionDuration();
    progress = 100;
  }
  
  // Get current session duration based on state
  function getCurrentSessionDuration() {
    switch (timerState) {
      case WORK:
        return workDuration;
      case SHORT_BREAK:
        return shortBreakDuration;
      case LONG_BREAK:
        return longBreakDuration;
      default:
        return workDuration;
    }
  }
  
  // Update durations when settings are changed
  function updateDurations() {
    // If timer is not running, update the current timeLeft
    if (!isRunning) {
      timeLeft = getCurrentSessionDuration();
      progress = 100;
    }
  }
  
  // Show browser notification
  function showNotification(title: string, body: string) {
    if (!notificationsEnabled) return;
    
    if (Notification && Notification.permission === 'granted') {
      new Notification(title, {
        body,
        icon: '/src/assets/Logos/timetunes-icon.png'
      });
    }
  }
  
  // Get background color based on timer state
  $: bgColor = timerState === WORK 
    ? 'bg-amber-600' 
    : timerState === SHORT_BREAK 
      ? 'bg-green-500' 
      : 'bg-blue-600';
  
  // Get text color based on timer state
  $: textColor = timerState === WORK 
    ? 'text-amber-600' 
    : timerState === SHORT_BREAK 
      ? 'text-green-500' 
      : 'text-blue-600';
</script>

<div class="min-h-screen bg-gradient-to-br from-amber-50 to-amber-100">
  <!-- Header -->
  <header class="bg-gradient-to-r from-amber-600 to-amber-800 text-white p-6 shadow-lg">
    <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
      <div class="flex items-center mb-4 md:mb-0">
        <a href="/timetunes" class="flex items-center no-underline text-white">
          <TimetunesLogo size={50} />
          <h1 class="text-3xl font-bold ml-4">TimeTunes</h1>
        </a>
      </div>
      <div class="flex items-center space-x-4">
        <a href="/timetunes" class="hover:text-amber-200 transition-colors">Timer</a>
        <a href="/timetunes#dashboard" class="hover:text-amber-200 transition-colors">Dashboard</a>
        <a href="/timetunes/reports" class="hover:text-amber-200 transition-colors">Reports</a>
        <a href="/timetunes/projects" class="hover:text-amber-200 transition-colors">Projects</a>
        <a href="/timetunes/pomodoro" class="text-amber-200 font-medium transition-colors border-b-2 border-amber-200 pb-1">Pomodoro</a>
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-6">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Pomodoro Timer -->
      <div class="lg:col-span-2">
        <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Pomodoro Timer</h2>
          
          <!-- Timer Display -->
          <div class="flex flex-col items-center mb-8">
            <div class="relative w-64 h-64">
              <!-- Timer Circle -->
              <svg class="w-full h-full" viewBox="0 0 100 100">
                <!-- Background Circle -->
                <circle 
                  cx="50" cy="50" r="45" 
                  fill="none" 
                  stroke="#f3f4f6" 
                  stroke-width="8"
                />
                
                <!-- Progress Circle -->
                <circle 
                  cx="50" cy="50" r="45" 
                  fill="none" 
                  stroke={timerState === WORK ? '#d97706' : timerState === SHORT_BREAK ? '#10b981' : '#2563eb'} 
                  stroke-width="8"
                  stroke-dasharray="283"
                  stroke-dashoffset={283 - (283 * progress / 100)}
                  transform="rotate(-90 50 50)"
                />
              </svg>
              
              <!-- Timer Text -->
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-4xl font-bold mb-1">{formatTime(timeLeft)}</span>
                <span class="uppercase tracking-wider font-medium text-sm opacity-75">
                  {timerState === WORK ? 'Focus' : timerState === SHORT_BREAK ? 'Short Break' : 'Long Break'}
                </span>
              </div>
            </div>
            
            <!-- Session Counter -->
            <div class="mt-4 flex items-center">
              {#each Array(longBreakInterval) as _, i}
                <div 
                  class={`w-3 h-3 mx-1 rounded-full ${i < completedSessions % longBreakInterval ? bgColor : 'bg-gray-300'}`}
                ></div>
              {/each}
            </div>
            <div class="mt-2 text-sm text-gray-600">
              Session {Math.floor(completedSessions / longBreakInterval) * longBreakInterval + (completedSessions % longBreakInterval) + 1}
            </div>
          </div>
          
          <!-- Timer Controls -->
          <div class="flex justify-center space-x-4 mb-6">
            {#if !isRunning}
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
                on:click={pauseTimer}
                class="bg-amber-600 hover:bg-amber-700 text-white px-8 py-3 rounded-full font-semibold transition-colors flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                Pause
              </button>
            {/if}
            
            <button 
              on:click={resetTimer}
              class="border-2 border-amber-600 text-amber-600 hover:bg-amber-50 px-6 py-3 rounded-full font-semibold transition-colors"
            >
              Reset
            </button>
            
            <button 
              on:click={skipSession}
              class="border-2 border-gray-300 text-gray-600 hover:bg-gray-50 px-6 py-3 rounded-full font-semibold transition-colors"
            >
              Skip
            </button>
          </div>
          
          <!-- Session Selector -->
          <div class="flex justify-center space-x-2 mb-6">
            <button 
              class={`py-2 px-4 rounded-lg font-medium transition-colors ${timerState === WORK ? 'bg-amber-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              on:click={() => { timerState = WORK; resetTimer(); }}
            >
              Focus
            </button>
            
            <button 
              class={`py-2 px-4 rounded-lg font-medium transition-colors ${timerState === SHORT_BREAK ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              on:click={() => { timerState = SHORT_BREAK; resetTimer(); }}
            >
              Short Break
            </button>
            
            <button 
              class={`py-2 px-4 rounded-lg font-medium transition-colors ${timerState === LONG_BREAK ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
              on:click={() => { timerState = LONG_BREAK; resetTimer(); }}
            >
              Long Break
            </button>
          </div>
        </section>
        
        <!-- Today's Sessions -->
        <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Today's Sessions</h2>
          
          {#if sessions.length === 0}
            <div class="text-center py-8 text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p>No completed sessions yet. Start your first Pomodoro session!</p>
            </div>
          {:else}
            <div class="space-y-3">
              {#each sessions.slice(0, 5) as session, index}
                <div class="border border-gray-200 rounded-lg p-3 hover:bg-amber-50 transition-colors">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center">
                      <div class={`w-3 h-3 rounded-full mr-2 ${
                        session.type === WORK 
                          ? 'bg-amber-600' 
                          : session.type === SHORT_BREAK 
                            ? 'bg-green-500' 
                            : 'bg-blue-600'
                      }`}></div>
                      <span class="font-medium">
                        {session.type === WORK ? 'Focus session' : session.type === SHORT_BREAK ? 'Short break' : 'Long break'}
                      </span>
                    </div>
                    <span class="text-gray-500 text-sm">
                      {formatTime(session.duration)}
                    </span>
                  </div>
                </div>
              {/each}
              
              {#if sessions.length > 5}
                <div class="text-center mt-4">
                  <button class="text-amber-600 hover:text-amber-700 font-medium text-sm">
                    Show all sessions ({sessions.length})
                  </button>
                </div>
              {/if}
            </div>
          {/if}
        </section>
      </div>
      
      <!-- Settings Panel -->
      <div class="lg:col-span-1">
        <section class="bg-white rounded-2xl p-6 shadow-lg sticky top-6">
          <h2 class="text-xl font-bold text-gray-800 mb-6">Timer Settings</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Focus Duration (minutes)
              </label>
              <input 
                type="number" 
                bind:value={workDuration}
                on:change={() => { workDuration = workDuration * 60; updateDurations(); }}
                min="1" 
                max="60"
                step="1"
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Short Break Duration (minutes)
              </label>
              <input 
                type="number" 
                bind:value={shortBreakDuration}
                on:change={() => { shortBreakDuration = shortBreakDuration * 60; updateDurations(); }}
                min="1" 
                max="30"
                step="1"
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Long Break Duration (minutes)
              </label>
              <input 
                type="number" 
                bind:value={longBreakDuration}
                on:change={() => { longBreakDuration = longBreakDuration * 60; updateDurations(); }}
                min="1" 
                max="60"
                step="1"
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Long Break Interval
              </label>
              <input 
                type="number" 
                bind:value={longBreakInterval}
                min="1" 
                max="10"
                step="1"
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              />
              <p class="text-sm text-gray-500 mt-1">
                Number of focus sessions before a long break
              </p>
            </div>
            
            <div>
              <label for="notifications" class="flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  id="notifications" 
                  bind:checked={notificationsEnabled}
                  class="sr-only" 
                />
                <div 
                  class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner"
                  class:bg-amber-500={notificationsEnabled}
                >
                  <div 
                    class="dot absolute w-4 h-4 bg-white rounded-full shadow transition-all"
                    class:left-1={!notificationsEnabled}
                    class:left-5={notificationsEnabled}
                    style="top: 0.25rem;"
                  ></div>
                </div>
                <div class="ml-3 text-gray-700 font-medium">
                  Sound & Notification Alerts
                </div>
              </label>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <h3 class="text-lg font-semibold mb-2">Pomodoro Statistics</h3>
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-amber-50 p-3 rounded-lg">
                  <div class="text-sm text-gray-600">Focus Sessions</div>
                  <div class="text-2xl font-bold text-amber-700">
                    {sessions.filter(s => s.type === WORK).length}
                  </div>
                </div>
                
                <div class="bg-blue-50 p-3 rounded-lg">
                  <div class="text-sm text-gray-600">Break Sessions</div>
                  <div class="text-2xl font-bold text-blue-700">
                    {sessions.filter(s => s.type === SHORT_BREAK || s.type === LONG_BREAK).length}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
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
            <h4 class="font-semibold mb-3">Product</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">Features</a></li>
              <li><a href="#" class="hover:text-white">Pricing</a></li>
              <li><a href="#" class="hover:text-white">Apps</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3">Resources</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">Blog</a></li>
              <li><a href="#" class="hover:text-white">Help Center</a></li>
              <li><a href="#" class="hover:text-white">Contact</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3">Company</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">About Us</a></li>
              <li><a href="#" class="hover:text-white">Careers</a></li>
              <li><a href="#" class="hover:text-white">Legal</a></li>
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
  
  /* Circle animation */
  circle {
    transition: stroke-dashoffset 0.5s ease-in-out;
  }
  
  /* Toggle switch styling */
  input:checked ~ .dot {
    transform: translateX(100%);
  }
  
  input:checked ~ div {
    background-color: #F59E0B;
  }
</style>