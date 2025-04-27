<script>
    import CoursitoLogo from '../../components/logos/coursitoLogo.svelte';
    import CoursitoIcon from '../../components/icons/coursitoIcon.svelte';
    import { onMount } from 'svelte';
    
    // For animation effects
    let isLoaded = false;
    
    // Sample data for reviews
    const reviews = [
      {
        name: "Alex Johnson",
        role: "Computer Science Student",
        image: "https://randomuser.me/api/portraits/men/32.jpg",
        text: "Coursito helped me find the perfect machine learning course that actually taught practical skills. The 'Actual Learning Score' feature saved me from wasting money on overhyped courses.",
        stars: 5
      },
      {
        name: "Priya Patel",
        role: "UX Design Professional",
        image: "https://randomuser.me/api/portraits/women/44.jpg",
        text: "The AI recommendations were spot on! Found a UX design course that perfectly matched my skill level and learning goals. I've tried other platforms but nothing compares to the accuracy of Coursito.",
        stars: 5
      },
      {
        name: "Marcus Chen",
        role: "Web Developer",
        image: "https://randomuser.me/api/portraits/men/22.jpg",
        text: "The verified reviews make all the difference. I can trust that I'm getting honest feedback about courses before investing my time and money. Coursito is now my go-to for all learning decisions.",
        stars: 4
      }
    ];
    
    // Sample data for course platforms
    const platforms = [
      { name: "Udemy", logo: "https://s.udemycdn.com/meta/default-meta-image-v2.png", courses: "3,500+" },
      { name: "Coursera", logo: "https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/media/coursera-rebrand-logo-square.png", courses: "1,200+" },
      { name: "edX", logo: "https://www.edx.org/images/logos/edx-logo-elm.svg", courses: "850+" },
      { name: "LinkedIn Learning", logo: "https://cdn.lynda.com/static/landing/images/meta/linkedin-learning-banner-image-v2.jpg", courses: "2,100+" },
      { name: "Pluralsight", logo: "https://www.pluralsight.com/content/dam/pluralsight2/general/icons/light/ps-icon.png", courses: "700+" }
    ];
    
    // Sample metrics for the platform
    const metrics = [
      { value: "50,000+", label: "Verified Reviews" },
      { value: "8,400+", label: "Courses Analyzed" },
      { value: "94%", label: "User Satisfaction" },
      { value: "12,500+", label: "Personalized Recommendations" }
    ];
    
    onMount(() => {
      // Trigger animations after component mounts
      setTimeout(() => {
        isLoaded = true;
      }, 100);
      
      // Initialize intersection observer for scroll animations
      const sections = document.querySelectorAll('.animate-on-scroll');
      const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
      };
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-visible');
            observer.unobserve(entry.target);
          }
        });
      }, observerOptions);
      
      sections.forEach(section => {
        observer.observe(section);
      });
    });
  </script>
  
  <main class="flex flex-col min-h-screen bg-gradient-to-b from-white to-gray-50 text-gray-900 overflow-hidden">
    <!-- Hero Section with parallax effect -->
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <!-- Background decorative elements with parallax effect -->
      <div class="absolute inset-0 z-0">
        <div class="absolute top-20 left-10 w-80 h-80 rounded-full bg-pink-200 filter blur-3xl opacity-20 transform -translate-y-1/4"></div>
        <div class="absolute bottom-20 right-10 w-72 h-72 rounded-full bg-purple-200 filter blur-3xl opacity-20 transform translate-y-1/4"></div>
      </div>
      
      <div class="relative z-10 container mx-auto px-4 flex flex-col items-center text-center max-w-5xl">
        <!-- Logo with entrance animation -->
        <div class={`mb-8 transform transition-all duration-1000 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <CoursitoLogo size={400} showText={false} />
        </div>
        
        <!-- Headline with staggered entrance -->
        <h1 class={`text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text transition-all duration-1000 delay-300 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          Find Your Perfect Learning Experience
        </h1>
        
        <p class={`text-xl md:text-2xl text-gray-600 max-w-3xl mb-8 transition-all duration-1000 delay-500 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          The world's first AI-powered course review platform that helps you make informed decisions about your educational journey.
        </p>
        
        <!-- CTAs with staggered entrance -->
        <div class={`flex flex-wrap gap-4 justify-center transition-all duration-1000 delay-700 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <button class="px-8 py-4 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Start Exploring
          </button>
          <button class="px-8 py-4 border-2 border-pink-600 text-pink-600 hover:bg-pink-50 rounded-full font-medium transition-all transform hover:-translate-y-1">
            How It Works
          </button>
        </div>
        
        <!-- Scroll indicator -->
        <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </div>
    </section>
    
    <!-- Platform metrics section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          {#each metrics as metric}
            <div class="text-center">
              <div class="text-4xl md:text-5xl font-bold mb-2 bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text">
                {metric.value}
              </div>
              <div class="text-gray-600">{metric.label}</div>
            </div>
          {/each}
        </div>
      </div>
    </section>
    
    <!-- Feature overview section -->
    <section class="py-20 bg-gradient-to-r from-pink-50 to-purple-50 relative overflow-hidden">
      <!-- Decorative background elements -->
      <div class="absolute top-0 right-0 w-1/2 h-1/2 bg-pink-100 rounded-full filter blur-3xl opacity-30 transform translate-x-1/2 -translate-y-1/2"></div>
      <div class="absolute bottom-0 left-0 w-1/2 h-1/2 bg-purple-100 rounded-full filter blur-3xl opacity-30 transform -translate-x-1/2 translate-y-1/2"></div>
      
      <div class="container mx-auto px-4 relative z-10">
        <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <h2 class="text-3xl md:text-5xl font-bold mb-6">
            The <span class="bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text">Zomato</span> for E-Learning
          </h2>
          <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            We're revolutionizing how you discover, evaluate, and choose online courses with our AI-powered platform.
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-12">
          <!-- Feature 1 -->
          <div class="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-transform hover:-translate-y-2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
            <div class="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">Verified User Reviews</h3>
            <p class="text-gray-600">Only genuine student reviews that have been verified through our proprietary authentication system. No more fake reviews or marketing hype.</p>
          </div>
          
          <!-- Feature 2 -->
          <div class="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-transform hover:-translate-y-2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-100">
            <div class="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">"Actual Learning Score"</h3>
            <p class="text-gray-600">Our proprietary metric measures real learning outcomes, not just completion rates or instructor ratings. Know what you'll actually learn before investing.</p>
          </div>
          
          <!-- Feature 3 -->
          <div class="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-transform hover:-translate-y-2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-200">
            <div class="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center mb-6">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold mb-4">AI Recommendations</h3>
            <p class="text-gray-600">Our advanced AI analyzes your skills, goals, and learning style to recommend courses that are perfectly tailored to your unique educational journey.</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- How it works section -->
    <section class="py-24 bg-white relative">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <h2 class="text-3xl md:text-5xl font-bold mb-6">How Coursito Works</h2>
          <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Finding the perfect course has never been easier with our intuitive platform.
          </p>
        </div>
        
        <div class="grid md:grid-cols-4 gap-8">
          <!-- Step 1 -->
          <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
            <div class="w-16 h-16 rounded-full bg-pink-600 text-white text-2xl font-bold flex items-center justify-center mb-6">1</div>
            <h3 class="text-2xl font-bold mb-4">Tell Us Your Goals</h3>
            <p class="text-gray-600">Share your learning objectives, skill level, and preferences to help our AI understand your needs.</p>
          </div>
          
          <!-- Step 2 -->
          <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-100">
            <div class="w-16 h-16 rounded-full bg-purple-600 text-white text-2xl font-bold flex items-center justify-center mb-6">2</div>
            <h3 class="text-2xl font-bold mb-4">Browse Reviews</h3>
            <p class="text-gray-600">Explore verified reviews from real students who've completed the courses you're interested in.</p>
          </div>
          
          <!-- Step 3 -->
          <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-200">
            <div class="w-16 h-16 rounded-full bg-pink-600 text-white text-2xl font-bold flex items-center justify-center mb-6">3</div>
            <h3 class="text-2xl font-bold mb-4">Compare Learning Scores</h3>
            <p class="text-gray-600">Use our Actual Learning Score to compare courses objectively and make informed decisions.</p>
          </div>
          
          <!-- Step 4 -->
          <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-300">
            <div class="w-16 h-16 rounded-full bg-purple-600 text-white text-2xl font-bold flex items-center justify-center mb-6">4</div>
            <h3 class="text-2xl font-bold mb-4">Get Learning!</h3>
            <p class="text-gray-600">Start your educational journey with confidence knowing you've made the right choice.</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Platform showcase -->
    <section class="py-20 bg-gradient-to-r from-purple-50 to-pink-50 relative overflow-hidden">
      <div class="container mx-auto px-4 relative z-10">
        <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <h2 class="text-3xl md:text-5xl font-bold mb-6">Platforms We Cover</h2>
          <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            We analyze courses from all major e-learning platforms to give you complete coverage.
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8 items-center">
          {#each platforms as platform}
            <div class="flex flex-col items-center gap-4 bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 animate-on-scroll opacity-0 transition-all duration-700">
              <div class="h-16 flex items-center justify-center">
                <img src={platform.logo} alt={platform.name} class="h-full object-contain" />
              </div>
              <div class="text-center">
                <div class="font-bold">{platform.name}</div>
                <div class="text-sm text-gray-500">{platform.courses} courses</div>
              </div>
            </div>
          {/each}
        </div>
      </div>
      
      <!-- Decorative elements -->
      <div class="absolute top-0 left-0 w-1/2 h-1/2 bg-purple-100 rounded-full filter blur-3xl opacity-30 transform -translate-x-1/2 -translate-y-1/2"></div>
      <div class="absolute bottom-0 right-0 w-1/2 h-1/2 bg-pink-100 rounded-full filter blur-3xl opacity-30 transform translate-x-1/2 translate-y-1/2"></div>
    </section>
    
    <!-- User testimonials -->
    <section class="py-24 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <h2 class="text-3xl md:text-5xl font-bold mb-6">What Our Users Say</h2>
          <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Don't just take our word for it - hear from students who've found their perfect learning path.
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          {#each reviews as review, i}
            <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000" style="transition-delay: {i * 100}ms">
              <div class="flex items-center mb-6">
                <img src={review.image} alt={review.name} class="w-16 h-16 rounded-full mr-4 object-cover" />
                <div>
                  <div class="font-bold text-lg">{review.name}</div>
                  <div class="text-gray-600 text-sm">{review.role}</div>
                </div>
              </div>
              
              <div class="flex mb-4">
                {#each Array(5) as _, i}
                  <svg xmlns="http://www.w3.org/2000/svg" class={`h-5 w-5 ${i < review.stars ? 'text-yellow-500' : 'text-gray-300'}`} viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                {/each}
              </div>
              
              <p class="text-gray-600 italic">"<span class="text-gray-900">{review.text}</span>"</p>
            </div>
          {/each}
        </div>
      </div>
    </section>
    
    <!-- Interactive mockup section -->
    <section class="py-24 bg-gradient-to-br from-pink-600 to-purple-700 text-white relative overflow-hidden">
      <!-- Decorative elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute top-1/4 left-1/4 w-1/2 h-1/2 bg-white opacity-10 rounded-full filter blur-3xl"></div>
        <div class="absolute bottom-1/4 right-1/4 w-1/2 h-1/2 bg-white opacity-10 rounded-full filter blur-3xl"></div>
      </div>
      
      <div class="container mx-auto px-4 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-16">
          <div class="md:w-1/2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
            <h2 class="text-4xl md:text-5xl font-bold mb-6">Experience the Future of Course Selection</h2>
            <p class="text-xl mb-8 text-pink-100">
              Our intuitive interface makes finding the perfect learning resource simple, efficient, and even enjoyable.
            </p>
            <ul class="space-y-4 mb-8">
              <li class="flex items-center">
                <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>Powerful filtering and sorting options</span>
              </li>
              <li class="flex items-center">
                <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>Side-by-side course comparison</span>
              </li>
              <li class="flex items-center">
                <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>Interactive decision-making tools</span>
              </li>
            </ul>
            
            <button class="px-8 py-4 bg-white text-purple-700 hover:bg-pink-100 rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              Try Coursito Beta
            </button>
          </div>
          
          <div class="md:w-1/2 mt-12 md:mt-0 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-300">
            <!-- App mockup -->
            <div class="device-mockup relative transform perspective-1000 rotateY-10deg rotateX-5deg">
              <div class="bg-white rounded-2xl shadow-2xl overflow-hidden border-8 border-gray-800 relative">
                <!-- App header -->
                <div class="bg-gradient-to-r from-pink-600 to-purple-600 p-4 flex items-center">
                  <CoursitoLogo size={30} showText={false} />
                  <div class="ml-3 text-white">
                    <div class="font-bold">Coursito</div>
                    <div class="text-xs opacity-75">Find your perfect course</div>
                  </div>
                </div>
                
                <!-- App content -->
                <div class="p-4 bg-gray-50">
                  <div class="mb-4">
                    <div class="h-10 bg-white rounded-full shadow-md flex items-center px-4 mb-4">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                      <div class="text-gray-400">Search for courses...</div>
                    </div>
                    
                    <!-- Course card -->
                    <div class="bg-white rounded-xl shadow-md p-4 mb-4">
                      <div class="flex justify-between items-start">
                        <div>
                          <div class="font-bold text-gray-900">Machine Learning A-Z™</div>
                          <div class="text-sm text-gray-600">Udemy • 42.5 hours</div>
                        </div>
                        <div class="bg-green-100 text-green-800 font-bold rounded-full px-3 py-1 text-sm">
                          9.2 ALS
                        </div>
                      </div>
                      
                      <div class="flex items-center mt-2 mb-2">
                        {#each Array(5) as _, i}
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                        {/each}
                        <span class="text-sm text-gray-600 ml-2">(1,245 reviews)</span>
                      </div>
                      
                      <div class="bg-gray-50 rounded-lg p-2 text-sm text-gray-700 mt-2">
                        "This course completely changed my career path. The practical projects are excellent."
                      </div>
                    </div>
                    
                    <!-- Course card -->
                    <div class="bg-white rounded-xl shadow-md p-4">
                      <div class="flex justify-between items-start">
                        <div>
                          <div class="font-bold text-gray-900">Python for Data Science</div>
                          <div class="text-sm text-gray-600">Coursera • 28 hours</div>
                        </div>
                        <div class="bg-green-100 text-green-800 font-bold rounded-full px-3 py-1 text-sm">
                          8.7 ALS
                        </div>
                      </div>
                      
                      <div class="flex items-center mt-2 mb-2">
                        {#each Array(4) as _, i}
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                        {/each}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        <span class="text-sm text-gray-600 ml-2">(873 reviews)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Call to action -->
    <section class="py-24 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <div class="mb-8">
            <CoursitoLogo size={200} showText={false} />
          </div>
          <h2 class="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text">
            Ready to Find Your Perfect Learning Path?
          </h2>
          <p class="text-xl text-gray-600 mb-10">
            Join thousands of learners who've discovered the power of making informed educational choices with Coursito.
          </p>
          <div class="flex flex-wrap justify-center gap-4">
            <button class="px-8 py-4 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              Join the Waitlist
            </button>
            <button class="px-8 py-4 border-2 border-purple-600 text-purple-600 hover:bg-purple-50 rounded-full font-medium transition-all transform hover:-translate-y-1">
              Contact Us
            </button>
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
    
    /* Animation classes */
    .animate-visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
    
    /* Device mockup with 3D effect */
    .device-mockup {
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
      transition: all 0.5s ease;
    }
    
    .device-mockup:hover {
      transform: perspective(1000px) rotateY(-5deg) rotateX(2deg) translateY(-10px);
    }
    
    /* Custom perspective and rotation classes */
    .perspective-1000 {
      perspective: 1000px;
    }
    
    .rotateY-10deg {
      transform: rotateY(-10deg);
    }
    
    .rotateX-5deg {
      transform: rotateX(5deg);
    }
    
    @keyframes float {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
      100% { transform: translateY(0px); }
    }
    
    .animate-float {
      animation: float 3s ease-in-out infinite;
    }
  </style>