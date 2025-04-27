<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  // Track selected user type and additional info
  let selectedUserType = null;
  let additionalInfo = {};
  
  // Universities and companies for dropdowns
  const universities = [
    'Stanford University',
    'MIT',
    'Harvard University',
    'UC Berkeley',
    'Princeton University',
    'Yale University',
    'Other'
  ];
  
  const companies = [
    'Google',
    'Microsoft',
    'Apple',
    'Amazon',
    'Meta',
    'IBM',
    'Other'
  ];
  
  // Validation state
  let validationErrors = {};
  let submitAttempted = false;

  function validateForm() {
    validationErrors = {};
    
    if (selectedUserType === 'student') {
      if (!additionalInfo.university) validationErrors.university = 'Please select your university';
      if (!additionalInfo.major) validationErrors.major = 'Please enter your field of study';
      if (!additionalInfo.year) validationErrors.year = 'Please select your year of study';
    } else if (selectedUserType === 'professor') {
      if (!additionalInfo.university) validationErrors.university = 'Please select your university';
      if (!additionalInfo.department) validationErrors.department = 'Please enter your department';
      if (!additionalInfo.title) validationErrors.title = 'Please select your title';
    } else if (selectedUserType === 'recruiter') {
      if (!additionalInfo.company) validationErrors.company = 'Please select your company';
      if (!additionalInfo.role) validationErrors.role = 'Please enter your role';
      if (!additionalInfo.hiringFor) validationErrors.hiringFor = 'Please select what you\'re hiring for';
    }
    
    return Object.keys(validationErrors).length === 0;
  }

  function handleSubmit() {
    submitAttempted = true;
    
    if (!selectedUserType) {
      return;
    }
    
    if (!validateForm()) {
      return;
    }
    
    try {
      dispatch('userTypeSelected', {
        userType: selectedUserType,
        additionalInfo
      });
    } catch (error) {
      console.error('Error dispatching user type selection:', error);
      // Add error message to UI if needed
    }
  }

  function selectUserType(type) {
    selectedUserType = type;
    additionalInfo = {}; // Reset when changing user type
    validationErrors = {}; // Reset validation errors
    submitAttempted = false; // Reset submission attempt
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-white to-gray-100">
  <div class="max-w-2xl w-full bg-white rounded-lg shadow-xl overflow-hidden">
    <div class="p-8">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Welcome to CogitoHub!</h1>
        <p class="text-gray-600">Let's customize your experience. Which of the following best describes you?</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <!-- Student Option -->
        <button
          class="flex flex-col items-center p-6 border-2 rounded-lg transition-all {selectedUserType === 'student' ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-200'}"
          on:click={() => selectUserType('student')}
        >
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14v7" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900">Student</h3>
          <p class="text-sm text-gray-500 text-center mt-2">Explore projects, courses, and opportunities</p>
        </button>
        
        <!-- Professor Option -->
        <button
          class="flex flex-col items-center p-6 border-2 rounded-lg transition-all {selectedUserType === 'professor' ? 'border-purple-600 bg-purple-50' : 'border-gray-200 hover:border-purple-200'}"
          on:click={() => selectUserType('professor')}
        >
          <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900">Professor</h3>
          <p class="text-sm text-gray-500 text-center mt-2">Share knowledge and research opportunities</p>
        </button>
        
        <!-- Recruiter Option -->
        <button
          class="flex flex-col items-center p-6 border-2 rounded-lg transition-all {selectedUserType === 'recruiter' ? 'border-green-600 bg-green-50' : 'border-gray-200 hover:border-green-200'}"
          on:click={() => selectUserType('recruiter')}
        >
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900">Recruiter</h3>
          <p class="text-sm text-gray-500 text-center mt-2">Find talent and post opportunities</p>
        </button>
      </div>
      
      <!-- Additional Information based on user type -->
      {#if selectedUserType === 'student'}
        <div class="space-y-4 mb-8">
          <h2 class="text-lg font-medium text-gray-900">Tell us a bit more about yourself</h2>
          
          <div>
            <label for="university" class="block text-sm font-medium text-gray-700 mb-1">University</label>
            <select 
              id="university" 
              bind:value={additionalInfo.university}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select your university</option>
              {#each universities as university}
                <option value={university}>{university}</option>
              {/each}
            </select>
            {#if submitAttempted && validationErrors.university}
              <p class="text-red-600 text-sm mt-1">{validationErrors.university}</p>
            {/if}
          </div>
          
          <div>
            <label for="major" class="block text-sm font-medium text-gray-700 mb-1">Major / Field of Study</label>
            <input 
              type="text" 
              id="major" 
              bind:value={additionalInfo.major}
              placeholder="e.g. Computer Science, Physics, etc." 
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            {#if submitAttempted && validationErrors.major}
              <p class="text-red-600 text-sm mt-1">{validationErrors.major}</p>
            {/if}
          </div>
          
          <div>
            <label for="year" class="block text-sm font-medium text-gray-700 mb-1">Year of Study</label>
            <select 
              id="year" 
              bind:value={additionalInfo.year}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select your year</option>
              <option value="1st Year">1st Year</option>
              <option value="2nd Year">2nd Year</option>
              <option value="3rd Year">3rd Year</option>
              <option value="4th Year">4th Year</option>
              <option value="5th Year">5th Year</option>
              <option value="Graduate">Graduate Student</option>
            </select>
            {#if submitAttempted && validationErrors.year}
              <p class="text-red-600 text-sm mt-1">{validationErrors.year}</p>
            {/if}
          </div>
        </div>
      {:else if selectedUserType === 'professor'}
        <div class="space-y-4 mb-8">
          <h2 class="text-lg font-medium text-gray-900">Tell us a bit more about yourself</h2>
          
          <div>
            <label for="university" class="block text-sm font-medium text-gray-700 mb-1">University / Institution</label>
            <select 
              id="university" 
              bind:value={additionalInfo.university}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select your university</option>
              {#each universities as university}
                <option value={university}>{university}</option>
              {/each}
            </select>
            {#if submitAttempted && validationErrors.university}
              <p class="text-red-600 text-sm mt-1">{validationErrors.university}</p>
            {/if}
          </div>
          
          <div>
            <label for="department" class="block text-sm font-medium text-gray-700 mb-1">Department</label>
            <input 
              type="text" 
              id="department" 
              bind:value={additionalInfo.department}
              placeholder="e.g. Computer Science, Physics, etc." 
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            {#if submitAttempted && validationErrors.department}
              <p class="text-red-600 text-sm mt-1">{validationErrors.department}</p>
            {/if}
          </div>
          
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Academic Title</label>
            <select 
              id="title" 
              bind:value={additionalInfo.title}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select your title</option>
              <option value="Assistant Professor">Assistant Professor</option>
              <option value="Associate Professor">Associate Professor</option>
              <option value="Professor">Professor</option>
              <option value="Lecturer">Lecturer</option>
              <option value="Researcher">Researcher</option>
              <option value="Other">Other</option>
            </select>
            {#if submitAttempted && validationErrors.title}
              <p class="text-red-600 text-sm mt-1">{validationErrors.title}</p>
            {/if}
          </div>
        </div>
      {:else if selectedUserType === 'recruiter'}
        <div class="space-y-4 mb-8">
          <h2 class="text-lg font-medium text-gray-900">Tell us a bit more about yourself</h2>
          
          <div>
            <label for="company" class="block text-sm font-medium text-gray-700 mb-1">Company / Organization</label>
            <select 
              id="company" 
              bind:value={additionalInfo.company}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select your company</option>
              {#each companies as company}
                <option value={company}>{company}</option>
              {/each}
            </select>
            {#if submitAttempted && validationErrors.company}
              <p class="text-red-600 text-sm mt-1">{validationErrors.company}</p>
            {/if}
          </div>
          
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700 mb-1">Your Role</label>
            <input 
              type="text" 
              id="role" 
              bind:value={additionalInfo.role}
              placeholder="e.g. Technical Recruiter, HR Manager, etc." 
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            {#if submitAttempted && validationErrors.role}
              <p class="text-red-600 text-sm mt-1">{validationErrors.role}</p>
            {/if}
          </div>
          
          <div>
            <label for="hiringFor" class="block text-sm font-medium text-gray-700 mb-1">Looking to hire for</label>
            <select 
              id="hiringFor" 
              bind:value={additionalInfo.hiringFor}
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select option</option>
              <option value="Internships">Internships</option>
              <option value="Full-time Positions">Full-time Positions</option>
              <option value="Research Collaboration">Research Collaboration</option>
              <option value="Project-based Work">Project-based Work</option>
              <option value="Multiple Types">Multiple Types</option>
            </select>
            {#if submitAttempted && validationErrors.hiringFor}
              <p class="text-red-600 text-sm mt-1">{validationErrors.hiringFor}</p>
            {/if}
          </div>
        </div>
      {/if}
      
      <!-- Submit button -->
      <div class="flex justify-end">
        <button
          class="px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={!selectedUserType || (selectedUserType && Object.keys(additionalInfo).length === 0)}
          on:click={handleSubmit}
        >
          Get Started
        </button>
      </div>
    </div>
  </div>
</div>