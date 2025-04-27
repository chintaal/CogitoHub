<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, getUserProfile } from '../../lib/stores/authStore';
  import { listDocuments, createDocument, deleteDocument } from '../../lib/firebase/multitenantDb';
  import { uploadFile, listFiles, deleteFile } from '../../lib/firebase/storage';
  
  let userProfile = null;
  let loading = true;
  let notes = [];
  let files = [];
  let newNote = '';
  let uploadingFile = false;
  let message = '';
  let messageType = '';
  
  // Load user profile and data
  async function loadUserData() {
    if (!$user) {
      goto('/login');
      return;
    }
    
    loading = true;
    
    try {
      // Get user profile with tenant info
      userProfile = await getUserProfile($user.uid);
      
      // If we have a profile, load user's data
      if (userProfile) {
        // Load notes from Firestore with tenant isolation
        const notesResult = await listDocuments($user.uid, 'notes');
        if (notesResult.success) {
          notes = notesResult.data;
        }
        
        // Load files from Storage with tenant isolation
        const filesResult = await listFiles('user-files', $user.uid);
        if (filesResult.success) {
          files = filesResult.items || [];
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error);
      message = 'Failed to load data: ' + error.message;
      messageType = 'error';
    } finally {
      loading = false;
    }
  }
  
  // Add a new note with tenant isolation
  async function addNote() {
    if (!newNote.trim() || !$user) return;
    
    try {
      const result = await createDocument($user.uid, 'notes', {
        content: newNote.trim(),
        createdAt: new Date().toISOString()
      });
      
      if (result.success) {
        // Reload notes
        const notesResult = await listDocuments($user.uid, 'notes');
        if (notesResult.success) {
          notes = notesResult.data;
          newNote = '';
          message = 'Note added successfully';
          messageType = 'success';
        }
      }
    } catch (error) {
      console.error('Error adding note:', error);
      message = 'Failed to add note: ' + error.message;
      messageType = 'error';
    }
  }
  
  // Delete a note with tenant isolation
  async function removeNote(id) {
    try {
      const result = await deleteDocument($user.uid, 'notes', id);
      
      if (result.success) {
        // Remove from local array
        notes = notes.filter(note => note.id !== id);
        message = 'Note deleted successfully';
        messageType = 'success';
      }
    } catch (error) {
      console.error('Error deleting note:', error);
      message = 'Failed to delete note: ' + error.message;
      messageType = 'error';
    }
  }
  
  // Handle file upload with tenant isolation
  async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file || !$user) return;
    
    uploadingFile = true;
    message = '';
    
    try {
      const result = await uploadFile(file, `user-files/${file.name}`, $user.uid);
      
      if (result.success) {
        // Reload files
        const filesResult = await listFiles('user-files', $user.uid);
        if (filesResult.success) {
          files = filesResult.items || [];
          message = 'File uploaded successfully';
          messageType = 'success';
        }
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      message = 'Failed to upload file: ' + error.message;
      messageType = 'error';
    } finally {
      uploadingFile = false;
      // Clear the input
      event.target.value = '';
    }
  }
  
  // Delete a file with tenant isolation
  async function removeFile(path, name) {
    try {
      const result = await deleteFile(`user-files/${name}`, $user.uid);
      
      if (result.success) {
        // Remove from local array
        files = files.filter(file => file.name !== name);
        message = 'File deleted successfully';
        messageType = 'success';
      }
    } catch (error) {
      console.error('Error deleting file:', error);
      message = 'Failed to delete file: ' + error.message;
      messageType = 'error';
    }
  }
  
  // Initialize
  onMount(() => {
    const unsubscribe = user.subscribe(userData => {
      if (userData) {
        loadUserData();
      } else {
        // Redirect to login if not authenticated
        goto('/login');
      }
    });
    
    return unsubscribe;
  });
</script>

<div class="min-h-screen bg-gradient-to-b from-white to-gray-50 py-12 px-4">
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-900 mb-6">My Dashboard</h1>
    
    {#if message}
      <div class="mb-6 p-4 rounded-md {messageType === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}">
        {message}
      </div>
    {/if}
    
    {#if loading}
      <div class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    {:else if userProfile}
      <div class="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">Welcome, {userProfile.displayName || 'User'}</h2>
        <p class="text-gray-600 mb-2">
          Organization: <span class="font-medium">{userProfile.tenantId}</span>
        </p>
        <p class="text-sm text-gray-500">
          Your data is isolated and secure within your organization's context. 
          Each organization's data is completely separate from others.
        </p>
      </div>
      
      <div class="grid md:grid-cols-2 gap-8">
        <!-- Notes Section -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">My Notes</h2>
          
          <div class="mb-4">
            <div class="flex">
              <input 
                type="text" 
                bind:value={newNote} 
                placeholder="Add a new note" 
                class="flex-1 p-2 border border-gray-300 rounded-l-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <button 
                on:click={addNote}
                class="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Add
              </button>
            </div>
          </div>
          
          {#if notes.length === 0}
            <p class="text-gray-500 italic py-4 text-center">No notes yet. Add your first note!</p>
          {:else}
            <ul class="space-y-2">
              {#each notes as note (note.id)}
                <li class="p-3 bg-gray-50 rounded-md flex justify-between items-start">
                  <p class="text-gray-800">{note.content}</p>
                  <button 
                    on:click={() => removeNote(note.id)}
                    class="text-red-500 hover:text-red-700 ml-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
        
        <!-- Files Section -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">My Files</h2>
          
          <div class="mb-4">
            <label class="block">
              <span class="sr-only">Choose file</span>
              <input 
                type="file" 
                on:change={handleFileUpload} 
                class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
                file:rounded-md file:border-0 file:text-sm file:font-medium
                file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </label>
          </div>
          
          {#if uploadingFile}
            <div class="flex items-center space-x-2 text-sm text-gray-500 my-2">
              <div class="animate-spin h-4 w-4 border-2 border-blue-500 rounded-full border-t-transparent"></div>
              <span>Uploading file...</span>
            </div>
          {/if}
          
          {#if files.length === 0}
            <p class="text-gray-500 italic py-4 text-center">No files uploaded yet.</p>
          {:else}
            <ul class="space-y-2">
              {#each files as file (file.name)}
                <li class="p-3 bg-gray-50 rounded-md flex justify-between items-center">
                  <a 
                    href={file.url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    class="text-blue-600 hover:text-blue-800 truncate flex-1"
                  >
                    {file.name}
                  </a>
                  <button 
                    on:click={() => removeFile(file.fullPath, file.name)}
                    class="text-red-500 hover:text-red-700 ml-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </li>
              {/each}
            </ul>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>