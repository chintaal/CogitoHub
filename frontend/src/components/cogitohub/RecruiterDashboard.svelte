<script>
  import { onMount } from 'svelte';
  
  export let activeSection;
  export let userProfile;
  
  // Mock data for recruiter dashboard
  let opportunities = [
    {
      id: 'j1',
      title: 'Machine Learning Research Intern',
      company: 'Tech Innovations Inc.',
      type: 'Research Internship',
      location: 'San Francisco, CA',
      mode: 'Hybrid',
      compensation: 'Paid',
      duration: '6 months',
      deadline: '2025-06-15',
      applicants: 24,
      status: 'Active',
      requirements: ['Machine Learning', 'Python', 'Research'],
      description: 'Looking for exceptional students to join our ML research team focused on developing cutting-edge AI solutions.'
    },
    {
      id: 'j2',
      title: 'Software Development Engineer',
      company: 'Tech Innovations Inc.',
      type: 'Full-time',
      location: 'Remote',
      mode: 'Remote',
      compensation: 'Competitive',
      deadline: '2025-07-01',
      applicants: 45,
      status: 'Active',
      requirements: ['Full Stack', 'React', 'Node.js'],
      description: 'Seeking talented software engineers to help build next-generation web applications.'
    }
  ];
  
  let applications = [
    {
      id: 'a1',
      candidateName: 'Emma Thompson',
      university: 'Stanford University',
      major: 'Computer Science',
      year: '4th Year',
      position: 'Machine Learning Research Intern',
      appliedDate: '2025-04-15',
      status: 'Under Review'
    },
    {
      id: 'a2',
      candidateName: 'James Wilson',
      university: 'MIT',
      major: 'Electrical Engineering',
      year: 'Graduate',
      position: 'Software Development Engineer',
      appliedDate: '2025-04-16',
      status: 'Under Review'
    }
  ];
  
  let metrics = {
    totalOpportunities: 5,
    activeOpportunities: 2,
    totalApplications: 69,
    newApplications: 12,
    shortlisted: 8,
    hired: 3,
    averageTimeToHire: '21 days',
    topUniversities: [
      { name: 'Stanford University', applicants: 15 },
      { name: 'MIT', applicants: 12 },
      { name: 'UC Berkeley', applicants: 10 }
    ],
    popularSkills: [
      { name: 'Machine Learning', count: 28 },
      { name: 'Python', count: 35 },
      { name: 'React', count: 22 }
    ]
  };
  
  let messages = [
    {
      id: 'm1',
      from: 'Emma Thompson',
      subject: 'Follow-up Question: ML Research Position',
      preview: 'I had a few questions about the research project...',
      timestamp: '2025-04-16T10:30:00',
      unread: true
    },
    {
      id: 'm2',
      from: 'James Wilson',
      subject: 'Interview Scheduling',
      preview: 'Thank you for considering my application...',
      timestamp: '2025-04-16T09:15:00',
      unread: false
    }
  ];
  
  // Handle interactions
  function postNewOpportunity() {
    console.log('Post new opportunity');
  }
  
  function updateApplicationStatus(application, status) {
    console.log(`Update application ${application.id} to ${status}`);
  }
  
  function searchTalent() {
    console.log('Search talent');
  }
  
  onMount(() => {
    console.log('Recruiter dashboard mounted');
    // In a real app, we would load data based on userProfile.id
    console.log(`Loading data for recruiter: ${userProfile?.displayName} at ${userProfile?.company}`);
  });
</script>

