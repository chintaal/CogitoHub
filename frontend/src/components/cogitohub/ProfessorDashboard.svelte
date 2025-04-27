<script>
  import { onMount } from 'svelte';
  
  export let activeSection;
  export let userProfile;
  
  // Mock data for professor dashboard
  let myProjects = [
    {
      id: 'p1',
      title: 'AI for Climate Change Prediction',
      description: 'Developing machine learning models to predict climate change impacts on local ecosystems',
      status: 'Active',
      students: 3,
      applicants: 5,
      deadline: '2025-05-20',
      skills: ['Python', 'Machine Learning', 'Climate Science']
    },
    {
      id: 'p2',
      title: 'Quantum Computing Algorithms',
      description: 'Research on novel quantum computing algorithms for optimization problems',
      status: 'Recruiting',
      students: 1,
      applicants: 8,
      deadline: '2025-06-10',
      skills: ['Quantum Computing', 'Algorithms', 'Physics']
    }
  ];
  
  let myCourses = [
    {
      id: 'c1',
      title: 'Advanced Neural Networks',
      description: 'Deep dive into modern neural network architectures and applications',
      enrolled: 42,
      schedule: 'Mon/Wed 10:00-11:30 AM',
      startDate: '2025-05-01',
      endDate: '2025-07-15',
      status: 'Upcoming'
    },
    {
      id: 'c2',
      title: 'Research Methods in Computer Science',
      description: 'Introduction to research methodologies in computer science',
      enrolled: 28,
      schedule: 'Tue/Thu 2:00-3:30 PM',
      startDate: '2025-05-05',
      endDate: '2025-07-20',
      status: 'Upcoming'
    }
  ];
  
  let resources = [
    {
      id: 'r1',
      title: 'Deep Learning Foundations',
      description: 'Comprehensive guide to understanding the foundations of deep learning',
      type: 'Course Materials',
      downloads: 324,
      lastUpdated: '2025-04-01'
    },
    {
      id: 'r2',
      title: 'Research Paper Template',
      description: 'LaTeX template for student research papers following academic standards',
      type: 'Template',
      downloads: 156,
      lastUpdated: '2025-02-28'
    }
  ];
  
  let applicants = [
    {
      id: 'a1',
      name: 'Emma Johnson',
      university: 'Stanford University',
      major: 'Computer Science',
      year: '3rd Year',
      projectId: 'p1',
      projectTitle: 'AI for Climate Change Prediction',
      appliedDate: '2025-04-10',
      status: 'Pending'
    },
    {
      id: 'a2',
      name: 'Michael Chen',
      university: 'MIT',
      major: 'Physics',
      year: 'Graduate',
      projectId: 'p2',
      projectTitle: 'Quantum Computing Algorithms',
      appliedDate: '2025-04-12',
      status: 'Pending'
    }
  ];
  
  // Handle creating new projects, courses and resources
  function createNewProject() {
    console.log('Create new project');
  }
  
  function createNewCourse() {
    console.log('Create new course');
  }
  
  function uploadNewResource() {
    console.log('Upload new resource');
  }
  
  // Handle application updates
  function updateApplicantStatus(applicant, status) {
    console.log(`Update applicant ${applicant.id} to ${status}`);
  }
  
  onMount(() => {
    console.log('Professor dashboard mounted');
    // In a real app, we would load data based on userProfile.id
    console.log(`Loading data for professor: ${userProfile?.displayName}`);
  });
</script>

