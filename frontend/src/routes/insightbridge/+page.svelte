<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  
  // Register ChartJS components
  Chart.register(...registerables);
  
  // Mock student data (would come from API in real application)
  let student = {
    name: "Aditya Raj",
    grade: "4th Semester",
    school: "MS Ramiah Institute of Technology",
    avatar: "https://i.pravatar.cc/150?img=11"
  };
  
  // Performance metrics
  let performanceMetrics = {
    currentMonth: 87,
    previousMonth: 82,
    streak: 34,
    ranking: "Top 15%"
  };
  
  // Timeline data for progress chart
  let timelineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Overall Performance',
        data: [65, 68, 72, 75, 82, 87],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        fill: false
      },
      {
        label: 'Coding Skills',
        data: [60, 65, 70, 78, 80, 85],
        borderColor: 'rgb(153, 102, 255)',
        tension: 0.1,
        fill: false
      }
    ]
  };
  
  // Radar chart data for skills
  let skillsData = {
    labels: ['Algorithms', 'Data Structures', 'Problem-solving', 'Debugging', 'System Design', 'Collaboration'],
    datasets: [{
      label: 'Current Skills',
      data: [85, 80, 70, 90, 65, 75],
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgb(54, 162, 235)',
      pointBackgroundColor: 'rgb(54, 162, 235)',
      pointBorderColor: '#fff',
    }]
  };
  
  // Course progress data
  let courseProgress = {
    labels: ['Harvard CS50x', 'JavaScript Mastery', 'Python Data Science', 'React Frontend'],
    datasets: [{
      label: 'Completion %',
      data: [92, 78, 45, 65],
      backgroundColor: [
        'rgba(75, 192, 192, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(255, 205, 86, 0.6)',
        'rgba(54, 162, 235, 0.6)'
      ],
      borderColor: [
        'rgb(75, 192, 192)',
        'rgb(255, 159, 64)',
        'rgb(255, 205, 86)',
        'rgb(54, 162, 235)'
      ],
      borderWidth: 1
    }]
  };
  
  // Habit tracking data
  let habitData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
      label: 'Study Hours',
      data: [3, 4, 2, 5, 3, 6, 4],
      backgroundColor: 'rgba(153, 102, 255, 0.6)',
      borderColor: 'rgb(153, 102, 255)'
    }]
  };
  
  // Reference variables for the canvas elements
  let lineChartCanvas;
  let radarChartCanvas;
  let barChartCanvas;
  let doughnutChartCanvas;
  
  // Chart instances
  let lineChart;
  let radarChart;
  let barChart;
  let doughnutChart;
  
  // Insight cards
  let insightCards = [
    {
      icon: "🔥",
      title: "Coding Consistency Rising",
      content: "Solved 34 LeetCode problems this month (up 27%). Strength in DP and Graphs."
    },
    {
      icon: "⚡",
      title: "Peak Focus Hours",
      content: "Most productive between 8 PM–10 PM based on HabitForge logs."
    },
    {
      icon: "💬",
      title: "Coach Feedback",
      content: "Improved resilience in problem-solving noted by mentor in 3 out of 4 sessions."
    },
    {
      icon: "🚀",
      title: "Course Progress",
      content: "Completed \"Harvard CS50x\" with 92% quiz accuracy; rated it 4.8/5."
    }
  ];
  
  // Platform integration data
  let platformData = {
    leetcode: { problems: 187, ranking: "Top 15%", streaks: 34 },
    github: { repos: 27, contributions: 842, stars: 56 },
    codeforces: { rating: 1756, contests: 24, problemsSolved: 312 },
    hackerrank: { badges: 15, stars: 4, certifications: 3 }
  };
  
  // Time range for filtering data
  let timeRange = 3; // Default: 3 months
  
  // Toggle visibility of different sections
  let visibleSections = {
    overview: true,
    coding: true,
    habits: true,
    courses: true,
    coaching: true
  };
  
  // Handle time range change
  function updateTimeRange(event) {
    timeRange = event.target.value;
    // In a real app, this would trigger API calls to refresh data
  }
  
  // Toggle section visibility
  function toggleSection(section) {
    visibleSections[section] = !visibleSections[section];
  }
  
  // Initialize charts when DOM is available
  function initCharts() {
    // Line chart for performance timeline
    if (lineChartCanvas) {
      lineChart = new Chart(lineChartCanvas, {
        type: 'line',
        data: timelineData,
        options: { 
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
    
    // Radar chart for skills
    if (radarChartCanvas) {
      radarChart = new Chart(radarChartCanvas, {
        type: 'radar',
        data: skillsData,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
    
    // Bar chart for habits
    if (barChartCanvas) {
      barChart = new Chart(barChartCanvas, {
        type: 'bar',
        data: habitData,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
    
    // Doughnut chart for course progress
    if (doughnutChartCanvas) {
      doughnutChart = new Chart(doughnutChartCanvas, {
        type: 'doughnut',
        data: courseProgress,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
  }
  
  // Clean up charts when component is destroyed
  function destroyCharts() {
    if (lineChart) lineChart.destroy();
    if (radarChart) radarChart.destroy();
    if (barChart) barChart.destroy();
    if (doughnutChart) doughnutChart.destroy();
  }
  
  onMount(() => {
    // Initialize charts
    initCharts();
    
    // Here we would fetch real data from APIs
    console.log("Dashboard mounted, fetching data...");
    
    // Clean up on component unmount
    return destroyCharts;
  });
</script>

<main class="container mx-auto px-4 py-8">
  <header class="mb-8">
    <div class="flex flex-col md:flex-row justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-primary mb-4 md:mb-0">InsightsBridge</h1>
      
      <div class="flex items-center space-x-4">
        <div class="text-right">
          <div class="flex items-center">
            <div>
              <div class="text-lg font-semibold">{student.name}</div>
              <div class="text-sm text-gray-600">{student.grade} · {student.school}</div>
            </div>
            <img src={student.avatar} alt={student.name} class="ml-4 h-12 w-12 rounded-full border-2 border-primary"/>
          </div>
        </div>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <h2 class="text-xl font-semibold">Performance Overview</h2>
          <div class="text-sm text-gray-500">Filter by time range</div>
        </div>
        
        <div class="w-full md:w-1/2">
          <input 
            type="range" 
            min="1" 
            max="12" 
            value={timeRange}
            on:input={updateTimeRange}
            class="range w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 px-2 mt-1">
            <span>1 month</span>
            <span>3 months</span>
            <span>6 months</span>
            <span>12 months</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
        <div class="text-sm text-gray-600">Performance Score</div>
        <div class="text-3xl font-bold text-primary">{performanceMetrics.currentMonth}%</div>
        <div class="text-sm text-green-600">↑ {performanceMetrics.currentMonth - performanceMetrics.previousMonth}% from last month</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
        <div class="text-sm text-gray-600">Consistency Streak</div>
        <div class="text-3xl font-bold text-indigo-600">{performanceMetrics.streak} days</div>
        <div class="text-sm text-gray-600">Personal best: 42 days</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
        <div class="text-sm text-gray-600">Peer Ranking</div>
        <div class="text-3xl font-bold text-blue-600">{performanceMetrics.ranking}</div>
        <div class="text-sm text-green-600">↑ 5% from last quarter</div>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
        <div class="text-sm text-gray-600">Growth Index</div>
        <div class="text-3xl font-bold text-teal-600">4.2/5</div>
        <div class="text-sm text-gray-600">Steady improvement</div>
      </div>
    </div>
  </header>
  
  <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
    <!-- First column: Timeline chart -->
    <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-4">
      <h2 class="text-xl font-semibold mb-4">Growth Timeline</h2>
      <div class="h-80">
        <canvas bind:this={lineChartCanvas}></canvas>
      </div>
    </div>
    
    <!-- Second column: Insight cards -->
    <div class="lg:col-span-1 space-y-4">
      {#each insightCards as card}
        <div class="bg-white rounded-lg shadow-md p-4 border-l-4 border-primary hover:shadow-lg transition-shadow">
          <div class="flex items-start">
            <div class="text-2xl mr-3">{card.icon}</div>
            <div>
              <h3 class="font-semibold">{card.title}</h3>
              <p class="text-sm text-gray-600">{card.content}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </section>
  
  <section class="mb-8" class:hidden={!visibleSections.coding}>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Coding Skills Analysis</h2>
      <button on:click={() => toggleSection('coding')} class="text-sm text-gray-500">
        {visibleSections.coding ? 'Hide' : 'Show'}
      </button>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Radar chart for skills -->
      <div class="bg-white rounded-lg shadow-md p-4">
        <h3 class="text-lg font-semibold mb-2">Skills Breakdown</h3>
        <div class="h-80">
          <canvas bind:this={radarChartCanvas}></canvas>
        </div>
      </div>
      
      <!-- Coding platforms stats -->
      <div class="bg-white rounded-lg shadow-md p-4">
        <h3 class="text-lg font-semibold mb-4">Coding Platform Activity</h3>
        
        <div class="space-y-4">
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="flex justify-between items-center mb-1">
              <span class="font-medium">LeetCode</span>
              <span class="text-sm font-semibold">{platformData.leetcode.problems} problems</span>
            </div>
            <div class="text-sm text-gray-600">Ranking: {platformData.leetcode.ranking}, Current Streak: {platformData.leetcode.streaks} days</div>
          </div>
          
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="flex justify-between items-center mb-1">
              <span class="font-medium">GitHub</span>
              <span class="text-sm font-semibold">{platformData.github.repos} repositories</span>
            </div>
            <div class="text-sm text-gray-600">{platformData.github.contributions} contributions, {platformData.github.stars} stars received</div>
          </div>
          
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="flex justify-between items-center mb-1">
              <span class="font-medium">Codeforces</span>
              <span class="text-sm font-semibold">Rating: {platformData.codeforces.rating}</span>
            </div>
            <div class="text-sm text-gray-600">{platformData.codeforces.contests} contests, {platformData.codeforces.problemsSolved} problems solved</div>
          </div>
          
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="flex justify-between items-center mb-1">
              <span class="font-medium">HackerRank</span>
              <span class="text-sm font-semibold">{platformData.hackerrank.badges} badges</span>
            </div>
            <div class="text-sm text-gray-600">{platformData.hackerrank.stars}★ rating, {platformData.hackerrank.certifications} certifications</div>
          </div>
        </div>
      </div>
    </div>
  </section>
  
  <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
    <!-- Habit tracking section -->
    <div class:hidden={!visibleSections.habits}>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Habit Tracking</h2>
        <button on:click={() => toggleSection('habits')} class="text-sm text-gray-500">
          {visibleSections.habits ? 'Hide' : 'Show'}
        </button>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-4">
        <h3 class="text-lg font-semibold mb-2">Weekly Study Pattern</h3>
        <div class="h-64">
          <canvas bind:this={barChartCanvas}></canvas>
        </div>
        
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="text-sm font-medium">Focus Quality</div>
            <div class="flex items-center">
              <div class="h-2 flex-grow rounded-full bg-gray-200">
                <div class="h-2 rounded-full bg-green-500" style="width: 78%"></div>
              </div>
              <span class="ml-2 text-sm font-semibold">78%</span>
            </div>
          </div>
          
          <div class="p-3 bg-gray-50 rounded-md">
            <div class="text-sm font-medium">Work-Break Balance</div>
            <div class="flex items-center">
              <div class="h-2 flex-grow rounded-full bg-gray-200">
                <div class="h-2 rounded-full bg-blue-500" style="width: 65%"></div>
              </div>
              <span class="ml-2 text-sm font-semibold">65%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Course progress section -->
    <div class:hidden={!visibleSections.courses}>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Course Progress</h2>
        <button on:click={() => toggleSection('courses')} class="text-sm text-gray-500">
          {visibleSections.courses ? 'Hide' : 'Show'}
        </button>
      </div>
      
      <div class="bg-white rounded-lg shadow-md p-4">
        <h3 class="text-lg font-semibold mb-2">Course Completion</h3>
        <div class="h-64">
          <canvas bind:this={doughnutChartCanvas}></canvas>
        </div>
        
        <div class="mt-4">
          <div class="text-sm font-medium mb-2">Recommended Next Courses</div>
          <div class="space-y-2">
            <div class="p-2 bg-blue-50 rounded-md text-sm border-l-4 border-blue-400">Advanced Data Structures</div>
            <div class="p-2 bg-green-50 rounded-md text-sm border-l-4 border-green-400">System Design Fundamentals</div>
          </div>
        </div>
      </div>
    </div>
  </section>
  
  <section class="mb-8" class:hidden={!visibleSections.coaching}>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Coach Assessment</h2>
      <button on:click={() => toggleSection('coaching')} class="text-sm text-gray-500">
        {visibleSections.coaching ? 'Hide' : 'Show'}
      </button>
    </div>
    
    <div class="bg-white rounded-lg shadow-md p-6">
      <div class="mb-6">
        <h3 class="text-lg font-semibold mb-3">Summary</h3>
        <p class="text-gray-700">Aditya continues to show strong progress in algorithmic problem solving and has demonstrated improved resilience when tackling complex challenges. Time management and study consistency have improved significantly over the past quarter, though there's room to develop better system design skills and collaborative coding practices.</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class="p-3 bg-gray-50 rounded-md">
          <div class="text-sm font-medium">Coachability</div>
          <div class="flex items-center mt-1">
            <div class="h-2 flex-grow rounded-full bg-gray-200">
              <div class="h-2 rounded-full bg-purple-500" style="width: 92%"></div>
            </div>
            <span class="ml-2 text-sm font-semibold">92%</span>
          </div>
        </div>
        
        <div class="p-3 bg-gray-50 rounded-md">
          <div class="text-sm font-medium">Problem-solving Approach</div>
          <div class="flex items-center mt-1">
            <div class="h-2 flex-grow rounded-full bg-gray-200">
              <div class="h-2 rounded-full bg-indigo-500" style="width: 88%"></div>
            </div>
            <span class="ml-2 text-sm font-semibold">88%</span>
          </div>
        </div>
        
        <div class="p-3 bg-gray-50 rounded-md">
          <div class="text-sm font-medium">Growth Mindset</div>
          <div class="flex items-center mt-1">
            <div class="h-2 flex-grow rounded-full bg-gray-200">
              <div class="h-2 rounded-full bg-teal-500" style="width: 95%"></div>
            </div>
            <span class="ml-2 text-sm font-semibold">95%</span>
          </div>
        </div>
      </div>
      
      <div class="mt-6">
        <h3 class="text-lg font-semibold mb-3">Recent Feedback</h3>
        <div class="space-y-3">
          <div class="p-4 bg-yellow-50 rounded-md border-l-4 border-yellow-400">
            <div class="text-sm font-medium mb-1">June 15: Algorithm Deep Dive Session</div>
            <p class="text-sm text-gray-700">Shows excellent progress in dynamic programming. Solved all challenge problems independently. Next focus area: graph algorithms and network flow problems.</p>
          </div>
          
          <div class="p-4 bg-blue-50 rounded-md border-l-4 border-blue-400">
            <div class="text-sm font-medium mb-1">May 30: Project Review</div>
            <p class="text-sm text-gray-700">GitHub project structure has improved significantly. Code is better documented and follows best practices. Consider adding more comprehensive unit tests in future projects.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
  
  <footer class="text-center text-gray-500 text-sm mt-12">
    <p>InsightsBridge by Cogito — Data last updated: Today, 2:30 PM</p>
  </footer>
</main>

<style>
  :global(body) {
    background-color: #f7f9fc;
  }
  
  .text-primary {
    color: #4f46e5;
  }
  
  .border-primary {
    border-color: #4f46e5;
  }
  
  /* Custom slider styling */
  input[type="range"] {
    -webkit-appearance: none;
    height: 7px;
    border-radius: 5px;
    background: #d3d3d3;
    outline: none;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #4f46e5;
    cursor: pointer;
  }
</style>
