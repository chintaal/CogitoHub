<script>
    import CoursitoLogo from '../../components/logos/coursitoLogo.svelte';
    import CoursitoIcon from '../../components/icons/coursitoIcon.svelte';
    import { onMount } from 'svelte';
    
    // For animation effects
    let isLoaded = false;
    
    // Sample data for course platforms
    const platforms = [
        { name: "Udemy", logo: "https://s.udemycdn.com/meta/default-meta-image-v2.png", courses: "3,500+" },
        { name: "Coursera", logo: "https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/media/coursera-rebrand-logo-square.png", courses: "1,200+" },
        { name: "edX", logo: "https://www.edx.org/images/logos/edx-logo-elm.svg", courses: "850+" },
        { name: "LinkedIn Learning", logo: "https://cdn.lynda.com/static/landing/images/meta/linkedin-learning-banner-image-v2.jpg", courses: "2,100+" },
        { name: "Pluralsight", logo: "https://www.pluralsight.com/content/dam/pluralsight2/general/icons/light/ps-icon.png", courses: "700+" },
        { name: "Skillshare", logo: "https://static.skillshare.com/assets/images/default-meta-ogg-image.jpg", courses: "1,800+" }
    ];
    
    // Sample metrics for the platform
    const metrics = [
        { value: "50,000+", label: "Verified Reviews" },
        { value: "8,400+", label: "Courses Analyzed" },
        { value: "94%", label: "User Satisfaction" },
        { value: "12,500+", label: "Personalized Recommendations" }
    ];
    
    // Testimonials from users
    const testimonials = [
        {
            name: "Sarah T.",
            role: "Data Science Student",
            image: "https://randomuser.me/api/portraits/women/12.jpg",
            quote: "Coursito saved me over $300 by steering me away from overhyped courses to ones with actual value. The AI recommendations were spot-on for my career goals."
        },
        {
            name: "Michael R.",
            role: "Software Engineer",
            image: "https://randomuser.me/api/portraits/men/45.jpg",
            quote: "The side-by-side course comparison is a game-changer. I can now make informed decisions in minutes instead of hours of research."
        },
        {
            name: "Priya K.",
            role: "UX Designer",
            image: "https://randomuser.me/api/portraits/women/32.jpg",
            quote: "As someone who invests heavily in continuous learning, Coursito has become my go-to platform before purchasing any online course."
        }
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
      <!-- Logo with entrance animation - Fixed size and made more visible -->
      <div class={`mb-8 transform transition-all duration-1000 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
        <div class="w-64 h-64 mx-auto">
          <CoursitoLogo />
        </div>
      </div>
      
      <!-- Headline with staggered entrance -->
      <h1 class={`text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text transition-all duration-1000 delay-300 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
        Your AI Course Advisor & Review Platform
      </h1>
      
      <p class={`text-xl md:text-2xl text-gray-600 max-w-3xl mb-8 transition-all duration-1000 delay-500 ease-out ${isLoaded ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
        Stop wasting time and money on mediocre courses. Discover the perfect learning experience tailored to your unique goals and learning style.
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
          The <span class="bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text">Smart Filter</span> for E-Learning
        </h2>
        <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Don't let slick marketing fool you. Find courses with proven results using our AI-powered platform.
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
          <h3 class="text-2xl font-bold mb-4">Beyond 5-Star Reviews</h3>
          <p class="text-gray-600">Our AI analyzes review sentiment, instructor responsiveness, and actual student outcomes to reveal the real value behind the ratings.</p>
        </div>
        
        <!-- Feature 2 -->
        <div class="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-transform hover:-translate-y-2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-100">
          <div class="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold mb-4">"Actual Learning Score"</h3>
          <p class="text-gray-600">Our proprietary metric combines content quality, practical application, and long-term knowledge retention to measure what you'll actually learn.</p>
        </div>
        
        <!-- Feature 3 -->
        <div class="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-transform hover:-translate-y-2 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-200">
          <div class="w-16 h-16 rounded-full bg-pink-100 flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold mb-4">Personalized Learning Path</h3>
          <p class="text-gray-600">Tell us your goals, background, and learning style, and our AI builds a custom curriculum from the best courses across all platforms.</p>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Testimonials section -->
  <section class="py-24 bg-white">
    <div class="container mx-auto px-4">
      <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
        <h2 class="text-3xl md:text-5xl font-bold mb-6">What Our Users Say</h2>
        <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Join thousands of learners who've transformed their educational journey with Coursito.
        </p>
      </div>
      
      <div class="grid md:grid-cols-3 gap-8">
        {#each testimonials as testimonial, i}
          <div class="bg-gradient-to-r from-pink-50 to-purple-50 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000" style="transition-delay: {i * 100}ms">
            <div class="flex items-center mb-6">
              <img src={testimonial.image} alt={testimonial.name} class="w-14 h-14 rounded-full object-cover border-2 border-purple-200" />
              <div class="ml-4">
                <div class="font-bold text-lg">{testimonial.name}</div>
                <div class="text-sm text-gray-600">{testimonial.role}</div>
              </div>
            </div>
            <blockquote class="text-gray-700 italic">"{testimonial.quote}"</blockquote>
          </div>
        {/each}
      </div>
    </div>
  </section>
  
  <!-- How it works section -->
  <section class="py-24 bg-gradient-to-r from-pink-50 to-purple-50 relative">
    <div class="container mx-auto px-4">
      <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
        <h2 class="text-3xl md:text-5xl font-bold mb-6">How Coursito Works</h2>
        <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Finding your perfect learning path is simple, efficient, and even enjoyable.
        </p>
      </div>
      
      <div class="grid md:grid-cols-4 gap-8">
        <!-- Step 1 -->
        <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
          <div class="w-16 h-16 rounded-full bg-pink-600 text-white text-2xl font-bold flex items-center justify-center mb-6">1</div>
          <h3 class="text-2xl font-bold mb-4">Share Your Goals</h3>
          <p class="text-gray-600">Tell our AI about your learning objectives, skill level, and career aspirations.</p>
        </div>
        
        <!-- Step 2 -->
        <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-100">
          <div class="w-16 h-16 rounded-full bg-purple-600 text-white text-2xl font-bold flex items-center justify-center mb-6">2</div>
          <h3 class="text-2xl font-bold mb-4">Get Matched</h3>
          <p class="text-gray-600">Our algorithm matches you with courses that align with your learning style and goals.</p>
        </div>
        
        <!-- Step 3 -->
        <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-200">
          <div class="w-16 h-16 rounded-full bg-pink-600 text-white text-2xl font-bold flex items-center justify-center mb-6">3</div>
          <h3 class="text-2xl font-bold mb-4">Compare & Decide</h3>
          <p class="text-gray-600">Use our side-by-side comparison tools to evaluate courses by what matters most to you.</p>
        </div>
        
        <!-- Step 4 -->
        <div class="flex flex-col items-center text-center animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000 delay-300">
          <div class="w-16 h-16 rounded-full bg-purple-600 text-white text-2xl font-bold flex items-center justify-center mb-6">4</div>
          <h3 class="text-2xl font-bold mb-4">Track Your Progress</h3>
          <p class="text-gray-600">Rate courses as you complete them to improve recommendations and help other learners.</p>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Platform showcase -->
  <section class="py-20 bg-white relative overflow-hidden">
    <div class="container mx-auto px-4 relative z-10">
      <div class="text-center mb-16 animate-on-scroll opacity-0 transform translate-y-10 transition-all duration-1000">
        <h2 class="text-3xl md:text-5xl font-bold mb-6">Platforms We Cover</h2>
        <div class="h-1 w-24 bg-gradient-to-r from-pink-500 to-purple-500 mx-auto mb-6 rounded-full"></div>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          We analyze courses from all major learning platforms so you can make the best choice, regardless of provider.
        </p>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center">
        {#each platforms as platform, i}
          <div class="flex flex-col items-center gap-4 bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 animate-on-scroll opacity-0 transition-all duration-700" style="transition-delay: {i * 50}ms">
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
            Stop wasting time and money on courses that don't deliver. Our AI-powered platform ensures you get the maximum return on your educational investment.
          </p>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <span>Average time savings: 6+ hours per course selection</span>
            </li>
            <li class="flex items-center">
              <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <span>97% of users found better courses at lower prices</span>
            </li>
            <li class="flex items-center">
              <div class="w-8 h-8 bg-pink-500 bg-opacity-30 rounded-full flex items-center justify-center mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <span>Skill acquisition rates improved by 32%</span>
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
                <div class="h-8 w-8">
                  <CoursitoIcon />
                </div>
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
        <div class="mb-8 w-36 h-36 mx-auto">
          <CoursitoLogo />
        </div>
        <h2 class="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-pink-600 to-purple-600 text-transparent bg-clip-text">
          Stop Guessing. Start Learning.
        </h2>
        <p class="text-xl text-gray-600 mb-10">
          Join our early access program and be the first to transform your educational journey with Coursito's AI-powered course recommendations.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <button class="px-8 py-4 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white rounded-full font-medium transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Join the Early Access
          </button>
          <button class="px-8 py-4 border-2 border-purple-600 text-purple-600 hover:bg-purple-50 rounded-full font-medium transition-all transform hover:-translate-y-1">
            Request Demo
          </button>
        </div>
        
        <p class="mt-8 text-sm text-gray-500">
          Currently in beta. Full platform launch scheduled for Q2 2023.
        </p>
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