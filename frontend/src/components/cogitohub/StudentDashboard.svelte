<script>
  import { onMount } from 'svelte';
  
  export let activeSection;
  export let userProfile;
  
  // Mock data for demonstration
  let projects = [
    {
      id: 'p1',
      title: 'Machine Learning for Healthcare',
      description: 'Research project focused on developing ML algorithms for early disease detection',
      professor: 'Dr. Sarah Chen',
      university: 'Stanford University',
      skills: ['Python', 'TensorFlow', 'Healthcare'],
      type: 'Research',
      deadline: '2025-06-15',
      applicants: 12,
      status: 'Open'
    },
    {
      id: 'p2',
      title: 'Sustainable Urban Planning App',
      description: 'Develop a mobile application to help urban planners design more sustainable cities',
      professor: 'Prof. Michael Johnson',
      university: 'MIT',
      skills: ['React Native', 'Firebase', 'GIS'],
      type: 'Development',
      deadline: '2025-05-30',
      applicants: 8,
      status: 'Open'
    },
    {
      id: 'p3',
      title: 'Blockchain for Supply Chain Transparency',
      description: 'Implementing blockchain solutions to improve transparency in global supply chains',
      professor: 'Dr. Robert Williams',
      university: 'UC Berkeley',
      skills: ['Solidity', 'Ethereum', 'Supply Chain'],
      type: 'Industry Collaboration',
      deadline: '2025-07-10',
      applicants: 5,
      status: 'Open'
    }
  ];
  
  let resources = [
    {
      id: 'r1',
      title: 'Complete Machine Learning Roadmap',
      description: 'A comprehensive guide to learning machine learning from beginner to advanced',
      author: 'Dr. Andrew Miller',
      type: 'Learning Path',
      rating: 4.9,
      downloadCount: 1245
    },
    {
      id: 'r2',
      title: 'Academic Research Paper Template',
      description: 'LaTeX template for academic research papers following IEEE standards',
      author: 'Prof. Lisa Johnson',
      type: 'Template',
      rating: 4.7,
      downloadCount: 873
    },
    {
      id: 'r3',
      title: 'The Art of Technical Writing',
      description: 'Guide to writing clear and effective technical documentation',
      author: 'Dr. James Wilson',
      type: 'E-Book',
      rating: 4.8,
      downloadCount: 962
    }
  ];
  
  let courses = [
    {
      id: 'c1',
      title: 'Advanced Deep Learning',
      description: 'Deep dive into neural network architectures and state-of-the-art techniques',
      professor: 'Dr. Emma Davis',
      university: 'Stanford University',
      duration: '8 weeks',
      startDate: '2025-05-01',
      enrolled: 156,
      level: 'Advanced'
    },
    {
      id: 'c2',
      title: 'Introduction to Quantum Computing',
      description: 'Learn the fundamentals of quantum computing and its applications',
      professor: 'Dr. Richard Feynman',
      university: 'CalTech',
      duration: '10 weeks',
      startDate: '2025-06-15',
      enrolled: 89,
      level: 'Intermediate'
    },
    {
      id: 'c3',
      title: 'Sustainable Engineering Practices',
      description: 'Explore environmentally sustainable approaches to engineering projects',
      professor: 'Dr. Laura Green',
      university: 'MIT',
      duration: '6 weeks',
      startDate: '2025-05-20',
      enrolled: 112,
      level: 'All Levels'
    }
  ];
  
  let opportunities = [
    {
      id: 'o1',
      title: 'Summer Research Internship: AI Ethics',
      company: 'Google Research',
      location: 'Mountain View, CA',
      type: 'Research Internship',
      compensation: 'Paid',
      duration: '3 months',
      deadline: '2025-05-15',
      skills: ['Ethics', 'AI', 'Research']
    },
    {
      id: 'o2',
      title: 'Research Assistant: Climate Modeling',
      company: 'Climate Science Institute',
      location: 'Remote',
      type: 'Research Assistant',
      compensation: 'Stipend',
      duration: '6 months',
      deadline: '2025-06-01',
      skills: ['Python', 'Data Analysis', 'Climate Science']
    },
    {
      id: 'o3',
      title: 'Software Engineering Intern',
      company: 'Microsoft',
      location: 'Seattle, WA',
      type: 'Industry Internship',
      compensation: 'Paid',
      duration: '12 weeks',
      deadline: '2025-04-30',
      skills: ['Full Stack', 'Cloud', 'Azure']
    }
  ];

  // Filter functions for personalization
  function getRecommendedProjects() {
    // In a real app, this would use the user's profile data and interests
    return projects;
  }
  
  function getRecommendedCourses() {
    return courses;
  }
  
  function getRecommendedResources() {
    return resources;
  }
  
  function getRecommendedOpportunities() {
    return opportunities;
  }
  
  onMount(() => {
    // Here you would fetch real data based on the user's profile
    console.log('Student dashboard mounted');
    console.log(`Loading personalized data for student: ${userProfile?.displayName}`);
  });
