<script lang="ts">
  import { onMount } from 'svelte';
  import TimetunesLogo from '../../../components/logos/timetunesLogo.svelte';
  
  // User profile data (mock)
  let user = {
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    profilePicture: 'https://i.pravatar.cc/150?img=12',
    jobTitle: 'Product Designer',
    timeZone: 'America/New_York'
  };
  
  // App settings (mock)
  let settings = {
    theme: 'light',
    roundTime: 'nearest_15min',
    trackIdleTime: true,
    autoStartOnAppOpen: false,
    showNotifications: true,
    pomodoroEnabled: true,
    pomodoroWorkDuration: 25,
    pomodoroBreakDuration: 5,
    weekStartsOn: 0 // 0 = Sunday
  };
  
  // Integration settings (mock)
  let integrations = [
    { id: 'gcal', name: 'Google Calendar', connected: true, icon: 'google', lastSynced: '2025-04-11T22:30:00Z' },
    { id: 'outlook', name: 'Microsoft Outlook', connected: false, icon: 'microsoft' },
    { id: 'slack', name: 'Slack', connected: true, icon: 'slack', lastSynced: '2025-04-12T12:15:00Z' },
    { id: 'asana', name: 'Asana', connected: false, icon: 'asana' },
    { id: 'github', name: 'GitHub', connected: true, icon: 'github', lastSynced: '2025-04-12T10:45:00Z' }
  ];
  
  // Export/Import data (mock functions)
  function exportData() {
    // In a real app, this would trigger a file download
    alert('Data export started! (In a real app, this would download a file)');
  }
  
  function importData() {
    // In a real app, this would open a file picker
    alert('In a real app, this would open a file picker for importing data');
  }
  
  // Save settings
  function saveSettings() {
    // In a real app, this would send the settings to the backend
    alert('Settings saved successfully!');
  }
  
  // Toggle theme
  function toggleTheme() {
    settings.theme = settings.theme === 'light' ? 'dark' : 'light';
  }
  
  // Toggle integration connection
  function toggleIntegration(id: string) {
    const integration = integrations.find(i => i.id === id);
    if (integration) {
      integration.connected = !integration.connected;
      if (integration.connected) {
        integration.lastSynced = new Date().toISOString();
        alert(`Connected to ${integration.name}!`);
      } else {
        delete integration.lastSynced;
        alert(`Disconnected from ${integration.name}.`);
      }
      
      // Update integrations array to trigger UI update
      integrations = [...integrations];
    }
  }
  
  // Format date for display
  function formatDate(dateString: string) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  }
  
  // Available time zones
  const timeZones = [
    'Pacific/Honolulu',
    'America/Anchorage',
    'America/Los_Angeles',
    'America/Denver',
    'America/Chicago',
    'America/New_York',
    'America/Sao_Paulo',
    'Europe/London',
    'Europe/Paris',
    'Europe/Moscow',
    'Asia/Dubai',
    'Asia/Kolkata',
    'Asia/Singapore',
    'Asia/Tokyo',
    'Australia/Sydney',
    'Pacific/Auckland'
  ];
  
  // Current tab
  let activeTab = 'profile';
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
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-6">
    <!-- Settings Header -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Settings</h1>
        <button 
          on:click={saveSettings}
          class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          Save Changes
        </button>
      </div>
    </section>
    
    <!-- Settings Navigation Tabs -->
    <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
      <div class="border-b border-gray-200">
        <nav class="flex">
          <button 
            class={`px-6 py-4 text-sm font-medium ${activeTab === 'profile' ? 'text-amber-600 border-b-2 border-amber-600' : 'text-gray-500 hover:text-amber-600'}`}
            on:click={() => activeTab = 'profile'}
          >
            Profile
          </button>
          <button 
            class={`px-6 py-4 text-sm font-medium ${activeTab === 'preferences' ? 'text-amber-600 border-b-2 border-amber-600' : 'text-gray-500 hover:text-amber-600'}`}
            on:click={() => activeTab = 'preferences'}
          >
            Preferences
          </button>
          <button 
            class={`px-6 py-4 text-sm font-medium ${activeTab === 'integrations' ? 'text-amber-600 border-b-2 border-amber-600' : 'text-gray-500 hover:text-amber-600'}`}
            on:click={() => activeTab = 'integrations'}
          >
            Integrations
          </button>
          <button 
            class={`px-6 py-4 text-sm font-medium ${activeTab === 'data' ? 'text-amber-600 border-b-2 border-amber-600' : 'text-gray-500 hover:text-amber-600'}`}
            on:click={() => activeTab = 'data'}
          >
            Data Management
          </button>
        </nav>
      </div>
      
      <!-- Profile Settings -->
      {#if activeTab === 'profile'}
        <div class="p-6">
          <div class="max-w-3xl mx-auto">
            <h2 class="text-xl font-bold mb-6">User Profile</h2>
            
            <div class="flex flex-col md:flex-row mb-8">
              <div class="md:w-1/3 mb-6 md:mb-0 flex flex-col items-center">
                <div class="w-32 h-32 rounded-full overflow-hidden mb-4">
                  <img 
                    src={user.profilePicture} 
                    alt="{user.name}'s profile picture"
                    class="w-full h-full object-cover"
                  />
                </div>
                <button class="text-sm text-amber-600 hover:text-amber-700">
                  Change Picture
                </button>
              </div>
              
              <div class="md:w-2/3">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                    <input 
                      type="text" 
                      id="name"
                      bind:value={user.name}
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                    <input 
                      type="email" 
                      id="email"
                      bind:value={user.email}
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div>
                    <label for="job-title" class="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                    <input 
                      type="text" 
                      id="job-title"
                      bind:value={user.jobTitle}
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div>
                    <label for="timezone" class="block text-sm font-medium text-gray-700 mb-1">Time Zone</label>
                    <select 
                      id="timezone"
                      bind:value={user.timeZone}
                      class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    >
                      {#each timeZones as tz}
                        <option value={tz}>{tz}</option>
                      {/each}
                    </select>
                  </div>
                </div>
                
                <div class="mt-8">
                  <h3 class="text-lg font-semibold mb-4">Account Security</h3>
                  
                  <div class="space-y-4">
                    <button class="text-amber-600 hover:text-amber-700 font-medium">
                      Change Password
                    </button>
                    
                    <div>
                      <label for="2fa" class="flex items-center cursor-pointer">
                        <input type="checkbox" id="2fa" class="sr-only" />
                        <div class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner">
                          <div class="dot absolute w-4 h-4 bg-white rounded-full shadow left-1 top-1 transition"></div>
                        </div>
                        <div class="ml-3 text-gray-700 font-medium">Enable Two-Factor Authentication</div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/if}
      
      <!-- App Preferences -->
      {#if activeTab === 'preferences'}
        <div class="p-6">
          <div class="max-w-3xl mx-auto">
            <h2 class="text-xl font-bold mb-6">Application Preferences</h2>
            
            <div class="space-y-8">
              <!-- Display Settings -->
              <div>
                <h3 class="text-lg font-semibold mb-4">Display Settings</h3>
                
                <div class="space-y-4">
                  <div>
                    <label for="theme" class="flex items-center justify-between cursor-pointer">
                      <span class="text-gray-700">Theme</span>
                      <div class="flex items-center">
                        <span class="text-gray-500 mr-3">{settings.theme === 'light' ? 'Light' : 'Dark'}</span>
                        <button 
                          on:click={toggleTheme}
                          class="w-12 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out"
                          class:bg-amber-500={settings.theme === 'dark'}
                        >
                          <div 
                            class="bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out"
                            class:translate-x-6={settings.theme === 'dark'} 
                          ></div>
                        </button>
                      </div>
                    </label>
                  </div>
                  
                  <div>
                    <label for="week-start" class="block text-sm font-medium text-gray-700 mb-1">Week Starts On</label>
                    <select 
                      id="week-start"
                      bind:value={settings.weekStartsOn}
                      class="w-full md:w-64 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    >
                      <option value={0}>Sunday</option>
                      <option value={1}>Monday</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <!-- Time Tracking Settings -->
              <div>
                <h3 class="text-lg font-semibold mb-4">Time Tracking</h3>
                
                <div class="space-y-4">
                  <div>
                    <label for="round-time" class="block text-sm font-medium text-gray-700 mb-1">Round Time Entries</label>
                    <select 
                      id="round-time"
                      bind:value={settings.roundTime}
                      class="w-full md:w-64 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                    >
                      <option value="none">Don't round</option>
                      <option value="nearest_5min">Nearest 5 minutes</option>
                      <option value="nearest_15min">Nearest 15 minutes</option>
                      <option value="nearest_30min">Nearest 30 minutes</option>
                    </select>
                  </div>
                  
                  <div>
                    <label for="track-idle" class="flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        id="track-idle" 
                        bind:checked={settings.trackIdleTime}
                        class="sr-only" 
                      />
                      <div 
                        class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner"
                        class:bg-amber-500={settings.trackIdleTime}
                      >
                        <div 
                          class="dot absolute w-4 h-4 bg-white rounded-full shadow transition-all"
                          class:left-1={!settings.trackIdleTime}
                          class:left-5={settings.trackIdleTime}
                          style="top: 0.25rem;"
                        ></div>
                      </div>
                      <div class="ml-3 text-gray-700 font-medium">Track idle time</div>
                    </label>
                  </div>
                  
                  <div>
                    <label for="auto-start" class="flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        id="auto-start" 
                        bind:checked={settings.autoStartOnAppOpen}
                        class="sr-only" 
                      />
                      <div 
                        class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner"
                        class:bg-amber-500={settings.autoStartOnAppOpen}
                      >
                        <div 
                          class="dot absolute w-4 h-4 bg-white rounded-full shadow transition-all"
                          class:left-1={!settings.autoStartOnAppOpen}
                          class:left-5={settings.autoStartOnAppOpen}
                          style="top: 0.25rem;"
                        ></div>
                      </div>
                      <div class="ml-3 text-gray-700 font-medium">Auto-start timer when app opens</div>
                    </label>
                  </div>
                  
                  <div>
                    <label for="show-notifications" class="flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        id="show-notifications" 
                        bind:checked={settings.showNotifications}
                        class="sr-only" 
                      />
                      <div 
                        class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner"
                        class:bg-amber-500={settings.showNotifications}
                      >
                        <div 
                          class="dot absolute w-4 h-4 bg-white rounded-full shadow transition-all"
                          class:left-1={!settings.showNotifications}
                          class:left-5={settings.showNotifications}
                          style="top: 0.25rem;"
                        ></div>
                      </div>
                      <div class="ml-3 text-gray-700 font-medium">Show timer notifications</div>
                    </label>
                  </div>
                </div>
              </div>
              
              <!-- Pomodoro Settings -->
              <div>
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-semibold">Pomodoro Timer</h3>
                  <div>
                    <label for="pomodoro-enabled" class="flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        id="pomodoro-enabled" 
                        bind:checked={settings.pomodoroEnabled}
                        class="sr-only" 
                      />
                      <div 
                        class="relative w-10 h-6 bg-gray-200 rounded-full shadow-inner"
                        class:bg-amber-500={settings.pomodoroEnabled}
                      >
                        <div 
                          class="dot absolute w-4 h-4 bg-white rounded-full shadow transition-all"
                          class:left-1={!settings.pomodoroEnabled}
                          class:left-5={settings.pomodoroEnabled}
                          style="top: 0.25rem;"
                        ></div>
                      </div>
                    </label>
                  </div>
                </div>
                
                <div class="space-y-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label for="work-duration" class="block text-sm font-medium text-gray-700 mb-1">
                        Work Duration (minutes)
                      </label>
                      <input 
                        type="number" 
                        id="work-duration" 
                        bind:value={settings.pomodoroWorkDuration}
                        min="1" 
                        max="120"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                      />
                    </div>
                    
                    <div>
                      <label for="break-duration" class="block text-sm font-medium text-gray-700 mb-1">
                        Break Duration (minutes)
                      </label>
                      <input 
                        type="number" 
                        id="break-duration" 
                        bind:value={settings.pomodoroBreakDuration}
                        min="1" 
                        max="60"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/if}
      
      <!-- Integrations -->
      {#if activeTab === 'integrations'}
        <div class="p-6">
          <div class="max-w-3xl mx-auto">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-bold">External Integrations</h2>
              <button class="text-sm text-amber-600 hover:text-amber-700 font-medium">
                + Add New Integration
              </button>
            </div>
            
            <div class="space-y-6">
              {#each integrations as integration}
                <div class="border border-gray-200 rounded-lg p-4 flex flex-col md:flex-row justify-between items-start md:items-center">
                  <div class="flex items-center mb-4 md:mb-0">
                    <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center mr-4">
                      <!-- Placeholder for the icon -->
                      <span class="text-gray-500 font-medium text-lg">{integration.icon.charAt(0).toUpperCase()}</span>
                    </div>
                    
                    <div>
                      <h3 class="font-medium">{integration.name}</h3>
                      {#if integration.connected && integration.lastSynced}
                        <p class="text-sm text-gray-500">Last synced: {formatDate(integration.lastSynced)}</p>
                      {:else}
                        <p class="text-sm text-gray-500">Not connected</p>
                      {/if}
                    </div>
                  </div>
                  
                  <button 
                    on:click={() => toggleIntegration(integration.id)}
                    class={`px-4 py-2 text-sm font-medium rounded-full ${
                      integration.connected 
                        ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' 
                        : 'bg-amber-600 text-white hover:bg-amber-700'
                    }`}
                  >
                    {integration.connected ? 'Disconnect' : 'Connect'}
                  </button>
                </div>
              {/each}
            </div>
          </div>
        </div>
      {/if}
      
      <!-- Data Management -->
      {#if activeTab === 'data'}
        <div class="p-6">
          <div class="max-w-3xl mx-auto">
            <h2 class="text-xl font-bold mb-6">Data Management</h2>
            
            <div class="space-y-8">
              <!-- Export/Import -->
              <div>
                <h3 class="text-lg font-semibold mb-4">Export/Import</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="bg-amber-50 p-6 rounded-lg">
                    <h4 class="font-medium mb-2">Export Your Data</h4>
                    <p class="text-sm text-gray-600 mb-4">
                      Download all your time tracking data in a CSV or JSON format.
                    </p>
                    <div class="flex space-x-3">
                      <button 
                        on:click={exportData}
                        class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        Export as CSV
                      </button>
                      <button 
                        on:click={exportData}
                        class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        Export as JSON
                      </button>
                    </div>
                  </div>
                  
                  <div class="bg-amber-50 p-6 rounded-lg">
                    <h4 class="font-medium mb-2">Import Data</h4>
                    <p class="text-sm text-gray-600 mb-4">
                      Import time tracking data from a CSV or JSON file.
                    </p>
                    <button 
                      on:click={importData}
                      class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                    >
                      Import Data
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Data Retention -->
              <div>
                <h3 class="text-lg font-semibold mb-4">Data Retention</h3>
                
                <div>
                  <label for="data-retention" class="block text-sm font-medium text-gray-700 mb-1">
                    Keep data for
                  </label>
                  <select 
                    id="data-retention"
                    class="w-full md:w-64 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  >
                    <option value="forever">Forever</option>
                    <option value="1year">1 year</option>
                    <option value="6months">6 months</option>
                    <option value="3months">3 months</option>
                  </select>
                  <p class="mt-2 text-sm text-gray-500">
                    Time entries older than this will be automatically archived.
                  </p>
                </div>
              </div>
              
              <!-- Account Actions -->
              <div>
                <h3 class="text-lg font-semibold mb-4">Account Actions</h3>
                
                <div class="space-y-4">
                  <button class="text-amber-600 hover:text-amber-700 font-medium">
                    Archive All Data
                  </button>
                  
                  <button class="text-red-600 hover:text-red-700 font-medium">
                    Delete Account
                  </button>
                  
                  <p class="text-sm text-gray-500 mt-2">
                    Warning: Deleting your account will permanently remove all your data.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/if}
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
  
  /* Toggle switch styling */
  input:checked ~ .dot {
    transform: translateX(100%);
  }
  
  input:checked ~ div {
    background-color: #F59E0B;
  }
</style>