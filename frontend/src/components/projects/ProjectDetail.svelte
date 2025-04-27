<script>
  import { onMount } from 'svelte';
  import { user } from '../../lib/stores/authStore';
  import { initializeFirebase } from '../../lib/firebase/firebase';
  import { doc, getDoc, updateDoc, collection, query, where, getDocs } from 'firebase/firestore';
  import { createChatRoom } from '../../lib/firebase/realtimeDb';
  import ProjectCollaboration from './ProjectCollaboration.svelte';

  export let projectId;
  
  let project = null;
  let loading = true;
  let error = '';
  let editing = false;
  let participants = [];
  
  // Editable fields
  let title = '';
  let description = '';
  let requirements = '';
  let deadline = '';
  let maxParticipants = 0;
  
  // Check if the current user is the owner
  $: isOwner = project && $user && project.createdBy === $user.uid;
  
  // Check if the current user is a participant
  $: isParticipant = project && $user && 
    (project.participants && project.participants.includes($user.uid));

  // Load project data
  async function loadProject() {
    loading = true;
    error = '';
    
    try {
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not initialized');
      
      const docRef = doc(db, 'projects', projectId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        project = { id: docSnap.id, ...docSnap.data() };
        
        // Set editable fields
        title = project.title || '';
        description = project.description || '';
        requirements = project.requirements || '';
        deadline = project.deadline ? new Date(project.deadline).toISOString().split('T')[0] : '';
        maxParticipants = project.maxParticipants || 5;
        
        // Load participants data
        if (project.participants && project.participants.length > 0) {
          await loadParticipants(project.participants);
        }
      } else {
        error = 'Project not found';
      }
    } catch (err) {
      console.error('Error loading project:', err);
      error = err.message || 'An error occurred while loading the project';
    } finally {
      loading = false;
    }
  }
  
  // Load participants data
  async function loadParticipants(participantIds) {
    try {
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not initialized');
      
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
      
      participants = participantsData;
    } catch (err) {
      console.error('Error loading participants:', err);
    }
  }
  
  // Save project changes
  async function saveChanges() {
    if (!isOwner) return;
    
    try {
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not initialized');
      
      const docRef = doc(db, 'projects', projectId);
      
      await updateDoc(docRef, {
        title,
        description,
        requirements,
        deadline: deadline ? new Date(deadline).toISOString() : null,
        maxParticipants: parseInt(maxParticipants) || 5,
        updatedAt: new Date().toISOString()
      });
      
      // Refresh project data
      await loadProject();
      editing = false;
    } catch (err) {
      console.error('Error saving project:', err);
      error = err.message || 'An error occurred while saving the project';
    }
  }
  
  // Join project
  async function joinProject() {
    if (!$user || isParticipant) return;
    
    try {
      const { db } = await initializeFirebase();
      if (!db) throw new Error('Database not initialized');
      
      const docRef = doc(db, 'projects', projectId);
      
      // Check if maximum participants reached
      if (project.participants && project.participants.length >= project.maxParticipants) {
        error = 'This project has reached the maximum number of participants';
        return;
      }
      
      // Add user to participants array
      const updatedParticipants = [...(project.participants || []), $user.uid];
      
      await updateDoc(docRef, {
        participants: updatedParticipants,
        updatedAt: new Date().toISOString()
      });
      
      // Refresh project data
      await loadProject();
    } catch (err) {
      console.error('Error joining project:', err);
      error = err.message || 'An error occurred while joining the project';
    }
  }

  // Create project chat room
  async function createProjectChat() {
    if (!$user || !isParticipant) return;
    
    try {
      // Use all participants as chat members
      const result = await createChatRoom(
        `Project: ${project.title}`,
        'project',
        $user.uid,
        project.participants
      );
      
      if (result.success) {
        // Redirect to chat (implement as needed)
        alert('Project chat room created! Check your messages.');
      } else {
        error = result.error || 'Failed to create chat room';
      }
    } catch (err) {
      console.error('Error creating project chat:', err);
      error = err.message || 'An error occurred';
    }
  }
  
  // Initialize
  onMount(() => {
    if (projectId) {
      loadProject();
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
  {:else if project}
    <!-- Project Header -->
    <div class="bg-blue-700 text-white p-6">
      {#if editing}
        <input
          type="text"
          bind:value={title}
          class="w-full p-2 text-xl font-bold bg-blue-600 text-white border border-blue-400 rounded mb-2 focus:outline-none"
          placeholder="Project Title"
        />
      {:else}
        <h1 class="text-2xl font-bold">{project.title}</h1>
      {/if}
      
      <div class="flex items-center mt-2 text-blue-100">
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-sm">
            {project.createdAt ? new Date(project.createdAt).toLocaleDateString() : 'Unknown date'}
          </span>
        </div>
        
        <div class="mx-3">•</div>
        
        <div class="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="text-sm">
            {project.creatorName || 'Unknown'}
          </span>
        </div>
        
        {#if project.deadline}
          <div class="mx-3">•</div>
          
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span class="text-sm">
              Due: {new Date(project.deadline).toLocaleDateString()}
            </span>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="flex flex-col md:flex-row">
      <!-- Left Side: Project Details -->
      <div class="flex-1 p-6 border-b md:border-b-0 md:border-r">
        {#if editing}
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              bind:value={description}
              rows="6"
              class="w-full p-2 border rounded"
              placeholder="Project description"
            ></textarea>
          </div>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Requirements</label>
            <textarea
              bind:value={requirements}
              rows="4"
              class="w-full p-2 border rounded"
              placeholder="Project requirements"
            ></textarea>
          </div>
          
          <div class="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Deadline</label>
              <input
                type="date"
                bind:value={deadline}
                class="w-full p-2 border rounded"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Max Participants</label>
              <input
                type="number"
                bind:value={maxParticipants}
                min="1"
                max="20"
                class="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          <div class="flex space-x-3 mt-6">
            <button
              on:click={saveChanges}
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Save Changes
            </button>
            
            <button
              on:click={() => editing = false}
              class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        {:else}
          <div class="prose max-w-none">
            <h3>Description</h3>
            <div class="mb-6">
              {#if project.description}
                <p>{project.description}</p>
              {:else}
                <p class="text-gray-500 italic">No description provided</p>
              {/if}
            </div>
            
            <h3>Requirements</h3>
            <div class="mb-6">
              {#if project.requirements}
                <p>{project.requirements}</p>
              {:else}
                <p class="text-gray-500 italic">No specific requirements</p>
              {/if}
            </div>
            
            <div class="flex space-x-4">
              {#if isOwner}
                <button
                  on:click={() => editing = true}
                  class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Edit Project
                </button>
              {/if}
              
              {#if !isParticipant && $user}
                <button
                  on:click={joinProject}
                  class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Join Project
                </button>
              {:else if isParticipant}
                <button
                  on:click={createProjectChat}
                  class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
                >
                  Create Project Chat
                </button>
              {/if}
            </div>
          </div>
        {/if}
      </div>
      
      <!-- Right Side: Participants & Collaboration -->
      <div class="w-full md:w-80 p-6">
        <!-- Participants Section -->
        <div class="mb-6">
          <h3 class="text-lg font-medium mb-3">Participants ({participants.length}/{project.maxParticipants || 5})</h3>
          
          {#if participants.length === 0}
            <p class="text-gray-500 text-sm">No participants yet</p>
          {:else}
            <div class="space-y-3">
              {#each participants as participant}
                <div class="flex items-center">
                  <img
                    src={participant.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(participant.displayName || 'User')}`}
                    alt={participant.displayName}
                    class="w-8 h-8 rounded-full mr-2"
                  />
                  <div>
                    <div class="font-medium">{participant.displayName || 'Anonymous'}</div>
                    <div class="text-xs text-gray-500 capitalize">{participant.userType || 'User'}</div>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
        
        <!-- Real-time Collaboration Section -->
        {#if isParticipant}
          <ProjectCollaboration 
            projectId={project.id} 
            projectName={project.title}
            isEditable={true}
          />
        {/if}
      </div>
    </div>
  {:else}
    <div class="p-6 text-center">
      <p class="text-gray-500">Project not found</p>
    </div>
  {/if}
</div>