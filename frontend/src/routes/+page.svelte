<script>
    // Import all logo components
    import CoachpilotLogo from '../components/logos/coachpilotLogo.svelte';
    import CogitoHubLogo from '../components/logos/cogitohubLogo.svelte';
    import CoursitoLogo from '../components/logos/coursitoLogo.svelte';
    import HabitforgeLogo from '../components/logos/habitforgeLogo.svelte';
    import InsightbridgeLogo from '../components/logos/insightbridgeLogo.svelte';
    import TimetunesLogo from '../components/logos/timetunesLogo.svelte';
    import ZettaLogo from '../components/logos/zettaLogo.svelte';
    import QueritoLogo from '../components/logos/queritoLogo.svelte';
    import CogeeLogo from '../components/logos/cogeeLogo.svelte';
    import QueritoIcon from '../components/icons/queritoIcon.svelte';
    import CogeeIcon from '../components/icons/cogeeIcon.svelte';
  </script>
  
  <main class="min-h-screen bg-gradient-to-b from-white to-gray-50 text-gray-900">
    <!-- Hero Section -->
    <section class="container mx-auto py-20 md:py-32 px-4 flex flex-col items-center relative">
      <!-- Large decorative background elements -->
      <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
        <div class="absolute top-20 left-10 w-64 h-64 rounded-full bg-blue-200 filter blur-3xl opacity-30 animate-pulse"></div>
      <div class="absolute bottom-20 right-10 w-72 h-72 rounded-full bg-purple-200 filter blur-3xl opacity-30 animate-pulse"></div>
      </div>
      
      <!-- Logo and slogan -->
      <div class="relative z-10 mb-12 flex flex-col items-center">
      <div class="mb-8 transform hover:scale-105 transition-all duration-700 ease-out">
        <CogitoHubLogo size={600} showText={false} />
      </div>
     
      <p class="text-3xl md:text-3xl font-bold text-center max-w-4xl mb-6 text-gray-800">
        The Education System of the Future
      </p>
  
  
      <p class="text-xl text-gray-600 text-center max-w-3xl mb-12">
        Breakthrough AI-powered tools and platforms designed to transform how we learn, work, and grow
      </p>
      </div>
      
      <!-- Visual element - animated rings -->
      <div class="relative w-24 h-24 mb-20">
        <div class="absolute inset-0 border-4 border-blue-400 rounded-full opacity-25 animate-ping"></div>
        <div class="absolute inset-2 border-4 border-purple-400 rounded-full opacity-25 animate-pulse"></div>
        <div class="absolute inset-4 border-4 border-pink-400 rounded-full opacity-25 animate-ping" style="animation-delay: 0.5s;"></div>
        <div class="relative bg-white shadow-lg rounded-full w-24 h-24 flex items-center justify-center">
          <CogitoHubLogo size={40} showText={false} />
        </div>
      </div>
      
      <!-- Down arrow animation -->
      <div class="animate-bounce mt-8">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>
    
    <!-- Products Showcase Section -->
    <section class="container mx-auto py-16 px-4 relative">
      <!-- Background decorative elements -->
      <div class="absolute inset-0 overflow-hidden z-0">
        <div class="absolute -top-20 -right-20 w-72 h-72 rounded-full bg-blue-100 filter blur-3xl opacity-30"></div>
        <div class="absolute -bottom-20 -left-20 w-80 h-80 rounded-full bg-purple-100 filter blur-3xl opacity-30"></div>
      </div>
      
      <!-- Section heading -->
      <div class="relative z-10 text-center mb-20">
        <h2 class="text-3xl md:text-5xl font-bold mb-6">Our Ecosystem</h2>
        <div class="h-1 w-20 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          A comprehensive suite of AI tools designed to revolutionize the educational experience
        </p>
      </div>
      
      <!-- CoachPilot -->
      <div class="product-card mb-32 flex flex-col md:flex-row items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <div class="flex items-center space-x-4 mb-4">
            <CogitoHubLogo size={150} />
            <CoachpilotLogo size={150} />
          </div>
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">AI-Powered Academic Mentorship & Coaching</h2>
          <p class="text-xl text-gray-600 mb-6">Unlock your peak performance with personalized strategies to crush your goals</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Personalized productivity coaching</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Focus enhancement techniques</span>
            </li>
            <li class="flex items-center">
              <span class="bg-blue-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Academic success strategies</span>
            </li>
          </ul>
          <a href="/coachpilotinfo" class="inline-block px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-blue-50 to-blue-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-blue-100 rounded-lg p-3 mb-4 flex items-center">
                <CoachpilotLogo size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-blue-800"></div>
                  <div class="text-blue-600">Your productivity assistant</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <CoachpilotLogo size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
     
      
      <!-- Habitforge -->
      <div class="product-card mb-32 flex flex-col md:flex-row items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <CogitoHubLogo size={300} />
          <HabitforgeLogo size={200} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Next-Gen Habit Tracker</h2>
          <p class="text-xl text-gray-600 mb-6">Gamification Pro Max + Atomic Habits Tools</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-green-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Habit analytics dashboard</span>
            </li>
            <li class="flex items-center">
              <span class="bg-green-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Gamified tracking system</span>
            </li>
            <li class="flex items-center">
              <span class="bg-green-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Atomic habit building framework</span>
            </li>
          </ul>
          <a href="/habitforgeinfo" class="inline-block px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-green-50 to-green-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-green-100 rounded-lg p-3 mb-4 flex items-center">
                <HabitforgeLogo size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-green-800">HabitForge</div>
                  <div class="text-green-600">Build lasting habits</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <HabitforgeLogo size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Timetunes -->
      <div class="product-card mb-32 flex flex-col md:flex-row-reverse items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <CogitoHubLogo size={300} />
          <TimetunesLogo size={190} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Smart Time Management</h2>
          <p class="text-xl text-gray-600 mb-6">Time management that learns and adapts</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-amber-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">AI-powered scheduling</span>
            </li>
            <li class="flex items-center">
              <span class="bg-amber-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Notion Calendar++ functionality</span>
            </li>
            <li class="flex items-center">
              <span class="bg-amber-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Adaptive time optimization</span>
            </li>
          </ul>
          <a href="/timetunesinfo" class="inline-block px-8 py-3 bg-amber-600 hover:bg-amber-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
  
        
        <div class="md:w-1/2 bg-gradient-to-r from-amber-50 to-amber-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-amber-100 rounded-lg p-3 mb-4 flex items-center">
                <TimetunesLogo size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-amber-800">TimeTunes</div>
                  <div class="text-amber-600">Smart time management</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <TimetunesLogo size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Querito -->
      <div class="product-card mb-32 flex flex-col md:flex-row items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <CogitoHubLogo size={300} />
          <QueritoLogo size={200} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Knowledge Exchange Platform</h2>
          <p class="text-xl text-gray-600 mb-6">Real-time knowledge exchange with Cogee rewards</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-indigo-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Ask expert questions</span>
            </li>
            <li class="flex items-center">
              <span class="bg-indigo-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Earn Cogees for participation</span>
            </li>
            <li class="flex items-center">
              <span class="bg-indigo-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Community-driven learning</span>
            </li>
          </ul>
          <a href="/querito" class="inline-block px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-indigo-50 to-indigo-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-indigo-100 rounded-lg p-3 mb-4 flex items-center">
                <QueritoIcon size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-indigo-800">Querito</div>
                  <div class="text-indigo-600">Knowledge Exchange</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <QueritoIcon size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cogee -->
      <div class="product-card mb-32 flex flex-col md:flex-row-reverse items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <CogitoHubLogo size={300} />
          <CogeeLogo size={200} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Digital Learning Currency</h2>
          <p class="text-xl text-gray-600 mb-6">Earn, learn and redeem across the CogitoHub ecosystem</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Reward engagement & participation</span>
            </li>
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Unlock premium learning resources</span>
            </li>
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Track learning achievements</span>
            </li>
          </ul>
          <a href="/cogee" class="inline-block px-8 py-3 bg-cyan-600 hover:bg-cyan-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-cyan-50 to-cyan-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-cyan-100 rounded-lg p-3 mb-4 flex items-center">
                <CogeeIcon size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-cyan-800">Cogee</div>
                  <div class="text-cyan-600">Learning Currency</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <CogeeIcon size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Coursito -->
      <div class="product-card mb-32 flex flex-col md:flex-row items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <CoursitoLogo size={300} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Course Review Platform</h2>
          <p class="text-xl text-gray-600 mb-6">Zomato for the e-learning space</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-pink-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Verified user reviews</span>
            </li>
            <li class="flex items-center">
              <span class="bg-pink-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">"Actual Learning Score" metrics</span>
            </li>
            <li class="flex items-center">
              <span class="bg-pink-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">AI-powered course recommendations</span>
            </li>
          </ul>
          <a href="/coursito" class="inline-block px-8 py-3 bg-pink-600 hover:bg-pink-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-pink-50 to-pink-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-pink-100 rounded-lg p-3 mb-4 flex items-center">
                <CoursitoLogo size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-pink-800"></div>
                  <div class="text-pink-600">Find the perfect course</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <CoursitoLogo size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- InsightBridge -->
      <div class="product-card mb-32 flex flex-col md:flex-row-reverse items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
        <div class="md:w-1/2 p-8 md:p-16">
          <InsightbridgeLogo size={400} />
          <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Dynamic Monitoring Dashboard</h2>
          <p class="text-xl text-gray-600 mb-6">Track performance and progress for institutions and parents</p>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Real-time student progress tracking</span>
            </li>
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Analytics for parents and stakeholders</span>
            </li>
            <li class="flex items-center">
              <span class="bg-cyan-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
              <span class="text-gray-700">Performance visualization tools</span>
            </li>
          </ul>
          <a href="/insightbridgeinfo" class="inline-block px-8 py-3 bg-cyan-600 hover:bg-cyan-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Learn More
          </a>
        </div>
        <div class="md:w-1/2 bg-gradient-to-r from-cyan-50 to-cyan-100 h-full p-8 md:p-16 flex items-center justify-center">
          <div class="device-mockup relative">
            <!-- Placeholder for device mockup/screenshot -->
            <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
              <div class="bg-cyan-100 rounded-lg p-3 mb-4 flex items-center">
                <InsightbridgeLogo size={30} />
                <div class="ml-3 text-sm">
                  <div class="font-bold text-cyan-800">InsightBridge</div>
                  <div class="text-cyan-600">Performance monitoring</div>
                </div>
              </div>
              <div class="flex-1 p-2 space-y-2">
                <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
                <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
                <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
                <div class="mt-6 flex justify-center">
                  <InsightbridgeLogo size={80} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    

     <!-- Zetta -->
     <div class="product-card mb-32 flex flex-col md:flex-row-reverse items-center rounded-3xl bg-white shadow-xl overflow-hidden relative z-10">
      <div class="md:w-1/2 p-8 md:p-16">
        <ZettaLogo size={250} />
        <h2 class="text-3xl md:text-4xl font-bold mt-6 mb-4 text-gray-900">Cognitive Knowledge Tracing</h2>
        <p class="text-xl text-gray-600 mb-6">Learning that grows smarter with you</p>
        <ul class="space-y-3 mb-8">
          <li class="flex items-center">
            <span class="bg-purple-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
            <span class="text-gray-700">Adaptive learning algorithms</span>
          </li>
          <li class="flex items-center">
            <span class="bg-purple-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
            <span class="text-gray-700">Personalized knowledge paths</span>
          </li>
          <li class="flex items-center">
            <span class="bg-purple-500 rounded-full w-6 h-6 mr-3 flex items-center justify-center text-white">✓</span>
            <span class="text-gray-700">Memory-optimized learning</span>
          </li>
        </ul>
        <a href="/zettainfo" class="inline-block px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
          Learn More
        </a>
      </div>

      <div class="md:w-1/2 bg-gradient-to-r from-purple-50 to-purple-100 h-full p-8 md:p-16 flex items-center justify-center">
        <div class="device-mockup relative">
          <!-- Placeholder for device mockup/screenshot -->
          <div class="w-full h-64 md:h-80 bg-white rounded-xl shadow-2xl p-4 flex flex-col">
            <div class="bg-purple-100 rounded-lg p-3 mb-4 flex items-center">
              <ZettaLogo size={30} />
              <div class="ml-3 text-sm">
                <div class="font-bold text-purple-800">Zetta AI</div>
                <div class="text-purple-600">Adaptive knowledge tracing</div>
              </div>
            </div>
            <div class="flex-1 p-2 space-y-2">
              <div class="h-3 bg-gray-200 rounded-full w-3/4"></div>
              <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
              <div class="h-3 bg-gray-200 rounded-full w-2/3"></div>
              <div class="mt-6 flex justify-center">
                <ZettaLogo size={80} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    <!-- Feature highlights section -->
    <section class="py-20 bg-gradient-to-br from-blue-50 to-purple-50 relative overflow-hidden">
      <div class="container mx-auto px-4 relative z-10">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-6 text-gray-900">Why Choose Cogito?</h2>
          <div class="h-1 w-20 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Our suite of tools is designed to work together to create a seamless educational ecosystem
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
            <div class="rounded-full bg-blue-100 w-16 h-16 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-3 text-gray-900">AI-Powered Learning</h3>
            <p class="text-gray-600">Advanced algorithms that adapt to your learning style and optimize your educational journey.</p>
          </div>
          
          <!-- Feature 2 -->
          <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
            <div class="rounded-full bg-purple-100 w-16 h-16 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-3 text-gray-900">Fully Customizable</h3>
            <p class="text-gray-600">Personalized experiences tailored to your unique needs, goals, and learning preferences.</p>
          </div>
          
          <!-- Feature 3 -->
          <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
            <div class="rounded-full bg-green-100 w-16 h-16 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-3 text-gray-900">Modern Interfaces</h3>
            <p class="text-gray-600">Enterprise Grade Design, Modern UIs.</p>
          </div>
        </div>
      </div>
      
      <!-- Decorative elements -->
      <div class="absolute top-0 right-0 -mt-20 -mr-20 w-80 h-80 rounded-full bg-blue-100 filter blur-3xl opacity-40"></div>
      <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 rounded-full bg-purple-100 filter blur-3xl opacity-40"></div>
    </section>
    
  
  
    
    <!-- Call to Action Section -->
    <section class="py-24 px-4 text-center relative overflow-hidden">
      <!-- Background with gentle gradient -->
      <div class="absolute inset-0 bg-gradient-to-r from-blue-50 via-white to-purple-50 z-0"></div>
      
      <!-- Decorative elements -->
      <div class="absolute top-0 left-0 -mt-20 -ml-20 w-80 h-80 rounded-full bg-blue-100 filter blur-3xl opacity-40"></div>
      <div class="absolute bottom-0 right-0 -mb-20 -mr-20 w-80 h-80 rounded-full bg-purple-100 filter blur-3xl opacity-40"></div>
      
      <div class="container mx-auto relative z-10">
        <div class="max-w-4xl mx-auto rounded-3xl p-8 md:p-16 bg-white shadow-2xl border border-gray-100">
          <h2 class="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-transparent bg-clip-text">Ready to Transform Your Learning?</h2>
          <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Discover our AI-powered ecosystem and take the next step in your productivity, learning, and personal development journey.
          </p>
          <div class="flex flex-wrap gap-4 justify-center">
            <a href="/cogito" class="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              Get Started Today
            </a>
            <a href="/info" class="px-8 py-4 border-2 border-purple-600 text-purple-600 hover:bg-purple-50 rounded-full font-medium transition-all transform hover:-translate-y-1">
              Learn More
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>
  
  <style>
    /* Apple-inspired styling */
    :global(body) {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    
    /* Smooth card hover effects */
    .product-card {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .product-card:hover {
      transform: translateY(-8px);
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
    }
    
    /* Device mockup styling */
    .device-mockup {
      transform: perspective(1000px) rotateY(-15deg);
      transition: transform 0.5s ease;
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.1);
    }
    
    .product-card:hover .device-mockup {
      transform: perspective(1000px) rotateY(-5deg);
    }
    
    /* Custom animations */
    @keyframes float {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
      100% { transform: translateY(0px); }
    }
    
    @keyframes pulse-ring {
      0% { transform: scale(0.95); opacity: 0.7; }
      50% { transform: scale(1); opacity: 0.9; }
      100% { transform: scale(0.95); opacity: 0.7; }
    }
    
   
  </style>