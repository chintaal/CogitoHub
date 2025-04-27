<script>
  import { onMount } from 'svelte';
  import { user, getUserProfile } from '../../lib/stores/authStore';
  import { 
    getUserChatRooms, 
    createChatRoom,
    onlineUsers
  } from '../../lib/firebase/realtimeDb';
  import ChatRoom from './ChatRoom.svelte';

  // State management
  let loading = true;
  let error = '';
  let chatRooms = [];
  let selectedRoomId = null;
  let selectedRoomName = '';
  let showNewChatForm = false;
  let newChatName = '';
  let newChatType = 'group'; // 'group', 'project', 'class', 'direct'
  let selectedParticipants = [];
  let potentialParticipants = [];
  let searchTerm = '';
  let creating = false;

  // Load chat rooms on mount
  onMount(async () => {
    if ($user) {
      await loadChatRooms();
      await loadPotentialParticipants();
    }
  });

  // Load user's chat rooms
  async function loadChatRooms() {
    loading = true;
    error = '';
    
    try {
      const result = await getUserChatRooms($user.uid);
      
      if (result.success) {
        chatRooms = result.rooms;
        
        // Select the first room if one exists and none is selected
        if (chatRooms.length > 0 && !selectedRoomId) {
          selectRoom(chatRooms[0].id, chatRooms[0].name);
        }
      } else {
        error = result.error || 'Failed to load chat rooms';
      }
    } catch (err) {
      error = err.message || 'An error occurred';
    } finally {
      loading = false;
    }
  }
  
  // Load potential participants for new chats - simple implementation for demo
  async function loadPotentialParticipants() {
    try {
      const userProfile = await getUserProfile($user.uid);
      if (!userProfile) return;
      
      const userType = userProfile.userType || 'student';
      
      // Based on user type, define who they can chat with
      if (userType === 'professor') {
        // Professors can chat with anyone online
        potentialParticipants = Object.entries($onlineUsers).flatMap(([type, users]) => {
          return Object.entries(users).map(([uid, userData]) => ({
            uid,
            displayName: userData.displayName || 'Anonymous',
            photoURL: userData.photoURL || '',
            userType: type.slice(0, -1) // Remove 's' from end (students -> student)
          }));
        });
      } else if (userType === 'student') {
        // Students can chat with professors and other students
        const professors = Object.entries($onlineUsers.professors || {}).map(([uid, userData]) => ({
          uid,
          displayName: userData.displayName || 'Anonymous',
          photoURL: userData.photoURL || '',
          userType: 'professor'
        }));
        
        const students = Object.entries($onlineUsers.students || {}).map(([uid, userData]) => ({
          uid,
          displayName: userData.displayName || 'Anonymous',
          photoURL: userData.photoURL || '',
          userType: 'student'
        })).filter(student => student.uid !== $user.uid); // Exclude self
        
        potentialParticipants = [...professors, ...students];
      } else if (userType === 'recruiter') {
        // Recruiters can chat with professors and students
        const professors = Object.entries($onlineUsers.professors || {}).map(([uid, userData]) => ({
          uid,
          displayName: userData.displayName || 'Anonymous',
          photoURL: userData.photoURL || '',
          userType: 'professor'
        }));
        
        const students = Object.entries($onlineUsers.students || {}).map(([uid, userData]) => ({
          uid,
          displayName: userData.displayName || 'Anonymous',
          photoURL: userData.photoURL || '',
          userType: 'student'
        }));
        
        potentialParticipants = [...professors, ...students];
      }
    } catch (err) {
      console.error('Error loading potential participants:', err);
    }
  }
  
  // Select a chat room
  function selectRoom(roomId, roomName) {
    selectedRoomId = roomId;
    selectedRoomName = roomName;
  }
  
  // Create a new chat room
  async function handleCreateChat() {
    if (!newChatName.trim() || creating) return;
    
    creating = true;
    error = '';
    
    try {
      const result = await createChatRoom(
        newChatName,
        newChatType,
        $user.uid,
        selectedParticipants.map(p => p.uid)
      );
      
      if (result.success) {
        // Reset form and select the new chat
        newChatName = '';
        selectedParticipants = [];
        showNewChatForm = false;
        
        // Reload chat rooms and select the new one
        await loadChatRooms();
        selectRoom(result.roomId, newChatName);
      } else {
        error = result.error || 'Failed to create chat room';
      }
    } catch (err) {
      error = err.message || 'An error occurred';
    } finally {
      creating = false;
    }
  }
  
  // Toggle participant selection
  function toggleParticipant(participant) {
    const index = selectedParticipants.findIndex(p => p.uid === participant.uid);
    
    if (index === -1) {
      selectedParticipants = [...selectedParticipants, participant];
    } else {
      selectedParticipants = [
        ...selectedParticipants.slice(0, index),
        ...selectedParticipants.slice(index + 1)
      ];
    }
  }
  
  // Filter participants by search term
  $: filteredParticipants = searchTerm 
    ? potentialParticipants.filter(p => 
        p.displayName.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : potentialParticipants;
</script>

<div class="flex flex-col h-full bg-white rounded-lg shadow">
  <div class="flex h-full overflow-hidden">
    <!-- Sidebar with chat rooms -->
    <div class="w-72 border-r flex flex-col">
      <!-- Header with create button -->
      <div class="p-4 border-b flex justify-between items-center">
        <h3 class="font-medium">Messages</h3>
        <button 
          on:click={() => showNewChatForm = !showNewChatForm}
          class="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700"
          aria-label="Create new conversation"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>
      
      <!-- Chat room list -->
      <div class="flex-1 overflow-y-auto">
        {#if loading}
          <div class="flex justify-center items-center h-32">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          </div>
        {:else if error}
          <div class="p-4 text-red-600 text-sm">{error}</div>
        {:else if chatRooms.length === 0}
          <div class="p-4 text-gray-500 text-sm text-center">
            No chat rooms yet. Create one to get started!
          </div>
        {:else}
          <div class="divide-y">
            {#each chatRooms as room}
              <button
                class="w-full px-4 py-3 text-left hover:bg-gray-50 flex items-start {selectedRoomId === room.id ? 'bg-blue-50' : ''}"
                on:click={() => selectRoom(room.id, room.name)}
              >
                <div class="flex-1 min-w-0">
                  <div class="flex justify-between">
                    <h4 class="font-medium text-gray-900 truncate">{room.name}</h4>
                    {#if room.lastActivity}
                      <span class="text-xs text-gray-500">
                        {new Date(room.lastActivity).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </span>
                    {/if}
                  </div>
                  {#if room.lastMessage}
                    <p class="text-sm text-gray-500 truncate">{room.lastMessage}</p>
                  {/if}
                </div>
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Chat panel -->
    <div class="flex-1 flex flex-col">
      {#if selectedRoomId}
        <ChatRoom roomId={selectedRoomId} roomName={selectedRoomName} />
      {:else}
        <div class="flex items-center justify-center h-full text-gray-500">
          Select a chat or create a new one to get started
        </div>
      {/if}
    </div>
  </div>
  
  <!-- New Chat Modal -->
  {#if showNewChatForm}
    <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        <div class="p-4 border-b">
          <h3 class="text-lg font-medium">New Conversation</h3>
        </div>
        
        <form on:submit|preventDefault={handleCreateChat} class="p-4">
          <!-- Chat name input -->
          <div class="mb-4">
            <label for="chatName" class="block text-sm font-medium text-gray-700 mb-1">
              Conversation Name
            </label>
            <input
              id="chatName"
              type="text"
              bind:value={newChatName}
              required
              placeholder="Enter conversation name"
              class="w-full border rounded px-3 py-2"
            />
          </div>
          
          <!-- Chat type selection -->
          <div class="mb-4">
            <label for="chatType" class="block text-sm font-medium text-gray-700 mb-1">
              Conversation Type
            </label>
            <div class="flex space-x-4" id="chatType">
              <label class="flex items-center">
                <input type="radio" bind:group={newChatType} value="group" id="type-group" name="chatType" class="mr-1">
                <span>Group</span>
              </label>
              <label class="flex items-center">
                <input type="radio" bind:group={newChatType} value="project" id="type-project" name="chatType" class="mr-1">
                <span>Project</span>
              </label>
              <label class="flex items-center">
                <input type="radio" bind:group={newChatType} value="class" id="type-class" name="chatType" class="mr-1">
                <span>Class</span>
              </label>
            </div>
          </div>
          
          <!-- Participant search -->
          <div class="mb-4">
            <label for="participantSearch" class="block text-sm font-medium text-gray-700 mb-1">
              Add Participants
            </label>
            <input
              id="participantSearch"
              type="text"
              bind:value={searchTerm}
              placeholder="Search people..."
              class="w-full border rounded px-3 py-2 mb-2"
            />
            
            <!-- Selected participants -->
            {#if selectedParticipants.length > 0}
              <div class="flex flex-wrap gap-2 mb-2">
                {#each selectedParticipants as participant, i}
                  <div class="flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                    <span>{participant.displayName}</span>
                    <button
                      on:click={() => toggleParticipant(participant)}
                      class="ml-1 text-blue-600 hover:text-blue-800"
                      aria-label={`Remove ${participant.displayName}`}
                    >
                      &times;
                    </button>
                  </div>
                {/each}
              </div>
            {/if}
            
            <!-- Available participants -->
            <div class="border rounded h-40 overflow-y-auto">
              {#if filteredParticipants.length === 0}
                <div class="p-3 text-gray-500 text-sm text-center">
                  {searchTerm ? 'No users found' : 'No online users available'}
                </div>
              {:else}
                {#each filteredParticipants as participant}
                  <button
                    type="button"
                    on:click={() => toggleParticipant(participant)}
                    class="w-full flex items-center p-2 hover:bg-gray-50 text-left {
                      selectedParticipants.some(p => p.uid === participant.uid) ? 'bg-blue-50' : ''
                    }"
                    aria-label={`${selectedParticipants.some(p => p.uid === participant.uid) ? 'Remove' : 'Add'} ${participant.displayName}`}
                  >
                    <img
                      src={participant.photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(participant.displayName)}`}
                      alt={participant.displayName}
                      class="w-6 h-6 rounded-full mr-2"
                    />
                    <div class="flex-1">
                      <div class="font-medium text-sm">{participant.displayName}</div>
                      <div class="text-xs text-gray-500 capitalize">{participant.userType}</div>
                    </div>
                    {#if selectedParticipants.some(p => p.uid === participant.uid)}
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                    {/if}
                  </button>
                {/each}
              {/if}
            </div>
          </div>
          
          {#if error}
            <div class="mb-4 text-red-600 text-sm">{error}</div>
          {/if}
          
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              on:click={() => showNewChatForm = false}
              class="px-4 py-2 border rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!newChatName.trim() || creating}
              class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
            >
              {#if creating}
                Creating...
              {:else}
                Create
              {/if}
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}
</div>