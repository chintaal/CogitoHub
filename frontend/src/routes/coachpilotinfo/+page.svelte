<script>
  import { assets } from '$app/paths';
  import CoachpilotLogo from '../../components/logos/coachpilotLogo.svelte';
  import CoachpilotIcon from '../../components/icons/coachpilotIcon.svelte';
</script>

<main class="min-h-screen bg-gradient-to-b from-blue-50 to-white text-gray-900">
  <!-- Hero Section -->
  <section class="container mx-auto py-20 md:py-32 px-4 flex flex-col items-center relative">
    <!-- Background elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
      <div class="absolute top-20 left-10 w-64 h-64 rounded-full bg-blue-200 filter blur-3xl opacity-30 animate-pulse"></div>
      <div class="absolute bottom-20 right-10 w-72 h-72 rounded-full bg-blue-100 filter blur-3xl opacity-30 animate-pulse"></div>
    </div>
    
    <!-- Logo and headline -->
    <div class="relative z-10 mb-12 flex flex-col items-center">
      <div class="mb-8 transform hover:scale-105 transition-all duration-700 ease-out">
        <div class="w-[300px] h-[300px] relative flex items-center justify-center">
          <CoachpilotLogo size={800} showText={false} />
        </div>
      </div>
      
      <h1 class="text-5xl md:text-6xl font-bold text-center max-w-4xl mb-6 text-gray-800">
        Your Personal AI Coach
      </h1>
      
      <p class="text-xl text-gray-600 text-center max-w-3xl mb-12">
        Empower your productivity with intelligent, AI-driven guidance that transforms how you manage tasks, set goals, and maximize your potential.
      </p>
      
      <a href="/coachpilot" class="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Try CoachPilot Today
      </a>
    </div>
  </section>
  
  <!-- Features Section -->
  <section class="container mx-auto py-16 px-4 relative">
    <div class="text-center mb-20">
      <h2 class="text-3xl md:text-4xl font-bold mb-6">Why Choose CoachPilot?</h2>
      <div class="h-1 w-20 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-6 rounded-full"></div>
    </div>
    
    <div class="grid md:grid-cols-3 gap-10">
      <!-- Feature 1 -->
      <div class="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
        <div class="rounded-full bg-blue-100 w-16 h-16 flex items-center justify-center mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold mb-3 text-gray-900">Agentic AI Technology</h3>
        <p class="text-gray-600">Advanced AI models that understand your unique challenges and provide personalized coaching tailored to your specific needs.</p>
      </div>
      
      <!-- Feature 2 -->
      <div class="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
        <div class="rounded-full bg-blue-100 w-16 h-16 flex items-center justify-center mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        </div>
        <h3 class="text-xl font-bold mb-3 text-gray-900">Comprehensive Task Management</h3>
        <p class="text-gray-600">From task lists and Kanban boards to mind maps and timelines, CoachPilot provides all the tools you need in one place.</p>
      </div>
      
      <!-- Feature 3 -->
      <div class="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
        <div class="rounded-full bg-blue-100 w-16 h-16 flex items-center justify-center mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold mb-3 text-gray-900">SMART Goal Setting</h3>
        <p class="text-gray-600">Turn your ambitions into achievable goals with our SMART framework that ensures you're always making measurable progress.</p>
      </div>
    </div>
  </section>
  
  <!-- Comparison Section -->
  <section class="py-20 bg-gradient-to-r from-blue-50 to-blue-100 relative">
    <div class="container mx-auto px-4 relative z-10">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold mb-6 text-gray-900">How We Compare</h2>
        <div class="h-1 w-20 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          See how CoachPilot stands out from traditional task management tools
        </p>
      </div>
      
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full">
            <thead>
              <tr class="bg-blue-50">
                <th class="py-4 px-6 text-left text-lg font-semibold text-gray-900 border-b">Features</th>
                <th class="py-4 px-6 text-center text-lg font-semibold text-blue-600 border-b">CoachPilot</th>
                <th class="py-4 px-6 text-center text-lg font-semibold text-gray-600 border-b">Traditional Tools</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="py-3 px-6 border-b text-gray-800 font-medium">AI-Powered Coaching</td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
              </tr>
              <tr>
                <td class="py-3 px-6 border-b text-gray-800 font-medium">Mind Maps & Timelines</td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 text-gray-400">
                    <span class="text-xs">Limited</span>
                  </span>
                </td>
              </tr>
              <tr>
                <td class="py-3 px-6 border-b text-gray-800 font-medium">SMART Goal Integration</td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
              </tr>
              <tr>
                <td class="py-3 px-6 border-b text-gray-800 font-medium">Personalized Insights</td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
                <td class="py-3 px-6 border-b text-center">
                  <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Call to Action Section -->
  <section class="py-20 bg-gradient-to-r from-blue-500 to-blue-600 text-white relative overflow-hidden">
    <div class="absolute top-0 right-0 w-72 h-72 rounded-full bg-blue-400 filter blur-3xl opacity-30"></div>
    <div class="absolute bottom-0 left-0 w-80 h-80 rounded-full bg-blue-700 filter blur-3xl opacity-30"></div>
    
    <div class="container mx-auto px-4 relative z-10 text-center">
      <h2 class="text-4xl font-bold mb-6">Ready to Boost Your Productivity?</h2>
      <p class="text-xl max-w-3xl mx-auto mb-10">Experience the power of AI-driven coaching and comprehensive task management with CoachPilot.</p>
      
      <div class="flex flex-wrap justify-center gap-4">
        <a href="/coachpilot" class="px-8 py-4 bg-white text-blue-600 hover:bg-blue-50 rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
          Try CoachPilot Free
        </a>
        <a href="#" class="px-8 py-4 border-2 border-white text-white hover:bg-blue-600 rounded-full font-medium transition-all transform hover:-translate-y-1">
          Watch Demo
        </a>
      </div>
    </div>
  </section>
  
  <!-- Features Details Section -->
  <section class="container mx-auto py-20 px-4">
    <div class="text-center mb-16">
      <h2 class="text-3xl md:text-4xl font-bold mb-6 text-gray-900">Powerful Features</h2>
      <div class="h-1 w-20 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-6 rounded-full"></div>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        Explore the comprehensive toolkit that CoachPilot offers to boost your productivity
      </p>
    </div>
    
    <div class="space-y-20">
      <!-- Feature Detail 1 -->
      <div class="flex flex-col md:flex-row items-center gap-10">
        <div class="md:w-1/2">
          <h3 class="text-2xl font-bold mb-4 text-gray-900">Task Management Reimagined</h3>
          <p class="text-gray-600 mb-6">CoachPilot's task management system goes beyond simple to-do lists. Our AI analyzes your work patterns and suggests optimal task organization, priority levels, and estimated completion times.</p>
          <ul class="space-y-3">
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Kanban boards with AI optimization</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Smart task prioritization</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Automated time estimates</span>
            </li>
          </ul>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-8 flex items-center justify-center">
          <div class="w-full h-64 bg-white rounded-xl shadow-xl p-4 flex flex-col">
            <div class="bg-blue-100 rounded-lg p-3 mb-4 flex items-center">
              <CoachpilotIcon size={30} showText={false} />
              <div class="ml-3 text-sm">
                <div class="font-bold text-blue-800">Task Manager</div>
              </div>
            </div>
            <div class="flex-1 p-2 space-y-2">
              <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
              <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
              <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
              <div class="grid grid-cols-3 gap-2 mt-4">
                <div class="bg-blue-50 rounded p-2">
                  <div class="h-2 bg-blue-200 rounded-full mb-1"></div>
                  <div class="h-2 bg-blue-200 rounded-full w-1/2"></div>
                </div>
                <div class="bg-green-50 rounded p-2">
                  <div class="h-2 bg-green-200 rounded-full mb-1"></div>
                  <div class="h-2 bg-green-200 rounded-full w-1/2"></div>
                </div>
                <div class="bg-amber-50 rounded p-2">
                  <div class="h-2 bg-amber-200 rounded-full mb-1"></div>
                  <div class="h-2 bg-amber-200 rounded-full w-1/2"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Feature Detail 2 -->
      <div class="flex flex-col md:flex-row-reverse items-center gap-10">
        <div class="md:w-1/2">
          <h3 class="text-2xl font-bold mb-4 text-gray-900">SMART Goal Achievement</h3>
          <p class="text-gray-600 mb-6">Our goal setting framework uses the SMART methodology (Specific, Measurable, Achievable, Relevant, Time-bound) combined with AI insights to keep you accountable and on track.</p>
          <ul class="space-y-3">
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">AI-assisted goal creation</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Progress tracking with visual metrics</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Adaptive milestone adjustments</span>
            </li>
          </ul>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-8 flex items-center justify-center">
          <div class="w-full h-64 bg-white rounded-xl shadow-xl p-4 flex flex-col">
            <div class="bg-blue-100 rounded-lg p-3 mb-4 flex items-center">
              <CoachpilotIcon size={30} showText={false} />
              <div class="ml-3 text-sm">
                <div class="font-bold text-blue-800">Goal Tracker</div>
              </div>
            </div>
            <div class="flex-1 p-2">
              <div class="mb-4">
                <div class="flex justify-between text-sm mb-1">
                  <span class="font-medium">Complete Project X</span>
                  <span>75%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-blue-600 h-2.5 rounded-full" style="width: 75%"></div>
                </div>
              </div>
              <div class="mb-4">
                <div class="flex justify-between text-sm mb-1">
                  <span class="font-medium">Learn New Skill</span>
                  <span>40%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-blue-600 h-2.5 rounded-full" style="width: 40%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  
  <!-- FAQ Section -->
  <section class="py-20 bg-gray-50 relative">
    <div class="container mx-auto px-4 relative z-10">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold mb-6 text-gray-900">Frequently Asked Questions</h2>
        <div class="h-1 w-20 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-6 rounded-full"></div>
      </div>
      
      <div class="max-w-3xl mx-auto space-y-6">
        <!-- FAQ Item 1 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h4 class="text-lg font-bold mb-2 text-gray-900">How does CoachPilot's AI coaching work?</h4>
          <p class="text-gray-600">CoachPilot uses advanced AI models including cognitive mapping and reinforcement learning to analyze your work patterns, preferences, and goals. It then provides personalized coaching suggestions to help optimize your productivity.</p>
        </div>
        
        <!-- FAQ Item 2 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h4 class="text-lg font-bold mb-2 text-gray-900">Can I integrate CoachPilot with other tools?</h4>
          <p class="text-gray-600">Yes! CoachPilot seamlessly integrates with popular productivity tools including Google Calendar, Microsoft Teams, Slack, and more. This allows for a centralized workflow while maintaining your existing tools.</p>
        </div>
        
        <!-- FAQ Item 3 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h4 class="text-lg font-bold mb-2 text-gray-900">Is my data secure with CoachPilot?</h4>
          <p class="text-gray-600">Absolutely. We implement industry-leading encryption and security practices. Your data is only used to power the AI coaching features and is never sold to third parties or used for advertising purposes.</p>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Final CTA Section -->
  <section class="container mx-auto py-16 px-4 text-center">
    <div class="max-w-3xl mx-auto bg-white rounded-3xl p-10 shadow-2xl border border-gray-100">
      <div class="mb-6 flex justify-center">
        <CoachpilotLogo size={100} showText={false} />
      </div>
      <h2 class="text-3xl font-bold mt-6 mb-4 text-gray-900">Transform Your Productivity Today</h2>
      <p class="text-xl text-gray-600 mb-8">Join thousands of professionals using CoachPilot's AI-driven coaching to maximize their potential.</p>
      <a href="/coachpilot" class="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Get Started Now
      </a>
    </div>
  </section>
</main>

<style>
  /* Apple-inspired styling */
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  
  /* Smooth hover transitions */
  a, button {
    transition: all 0.3s ease;
  }
  
  /* Custom animations */
  @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
  }
  
  .animate-float {
    animation: float 3s ease-in-out infinite;
  }
</style>