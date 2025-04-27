<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import { user, getUserProfile } from '../../lib/stores/authStore';
  import { initializeFirebase } from '../../lib/firebase/firebase';
  import { doc, getDoc, collection, query, where, getDocs } from 'firebase/firestore';
  import { createChatRoom } from '../../lib/firebase/realtimeDb';
  import CourseActivity from './CourseActivity.svelte';

  export let courseId;
  
  let course = null;
  let loading = true;
  let error = '';
  let materials = [];
  let assignments = [];
  let announcements = [];
  let students = [];
  let instructors = [];
  
  const currentSection = writable('overview');
  
  // Check if the current user is an instructor
  $: isInstructor = course && $user && 
    (course.instructors && course.instructors.includes($user.uid));
    
  // Check if the current user is enrolled
  $: isEnrolled = course && $user && 
    (course.students && course.students.includes($user.uid));
    
  // Current user type (for activity tracking)
  $: userType = isInstructor ? 'professor' : 'student';
  
  // Load course data
  async function loadCourse() {
    loading = true;
    error = '';
    
    try {
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not initialized');
      
      const docRef = doc(db, 'courses', courseId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        course = { id: docSnap.id, ...docSnap.data() };
        
        // Load course materials
        await loadMaterials();
        
        // Load course assignments
        await loadAssignments();
        
        // Load announcements
        await loadAnnouncements();
        
        // Load students and instructors
        if (course.students && course.students.length > 0) {
          await loadParticipants(course.students, 'students');
        }
        
        if (course.instructors && course.instructors.length > 0) {
          await loadParticipants(course.instructors, 'instructors');
        }
      } else {
        error = 'Course not found';
      }
    } catch (err) {
      console.error('Error loading course:', err);
      error = err.message || 'An error occurred while loading the course';
    } finally {
      loading = false;
    }
  }
  
  // Load course materials
  async function loadMaterials() {
    try {
      const { db } = await initializeFirebase();
      if (!db) return;
      
      const materialsQuery = query(
        collection(db, 'courseMaterials'),
        where('courseId', '==', courseId)
      );
      
      const querySnapshot = await getDocs(materialsQuery);
      materials = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (err) {
      console.error('Error loading materials:', err);
    }
  }
  
  // Load course assignments
  async function loadAssignments() {
    try {
      const { db } = await initializeFirebase();
      if (!db) return;
      
      const assignmentsQuery = query(
        collection(db, 'assignments'),
        where('courseId', '==', courseId)
      );
      
      const querySnapshot = await getDocs(assignmentsQuery);
      assignments = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      
      // Sort by due date (most recent first)
      assignments.sort((a, b) => {
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return new Date(a.dueDate) - new Date(b.dueDate);
      });
    } catch (err) {
      console.error('Error loading assignments:', err);
    }
  }
  
  // Load course announcements
  async function loadAnnouncements() {
    try {
      const { db } = await initializeFirebase();
      if (!db) return;
      
      const announcementsQuery = query(
        collection(db, 'announcements'),
        where('courseId', '==', courseId)
      );
      
      const querySnapshot = await getDocs(announcementsQuery);
      announcements = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      
      // Sort by date (newest first)
      announcements.sort((a, b) => {
        if (!a.createdAt) return 1;
        if (!b.createdAt) return -1;
        return new Date(b.createdAt) - new Date(a.createdAt);
      });
    } catch (err) {
      console.error('Error loading announcements:', err);
    }
  }
  
  // Load participants data
  async function loadParticipants(participantIds, type) {
    try {
      const { db } = await initializeFirebase();
      if (!db) return;
      
      const participantsData = [];
      
      for (const uid of participantIds) {
        const userRef = doc(db, 'users', uid);
        const userSnap = await getDoc(userRef);
        
        if (userSnap.exists()) {
          participantsData.push({
            uid,
            ...userSnap.data()
          });
        }
      }
      
      if (type === 'students') {
        students = participantsData;
      } else if (type === 'instructors') {
        instructors = participantsData;
      }
    } catch (err) {
      console.error(`Error loading ${type}:`, err);
    }
  }
  
  // Create course chat room
  async function createCourseChat() {
    if (!$user || (!isEnrolled && !isInstructor)) return;
    
    try {
      // Include all students and instructors
      const participants = [...(course.students || []), ...(course.instructors || [])];
      
      const result = await createChatRoom(
        `Course: ${course.title}`,
        'class',
        $user.uid,
        participants
      );
      
      if (result.success) {
        // Redirect to chat (implement as needed)
        alert('Course chat room created! Check your messages.');
      } else {
        error = result.error || 'Failed to create chat room';
      }
    } catch (err) {
      console.error('Error creating course chat:', err);
      error = err.message || 'An error occurred';
    }
  }
  
  // Format date for display
  function formatDate(dateStr) {
    if (!dateStr) return 'No date';
    
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
  
  // Handle section changes
  function changeSection(section) {
    currentSection.set(section);
  }
  
  // Initialize
  onMount(() => {
    if (courseId) {
      loadCourse();
    }
  });
</script>

<div class="bg-white rounded-lg shadow overflow-hidden">
  {#if loading}
    <div class="p-6 flex justify-center">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>
  {:else if error}
    <div class="p-6">
      <div class="bg-red-50 text-red-700 p-4 rounded">
        {error}
      </div>
    </div>
  {:else if course}
    <!-- Course Header -->
    <div class="bg-blue-600 text-white p-6">
      <h1 class="text-2xl font-bold">{course.title}</h1>
      <p class="mt-1 text-blue-100">{course.department || ''} • {course.courseCode || ''}</p>
      
      <div class="flex items-center mt-4 text-blue-100">
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="text-sm">
            {instructors.length > 0 
              ? `${instructors[0].displayName}${instructors.length > 1 ? ' +' + (instructors.length - 1) : ''}` 
              : 'Unknown instructor'}
          </span>
        </div>
        
        <div class="mx-3">•</div>
        
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <span class="text-sm">
            {students.length} student{students.length !== 1 ? 's' : ''}
          </span>
        </div>
        
        {#if course.term}
          <div class="mx-3">•</div>
          
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span class="text-sm">
              {course.term}
            </span>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Course Navigation -->
    <div class="border-b">
      <nav class="flex">
        <button
          class={`px-4 py-3 font-medium text-sm ${$currentSection === 'overview' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
          on:click={() => changeSection('overview')}
        >
          Overview
        </button>
        <button
          class={`px-4 py-3 font-medium text-sm ${$currentSection === 'materials' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
          on:click={() => changeSection('materials')}
        >
          Materials
        </button>
        <button
          class={`px-4 py-3 font-medium text-sm ${$currentSection === 'assignments' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
          on:click={() => changeSection('assignments')}
        >
          Assignments
        </button>
        <button
          class={`px-4 py-3 font-medium text-sm ${$currentSection === 'discussions' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
          on:click={() => changeSection('discussions')}
        >
          Discussions
        </button>
        
        {#if isInstructor}
          <button
            class={`px-4 py-3 font-medium text-sm ${$currentSection === 'people' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
            on:click={() => changeSection('people')}
          >
            People
          </button>
        {/if}
      </nav>
    </div>
    
    <!-- Main Content Area -->
    <div class="flex flex-col lg:flex-row">
      <div class="flex-1 p-6">
        <!-- Overview Section -->
        {#if $currentSection === 'overview'}
          <div class="mb-6">
            <h2 class="text-xl font-medium mb-4">Course Overview</h2>
            
            {#if course.description}
              <div class="prose max-w-none mb-6">
                <p>{course.description}</p>
              </div>
            {:else}
              <p class="text-gray-500 italic">No course description available.</p>
            {/if}
            
            {#if announcements.length > 0}
              <h3 class="text-lg font-medium mt-8 mb-4">Recent Announcements</h3>
              
              <div class="space-y-4">
                {#each announcements.slice(0, 3) as announcement}
                  <div class="border rounded-lg p-4">
                    <div class="flex items-start">
                      <img
                        src={announcement.authorPhotoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(announcement.authorName || 'Instructor')}`}
                        alt={announcement.authorName}
                        class="w-10 h-10 rounded-full mr-3"
                      />
                      <div class="flex-1">
                        <div class="flex justify-between">
                          <div>
                            <h4 class="font-bold">{announcement.authorName}</h4>
                            <p class="text-xs text-gray-500">
                              {formatDate(announcement.createdAt)}
                            </p>
                          </div>
                        </div>
                        <div class="mt-2 text-sm">
                          <p>{announcement.content}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
            
            {#if assignments.length > 0}
              <h3 class="text-lg font-medium mt-8 mb-4">Upcoming Assignments</h3>
              
              <div class="space-y-2">
                {#each assignments.filter(a => new Date(a.dueDate) > new Date()).slice(0, 3) as assignment}
                  <div class="flex items-center border rounded p-3">
                    <div class="mr-4">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div class="flex-1">
                      <h4 class="font-medium">{assignment.title}</h4>
                      <div class="text-sm text-gray-500">
                        Due {formatDate(assignment.dueDate)}
                      </div>
                    </div>
                    <div class="ml-4">
                      <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                        {assignment.points} pts
                      </span>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
            
            <!-- Call to Action Buttons -->
            <div class="flex mt-8 space-x-4">
              {#if isInstructor}
                <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                  Create Announcement
                </button>
                
                <button class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                  Create Assignment
                </button>
              {/if}
              
              <button 
                on:click={createCourseChat}
                class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
              >
                Create Course Chat
              </button>
            </div>
          </div>
        
        <!-- Materials Section -->
        {:else if $currentSection === 'materials'}
          <div>
            <h2 class="text-xl font-medium mb-6">Course Materials</h2>
            
            {#if materials.length === 0}
              <p class="text-gray-500 italic">No materials available for this course yet.</p>
            {:else}
              <div class="space-y-4">
                {#each materials as material}
                  <div class="flex items-start border rounded p-4">
                    <div class="mr-4">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div class="flex-1">
                      <h4 class="font-medium">{material.title}</h4>
                      <div class="text-sm text-gray-500 mt-1">
                        {material.description || 'No description'}
                      </div>
                      <div class="text-xs text-gray-500 mt-2">
                        Added {formatDate(material.createdAt)}
                      </div>
                    </div>
                    <div class="ml-4">
                      <button class="px-3 py-1 border rounded text-sm">
                        View
                      </button>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
            
            {#if isInstructor}
              <button class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Add Material
              </button>
            {/if}
          </div>
        
        <!-- Assignments Section -->
        {:else if $currentSection === 'assignments'}
          <div>
            <h2 class="text-xl font-medium mb-6">Assignments</h2>
            
            {#if assignments.length === 0}
              <p class="text-gray-500 italic">No assignments available for this course yet.</p>
            {:else}
              <div class="space-y-4">
                {#each assignments as assignment}
                  <div class="border rounded overflow-hidden">
                    <div class="p-4">
                      <div class="flex justify-between items-start">
                        <div>
                          <h4 class="font-medium">{assignment.title}</h4>
                          <div class="text-sm text-gray-500 mt-1">
                            {assignment.description || 'No description'}
                          </div>
                        </div>
                        <span class="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                          {assignment.points} pts
                        </span>
                      </div>
                      
                      <div class="flex items-center mt-3 text-sm">
                        <div class="text-gray-500">
                          {#if new Date(assignment.dueDate) < new Date()}
                            <span class="text-red-600">Due {formatDate(assignment.dueDate)}</span>
                          {:else}
                            Due {formatDate(assignment.dueDate)}
                          {/if}
                        </div>
                        
                        <div class="ml-auto">
                          <button class="px-3 py-1 border rounded text-sm">
                            View Details
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    {#if isInstructor}
                      <div class="bg-gray-50 px-4 py-2 text-xs text-gray-500 flex justify-between">
                        <span>{assignment.submissions || 0} submissions</span>
                        <button class="text-blue-600 hover:underline">Grade</button>
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
            {/if}
            
            {#if isInstructor}
              <button class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Create Assignment
              </button>
            {/if}
          </div>
        
        <!-- Discussions Section -->
        {:else if $currentSection === 'discussions'}
          <div>
            <h2 class="text-xl font-medium mb-6">Discussions</h2>
            
            <p class="text-gray-500 italic">No discussions available for this course yet.</p>
            
            <button class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Start Discussion
            </button>
          </div>
        
        <!-- People Section (Instructors Only) -->
        {:else if $currentSection === 'people' && isInstructor}
          <div>
            <h2 class="text-xl font-medium mb-6">People</h2>
            
            <h3 class="font-medium mb-3">Instructors ({instructors.length})</h3>
            <div class="border rounded mb-6">
              {#each instructors as instructor}
                <div class="flex items-center p-3 border-b last:border-0">
                  <img
                    src={instructor.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(instructor.displayName || 'Instructor')}`}
                    alt={instructor.displayName}
                    class="w-8 h-8 rounded-full mr-3"
                  />
                  <div>
                    <div class="font-medium">{instructor.displayName || 'Anonymous'}</div>
                    <div class="text-xs text-gray-500">{instructor.email}</div>
                  </div>
                </div>
              {/each}
            </div>
            
            <h3 class="font-medium mb-3">Students ({students.length})</h3>
            <div class="border rounded">
              {#if students.length === 0}
                <p class="p-3 text-gray-500 italic">No students enrolled yet.</p>
              {:else}
                {#each students as student}
                  <div class="flex items-center p-3 border-b last:border-0">
                    <img
                      src={student.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(student.displayName || 'Student')}`}
                      alt={student.displayName}
                      class="w-8 h-8 rounded-full mr-3"
                    />
                    <div class="flex-1">
                      <div class="font-medium">{student.displayName || 'Anonymous'}</div>
                      <div class="text-xs text-gray-500">{student.email}</div>
                    </div>
                  </div>
                {/each}
              {/if}
            </div>
            
            <div class="mt-6 space-x-4">
              <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                Invite Students
              </button>
              
              <button class="px-4 py-2 border rounded hover:bg-gray-50">
                Export Roster
              </button>
            </div>
          </div>
        {/if}
      </div>
      
      <!-- Sidebar with Real-time Activity -->
      <div class="w-full lg:w-80 p-6 lg:border-l">
        <CourseActivity 
          {courseId}
          courseTitle={course.title}
          {userType}
          currentSection={$currentSection}
        />
        
        <div class="mt-6 border rounded-lg p-4">
          <h3 class="font-medium mb-3">Course Information</h3>
          
          <div class="space-y-2 text-sm">
            {#if course.courseCode}
              <div>
                <span class="text-gray-500">Course Code:</span>
                <span class="ml-1 text-gray-800">{course.courseCode}</span>
              </div>
            {/if}
            
            {#if course.department}
              <div>
                <span class="text-gray-500">Department:</span>
                <span class="ml-1 text-gray-800">{course.department}</span>
              </div>
            {/if}
            
            {#if course.credits}
              <div>
                <span class="text-gray-500">Credits:</span>
                <span class="ml-1 text-gray-800">{course.credits}</span>
              </div>
            {/if}
            
            {#if course.term}
              <div>
                <span class="text-gray-500">Term:</span>
                <span class="ml-1 text-gray-800">{course.term}</span>
              </div>
            {/if}
            
            {#if course.schedule}
              <div>
                <span class="text-gray-500">Schedule:</span>
                <span class="ml-1 text-gray-800">{course.schedule}</span>
              </div>
            {/if}
            
            {#if course.location}
              <div>
                <span class="text-gray-500">Location:</span>
                <span class="ml-1 text-gray-800">{course.location}</span>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  {:else}
    <div class="p-6 text-center">
      <p class="text-gray-500">Course not found</p>
    </div>
  {/if}
</div>