<div>
  <!-- Header section with recruiter info -->
  <div class="mb-8">
    <h1 class="text-2xl font-bold text-gray-900">Welcome, {userProfile?.displayName || 'Recruiter'}</h1>
    <p class="text-gray-600">{userProfile?.company || 'Your Company'}</p>
  </div>

  <!-- Opportunities Section -->
  {#if $activeSection === 'opportunities'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Posted Opportunities</h2>
        <button 
          on:click={postNewOpportunity}
          class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Post Opportunity
        </button>
      </div>
      
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
        {#each opportunities as opportunity}
          <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{opportunity.title}</h3>
                <span class="bg-green-100 text-green-800 text-xs px-2.5 py-0.5 rounded">{opportunity.status}</span>
              </div>
              <p class="text-gray-600 text-sm">{opportunity.company} • {opportunity.location} • {opportunity.mode}</p>
              <p class="mt-2 text-gray-700">{opportunity.description}</p>
              
              <div class="mt-4 flex flex-wrap gap-1">
                {#each opportunity.requirements as skill}
                  <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded">{skill}</span>
                {/each}
              </div>
              
              <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                <div class="flex space-x-4 text-sm text-gray-500">
                  <span>Applicants: {opportunity.applicants}</span>
                  <span>Deadline: {new Date(opportunity.deadline).toLocaleDateString()}</span>
                </div>
                <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-md hover:bg-gray-200 transition-colors">
                  View Applicants
                </button>
              </div>
            </div>
          </div>
        {/each}
        
        {#if applications.length > 0}
          <div class="col-span-full mt-8">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Applications</h3>
            <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Candidate
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Position
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
                  {#each applications as application}
                    <tr>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div>
                            <div class="text-sm font-medium text-gray-900">
                              {application.candidateName}
                            </div>
                            <div class="text-sm text-gray-500">
                              {application.university} • {application.major} • {application.year}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{application.position}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{new Date(application.appliedDate).toLocaleDateString()}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                          {application.status}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button 
                            on:click={() => updateApplicationStatus(application, 'Shortlisted')}
                            class="text-blue-600 hover:text-blue-900"
                          >
                            Shortlist
                          </button>
                          <button 
                            on:click={() => updateApplicationStatus(application, 'Rejected')}
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
    </div>
  {/if}
  
  <!-- Talent Search Section -->
  {#if $activeSection === 'talent'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Find Talent</h2>
      </div>
      
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="mb-4">
          <label for="candidate-search" class="block text-sm font-medium text-gray-700 mb-1">Search Candidates</label>
          <div class="flex gap-2">
            <input
              id="candidate-search"
              type="text"
              placeholder="Search by skills, university, or major..."
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            <button 
              on:click={searchTalent}
              class="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors"
            >
              Search
            </button>
          </div>
        </div>
        
        <div class="flex gap-2 mb-4">
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Filter
          </button>
          <button class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Sort
          </button>
        </div>
        
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {#each metrics.topUniversities as university}
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex flex-col items-center mb-3">
                <h3 class="text-md font-semibold">{university.name}</h3>
                <p class="text-sm text-gray-500">{university.applicants} Candidates</p>
              </div>
              
              <div class="mt-4">
                <button class="w-full px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors">
                  View Candidates
                </button>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Analytics Section -->
  {#if $activeSection === 'analytics'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Recruitment Analytics</h2>
      </div>
      
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-sm font-medium text-gray-500">Total Applications</h3>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{metrics.totalApplications}</p>
          <p class="text-sm text-green-600">+{metrics.newApplications} new</p>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-sm font-medium text-gray-500">Shortlisted</h3>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{metrics.shortlisted}</p>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-sm font-medium text-gray-500">Hired</h3>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{metrics.hired}</p>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-sm font-medium text-gray-500">Time to Hire</h3>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{metrics.averageTimeToHire}</p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Top Skills</h3>
          <div class="space-y-2">
            {#each metrics.popularSkills as skill}
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">{skill.name}</span>
                <span class="text-sm font-medium text-gray-900">{skill.count} candidates</span>
              </div>
            {/each}
          </div>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Top Universities</h3>
          <div class="space-y-2">
            {#each metrics.topUniversities as university}
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">{university.name}</span>
                <span class="text-sm font-medium text-gray-900">{university.applicants} applicants</span>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Messages Section -->
  {#if $activeSection === 'messages'}
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Messages</h2>
      </div>
      
      <div class="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
        {#each messages as message}
          <div class="p-4 hover:bg-gray-50 transition-colors cursor-pointer">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium text-gray-900">
                {message.from}
                {#if message.unread}
                  <span class="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    New
                  </span>
                {/if}
              </h3>
              <span class="text-sm text-gray-500">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <p class="text-sm font-medium text-gray-900 mt-1">{message.subject}</p>
            <p class="text-sm text-gray-600 mt-1">{message.preview}</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>