</script>

<div>
  <!-- Header section with student info -->
  <div class="mb-8">
    <h1 class="text-2xl font-bold text-gray-900">Welcome, {userProfile?.displayName || 'Student'}</h1>
    <p class="text-gray-600">{userProfile?.institution || 'Your Institution'}</p>
  </div>

  <!-- Projects Section -->
  {#if $activeSection === 'projects'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Projects</h2>
        <div class="flex gap-2">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Sort
          </button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {#each getRecommendedProjects() as project}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{project.title}</h3>
                <span class="bg-green-100 text-green-800 text-xs px-2.5 py-0.5 rounded">{project.status}</span>
              </div>
              <p class="text-gray-600 text-sm">{project.professor} • {project.university}</p>
              <p class="mt-3 text-gray-700">{project.description}</p>
              
              <div class="mt-4 flex flex-wrap gap-1">
                {#each project.skills as skill}
                  <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded">{skill}</span>
                {/each}
              </div>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="text-sm text-gray-500">
                  <span>Deadline: {new Date(project.deadline).toLocaleDateString()}</span>
                </div>
                <button class="px-4 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
                  Apply
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
  
  <!-- Resources Section -->
  {#if $activeSection === 'resources'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Learning Resources</h2>
        <div class="flex gap-2">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {#each getRecommendedResources() as resource}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{resource.title}</h3>
                <span class="bg-purple-100 text-purple-800 text-xs px-2.5 py-0.5 rounded">{resource.type}</span>
              </div>
              <p class="text-gray-600 text-sm">By {resource.author}</p>
              <p class="mt-3 text-gray-700">{resource.description}</p>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="flex items-center text-sm">
                  <span class="text-yellow-500 mr-1">★</span>
                  <span>{resource.rating}</span>
                  <span class="mx-2">•</span>
                  <span>{resource.downloadCount} downloads</span>
                </div>
                <button class="px-4 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
                  Download
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
  
  <!-- Courses Section -->
  {#if $activeSection === 'courses'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Available Courses</h2>
        <div class="flex gap-2">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {#each getRecommendedCourses() as course}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{course.title}</h3>
                <span class="bg-indigo-100 text-indigo-800 text-xs px-2.5 py-0.5 rounded">{course.level}</span>
              </div>
              <p class="text-gray-600 text-sm">{course.professor} • {course.university}</p>
              <p class="mt-3 text-gray-700">{course.description}</p>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="flex flex-col text-sm text-gray-500">
                  <span>Duration: {course.duration}</span>
                  <span>Starts: {new Date(course.startDate).toLocaleDateString()}</span>
                </div>
                <button class="px-4 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
                  Enroll
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
  
  <!-- Opportunities Section -->
  {#if $activeSection === 'opportunities'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Research & Internship Opportunities</h2>
        <div class="flex gap-2">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {#each getRecommendedOpportunities() as opportunity}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start mb-2">
                <h3 class="text-lg font-semibold text-gray-900">{opportunity.title}</h3>
                <span class="bg-amber-100 text-amber-800 text-xs px-2.5 py-0.5 rounded">{opportunity.compensation}</span>
              </div>
              <p class="text-gray-600 text-sm">{opportunity.company} • {opportunity.location}</p>
              <p class="text-gray-600 text-sm mt-1">{opportunity.type} • {opportunity.duration}</p>
              
              <div class="mt-4 flex flex-wrap gap-1">
                {#each opportunity.skills as skill}
                  <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded">{skill}</span>
                {/each}
              </div>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="text-sm text-gray-500">
                  <span>Deadline: {new Date(opportunity.deadline).toLocaleDateString()}</span>
                </div>
                <button class="px-4 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
                  Apply
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>