<div>
  <!-- Header section with professor info -->
  <div class="mb-8">
    <h1 class="text-2xl font-bold text-gray-900">Welcome, {userProfile?.displayName || 'Professor'}</h1>
    <p class="text-gray-600">{userProfile?.institution || 'Your Institution'}</p>
  </div>

  <!-- Projects Section -->
  {#if $activeSection === 'projects'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">My Research Projects</h2>
        <button 
          on:click={createNewProject}
          class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New Project
        </button>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
        {#each myProjects as project}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{project.title}</h3>
                <span class="bg-blue-100 text-blue-800 text-xs px-2.5 py-0.5 rounded">{project.status}</span>
              </div>
              <p class="mt-2 text-gray-700">{project.description}</p>
              
              <div class="mt-4 flex flex-wrap gap-1">
                {#each project.skills as skill}
                  <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded">{skill}</span>
                {/each}
              </div>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="flex space-x-4 text-sm text-gray-500">
                  <span>Students: {project.students}</span>
                  <span>Applicants: {project.applicants}</span>
                  <span>Deadline: {new Date(project.deadline).toLocaleDateString()}</span>
                </div>
                <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                  Edit
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
      
      {#if applicants.length > 0}
        <div class="mt-8">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Project Applicants</h3>
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Student
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Project
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Applied Date
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {#each applicants as applicant}
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div>
                          <div class="text-sm font-medium text-gray-900">
                            {applicant.name}
                          </div>
                          <div class="text-sm text-gray-500">
                            {applicant.university} • {applicant.major} • {applicant.year}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">{applicant.projectTitle}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">{new Date(applicant.appliedDate).toLocaleDateString()}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                        {applicant.status}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div class="flex space-x-2">
                        <button 
                          on:click={() => updateApplicantStatus(applicant, 'Approved')}
                          class="text-green-600 hover:text-green-900"
                        >
                          Accept
                        </button>
                        <button 
                          on:click={() => updateApplicantStatus(applicant, 'Rejected')}
                          class="text-red-600 hover:text-red-900"
                        >
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {/if}
    </div>
  {/if}
  
  <!-- Courses Section -->
  {#if $activeSection === 'courses'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">My Courses</h2>
        <button 
          on:click={createNewCourse}
          class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          New Course
        </button>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
        {#each myCourses as course}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{course.title}</h3>
                <span class="bg-purple-100 text-purple-800 text-xs px-2.5 py-0.5 rounded">{course.status}</span>
              </div>
              <p class="mt-2 text-gray-700">{course.description}</p>
              
              <div class="mt-4 pt-4 border-t border-gray-100">
                <div class="grid grid-cols-2 gap-4 text-sm text-gray-500">
                  <div>
                    <span class="block font-medium text-gray-700">Schedule</span>
                    <span>{course.schedule}</span>
                  </div>
                  <div>
                    <span class="block font-medium text-gray-700">Enrolled</span>
                    <span>{course.enrolled} students</span>
                  </div>
                  <div>
                    <span class="block font-medium text-gray-700">Start Date</span>
                    <span>{new Date(course.startDate).toLocaleDateString()}</span>
                  </div>
                  <div>
                    <span class="block font-medium text-gray-700">End Date</span>
                    <span>{new Date(course.endDate).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div class="mt-4 flex justify-end space-x-2">
                  <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                    View Students
                  </button>
                  <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                    Edit
                  </button>
                </div>
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
        <h2 class="text-2xl font-bold text-gray-900">My Resources</h2>
        <button 
          on:click={uploadNewResource}
          class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload Resource
        </button>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
        {#each resources as resource}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{resource.title}</h3>
                <span class="bg-green-100 text-green-800 text-xs px-2.5 py-0.5 rounded">{resource.type}</span>
              </div>
              <p class="mt-2 text-gray-700">{resource.description}</p>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="flex space-x-4 text-sm text-gray-500">
                  <span>Downloads: {resource.downloads}</span>
                  <span>Last Updated: {new Date(resource.lastUpdated).toLocaleDateString()}</span>
                </div>
                <div class="flex space-x-2">
                  <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                    Edit
                  </button>
                  <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                    Analytics
                  </button>
                </div>
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
        <h2 class="text-2xl font-bold text-gray-900">Talent Pool</h2>
        <div class="flex gap-2">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
        </div>
      </div>
      
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="mb-4">
          <label for="student-search" class="block text-sm font-medium text-gray-700 mb-1">Search for Students</label>
          <div class="flex gap-2">
            <input
              id="student-search"
              type="text"
              placeholder="Search by major, skill or university..."
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            <button class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
              Search
            </button>
          </div>
        </div>
        
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex flex-col items-center mb-3">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-md font-semibold">David Wilson</h3>
              <p class="text-sm text-gray-500">Stanford University • Computer Science</p>
            </div>
            
            <div class="text-sm">
              <p class="mb-2 font-medium">Skills:</p>
              <div class="flex flex-wrap gap-1 mb-3">
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Machine Learning</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Python</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">NLP</span>
              </div>
            </div>
            
            <button class="w-full px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
              View Profile
            </button>
          </div>
          
          <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex flex-col items-center mb-3">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-md font-semibold">Emily Johnson</h3>
              <p class="text-sm text-gray-500">MIT • Physics</p>
            </div>
            
            <div class="text-sm">
              <p class="mb-2 font-medium">Skills:</p>
              <div class="flex flex-wrap gap-1 mb-3">
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Quantum Computing</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Matlab</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Research</span>
              </div>
            </div>
            
            <button class="w-full px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
              View Profile
            </button>
          </div>
          
          <div class="border border-gray-200 rounded-lg p-4">
            <div class="flex flex-col items-center mb-3">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 class="text-md font-semibold">Alex Rodriguez</h3>
              <p class="text-sm text-gray-500">UC Berkeley • Data Science</p>
            </div>
            
            <div class="text-sm">
              <p class="mb-2 font-medium">Skills:</p>
              <div class="flex flex-wrap gap-1 mb-3">
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Data Analysis</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">R</span>
                <span class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded">Statistics</span>
              </div>
            </div>
            
            <button class="w-full px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
              View Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>