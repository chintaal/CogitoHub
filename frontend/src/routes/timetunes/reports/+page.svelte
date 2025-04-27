<script lang="ts">
  import { onMount } from 'svelte';
  import TimetunesLogo from '../../../components/logos/timetunesLogo.svelte';
  
  // Mock data for reports
  // In a real app, this would come from an API/database
  let projects = [
    { id: 'proj1', name: 'Personal', color: '#FF5733' },
    { id: 'proj2', name: 'Work', color: '#33A8FF' },
    { id: 'proj3', name: 'Learning', color: '#A233FF' },
    { id: 'proj4', name: 'Side Project', color: '#33FF57' }
  ];
  
  // Sample time entries data spanning several days
  let timeEntries = [
    // Today
    { id: 'e1', projectId: 'proj2', duration: 7200000, date: new Date() }, // 2 hours
    { id: 'e2', projectId: 'proj3', duration: 3600000, date: new Date() }, // 1 hour
    
    // Yesterday
    { id: 'e3', projectId: 'proj1', duration: 5400000, date: new Date(Date.now() - 86400000) }, // 1.5 hours
    { id: 'e4', projectId: 'proj4', duration: 10800000, date: new Date(Date.now() - 86400000) }, // 3 hours
    
    // 2 days ago
    { id: 'e5', projectId: 'proj2', duration: 9000000, date: new Date(Date.now() - 86400000 * 2) }, // 2.5 hours
    { id: 'e6', projectId: 'proj3', duration: 1800000, date: new Date(Date.now() - 86400000 * 2) }, // 0.5 hours
    
    // 3 days ago
    { id: 'e7', projectId: 'proj1', duration: 3600000, date: new Date(Date.now() - 86400000 * 3) }, // 1 hour
    { id: 'e8', projectId: 'proj4', duration: 7200000, date: new Date(Date.now() - 86400000 * 3) }, // 2 hours
    
    // 4 days ago
    { id: 'e9', projectId: 'proj2', duration: 5400000, date: new Date(Date.now() - 86400000 * 4) }, // 1.5 hours
    { id: 'e10', projectId: 'proj3', duration: 3600000, date: new Date(Date.now() - 86400000 * 4) }, // 1 hour
    
    // 5 days ago
    { id: 'e11', projectId: 'proj1', duration: 7200000, date: new Date(Date.now() - 86400000 * 5) }, // 2 hours
    { id: 'e12', projectId: 'proj4', duration: 1800000, date: new Date(Date.now() - 86400000 * 5) }, // 0.5 hours
    
    // 6 days ago
    { id: 'e13', projectId: 'proj2', duration: 10800000, date: new Date(Date.now() - 86400000 * 6) }, // 3 hours
    { id: 'e14', projectId: 'proj3', duration: 5400000, date: new Date(Date.now() - 86400000 * 6) }, // 1.5 hours
  ];
  
  // For filtering
  let selectedDateRange = 'week';
  let selectedProjects = projects.map(p => p.id);
  let startDate = new Date();
  let endDate = new Date();
  
  // Set date range based on selection
  $: {
    const now = new Date();
    
    if (selectedDateRange === 'today') {
      startDate = new Date(now.setHours(0, 0, 0, 0));
      endDate = new Date(now.setHours(23, 59, 59, 999));
    } else if (selectedDateRange === 'yesterday') {
      startDate = new Date(now.setDate(now.getDate() - 1));
      startDate.setHours(0, 0, 0, 0);
      endDate = new Date(now);
      endDate.setHours(23, 59, 59, 999);
    } else if (selectedDateRange === 'week') {
      // Start from Sunday of this week
      startDate = new Date(now);
      startDate.setDate(now.getDate() - now.getDay());
      startDate.setHours(0, 0, 0, 0);
      
      endDate = new Date(now);
      endDate.setDate(startDate.getDate() + 6);
      endDate.setHours(23, 59, 59, 999);
    } else if (selectedDateRange === 'month') {
      startDate = new Date(now.getFullYear(), now.getMonth(), 1);
      endDate = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999);
    }
  }
  
  // Filter entries based on selected date range and projects
  $: filteredEntries = timeEntries.filter(entry => {
    const entryDate = new Date(entry.date);
    const isInDateRange = entryDate >= startDate && entryDate <= endDate;
    const isSelectedProject = selectedProjects.includes(entry.projectId);
    return isInDateRange && isSelectedProject;
  });
  
  // Calculate total tracked time
  $: totalTrackedTime = filteredEntries.reduce((sum, entry) => sum + entry.duration, 0);
  
  // Calculate time per project
  $: timePerProject = projects.reduce((acc, project) => {
    const projectEntries = filteredEntries.filter(entry => entry.projectId === project.id);
    const projectTime = projectEntries.reduce((sum, entry) => sum + entry.duration, 0);
    acc[project.id] = {
      time: projectTime,
      percentage: totalTrackedTime > 0 ? (projectTime / totalTrackedTime * 100).toFixed(1) : '0'
    };
    return acc;
  }, {});
  
  // Data for bar chart (time by day)
  $: timeByDay = Array(7).fill(0).map((_, index) => {
    const day = new Date(startDate);
    day.setDate(startDate.getDate() + index);
    day.setHours(0, 0, 0, 0);
    
    const nextDay = new Date(day);
    nextDay.setDate(day.getDate() + 1);
    
    const dayEntries = filteredEntries.filter(entry => {
      const entryDate = new Date(entry.date);
      return entryDate >= day && entryDate < nextDay;
    });
    
    const timeByProject = projects.reduce((acc, project) => {
      const projectTime = dayEntries
        .filter(entry => entry.projectId === project.id)
        .reduce((sum, entry) => sum + entry.duration, 0);
      
      acc[project.id] = projectTime;
      return acc;
    }, {});
    
    return {
      date: day,
      dayName: day.toLocaleDateString('en-US', { weekday: 'short' }),
      total: dayEntries.reduce((sum, entry) => sum + entry.duration, 0),
      byProject: timeByProject
    };
  });
  
  // Format time as HH:MM
  function formatTime(ms: number) {
    const hours = Math.floor(ms / 1000 / 60 / 60);
    const minutes = Math.floor((ms / 1000 / 60) % 60);
    
    return `${hours}h ${minutes}m`;
  }
  
  // Format date for display
  function formatDate(date: Date) {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric'
    });
  }
  
  // Reactive chart canvas references
  let barChartCanvas: HTMLCanvasElement;
  let pieChartCanvas: HTMLCanvasElement;
  let barChart: any;
  let pieChart: any;
  let Chart: any;
  
  // Initialize charts on mount
  onMount(async () => {
    // Dynamically import Chart.js
    const chartModule = await import('chart.js/auto');
    Chart = chartModule.default;
    
    // Initialize charts after component is mounted
    createBarChart();
    createPieChart();
    
    // Cleanup on destroy
    return () => {
      if (barChart) barChart.destroy();
      if (pieChart) pieChart.destroy();
    };
  });
  
  // Recreate charts when data changes
  $: if (Chart && filteredEntries.length >= 0) {
    if (barChart) barChart.destroy();
    if (pieChart) pieChart.destroy();
    
    setTimeout(() => {
      createBarChart();
      createPieChart();
    }, 0);
  }
  
  // Create bar chart (time by day)
  function createBarChart() {
    if (!barChartCanvas) return;
    
    // Prepare datasets for each project
    const datasets = projects.map(project => {
      return {
        label: project.name,
        data: timeByDay.map(day => day.byProject[project.id] / 3600000), // Convert to hours
        backgroundColor: project.color,
        borderColor: project.color,
        borderWidth: 1
      };
    });
    
    barChart = new Chart(barChartCanvas, {
      type: 'bar',
      data: {
        labels: timeByDay.map(day => day.dayName),
        datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Hours Tracked per Day'
          },
          legend: {
            position: 'bottom'
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.raw.toFixed(1)} hours`
            }
          }
        },
        scales: {
          x: {
            stacked: true
          },
          y: {
            stacked: true,
            ticks: {
              callback: (value) => `${value}h`
            }
          }
        }
      }
    });
  }
  
  // Create pie chart (time per project)
  function createPieChart() {
    if (!pieChartCanvas) return;
    
    const data = projects
      .filter(project => selectedProjects.includes(project.id))
      .map(project => {
        return {
          label: project.name,
          data: timePerProject[project.id].time / 3600000, // Convert to hours
          color: project.color
        };
      })
      .filter(item => item.data > 0);
    
    pieChart = new Chart(pieChartCanvas, {
      type: 'doughnut',
      data: {
        labels: data.map(item => item.label),
        datasets: [{
          data: data.map(item => item.data),
          backgroundColor: data.map(item => item.color),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Time Distribution by Project'
          },
          legend: {
            position: 'bottom'
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.raw || 0;
                const percentage = context.parsed || 0;
                return `${label}: ${value.toFixed(1)} hours (${percentage.toFixed(1)}%)`;
              }
            }
          }
        }
      }
    });
  }
  
  // Toggle project selection
  function toggleProject(projectId: string) {
    if (selectedProjects.includes(projectId)) {
      if (selectedProjects.length > 1) {
        selectedProjects = selectedProjects.filter(id => id !== projectId);
      }
    } else {
      selectedProjects = [...selectedProjects, projectId];
    }
  }
  
  // Export report
  function exportReport() {
    // In a real app, this would generate a PDF or CSV
    alert('Report exported! (In a real app, this would download a PDF or CSV file)');
  }
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
        <a href="/timetunes/reports" class="text-amber-200 font-medium transition-colors border-b-2 border-amber-200 pb-1">Reports</a>
        <a href="/timetunes/projects" class="hover:text-amber-200 transition-colors">Projects</a>
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-6">
    <!-- Report Controls -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Reports</h1>
        
        <div class="flex flex-wrap gap-3">
          <!-- Date range selector -->
          <select 
            bind:value={selectedDateRange}
            class="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-amber-500 focus:border-transparent"
          >
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          
          <button 
            on:click={exportReport}
            class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            Export
          </button>
        </div>
      </div>
      
      <!-- Selected date range display -->
      <div class="bg-amber-50 rounded-lg p-4 mb-6">
        <div class="flex justify-between items-center">
          <div>
            <span class="text-sm text-gray-500">Date range:</span>
            <span class="ml-2 font-medium">{formatDate(startDate)} - {formatDate(endDate)}</span>
          </div>
          <div class="text-right">
            <span class="text-sm text-gray-500">Total tracked time:</span>
            <span class="ml-2 font-medium text-amber-700">{formatTime(totalTrackedTime)}</span>
          </div>
        </div>
      </div>
      
      <!-- Project filter -->
      <div class="mb-4">
        <h3 class="text-sm font-medium text-gray-500 mb-3">Filter by project:</h3>
        <div class="flex flex-wrap gap-2">
          {#each projects as project}
            <button 
              class={`py-2 px-3 text-sm rounded-full flex items-center transition-colors ${selectedProjects.includes(project.id) ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-700'}`}
              on:click={() => toggleProject(project.id)}
            >
              <span class="inline-block w-3 h-3 rounded-full mr-2" style={`background-color: ${project.color}`}></span>
              {project.name}
            </button>
          {/each}
        </div>
      </div>
    </section>
    
    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Bar Chart - Time tracked per day -->
      <section class="bg-white rounded-2xl p-6 shadow-lg">
        <h2 class="text-xl font-bold mb-4">Time per Day</h2>
        <div class="h-64">
          <canvas bind:this={barChartCanvas}></canvas>
        </div>
      </section>
      
      <!-- Pie Chart - Time per project -->
      <section class="bg-white rounded-2xl p-6 shadow-lg">
        <h2 class="text-xl font-bold mb-4">Project Distribution</h2>
        <div class="h-64">
          <canvas bind:this={pieChartCanvas}></canvas>
        </div>
      </section>
    </div>
    
    <!-- Detailed Report Table -->
    <section class="bg-white rounded-2xl p-6 shadow-lg">
      <h2 class="text-xl font-bold mb-6">Detailed Report</h2>
      
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Project</th>
              <th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Time</th>
              <th class="py-3 px-4 text-left text-sm font-medium text-gray-500">Percentage</th>
            </tr>
          </thead>
          <tbody>
            {#each projects.filter(p => selectedProjects.includes(p.id)) as project}
              <tr class="border-b border-gray-200">
                <td class="py-4 px-4">
                  <div class="flex items-center">
                    <span class="w-3 h-3 rounded-full mr-2" style={`background-color: ${project.color}`}></span>
                    <span class="font-medium">{project.name}</span>
                  </div>
                </td>
                <td class="py-4 px-4">{formatTime(timePerProject[project.id].time)}</td>
                <td class="py-4 px-4">{timePerProject[project.id].percentage}%</td>
              </tr>
            {/each}
          </tbody>
          <tfoot>
            <tr class="bg-gray-50">
              <td class="py-4 px-4 font-bold">Total</td>
              <td class="py-4 px-4 font-bold">{formatTime(totalTrackedTime)}</td>
              <td class="py-4 px-4 font-bold">100%</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </section>
    
    <!-- Daily Breakdown -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mt-8">
      <h2 class="text-xl font-bold mb-6">Daily Breakdown</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {#each timeByDay as day}
          <div class="border border-gray-200 rounded-lg p-4">
            <h3 class="text-lg font-medium mb-2">{day.dayName} ({formatDate(day.date)})</h3>
            
            {#if day.total > 0}
              <div class="space-y-3">
                {#each projects.filter(p => selectedProjects.includes(p.id) && day.byProject[p.id] > 0) as project}
                  <div>
                    <div class="flex items-center justify-between text-sm mb-1">
                      <div class="flex items-center">
                        <span class="w-3 h-3 rounded-full mr-2" style={`background-color: ${project.color}`}></span>
                        <span>{project.name}</span>
                      </div>
                      <span>{formatTime(day.byProject[project.id])}</span>
                    </div>
                    <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        class="h-full rounded-full" 
                        style={`background-color: ${project.color}; width: ${day.byProject[project.id] / day.total * 100}%`}>
                      </div>
                    </div>
                  </div>
                {/each}
                
                <div class="text-right text-sm font-medium mt-2">
                  Total: {formatTime(day.total)}
                </div>
              </div>
            {:else}
              <div class="text-gray-500 text-center py-6">
                <p>No time tracked</p>
              </div>
            {/if}
          </div>
        {/each}
      </div>
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
</style>