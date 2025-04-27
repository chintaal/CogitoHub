<script lang="ts">
  import TimetunesLogo from '../../../components/logos/timetunesLogo.svelte';
  
  // Tag management state
  let tags = [
    { id: 'tag1', name: 'Important', color: '#FF5733', usageCount: 15 },
    { id: 'tag2', name: 'Meeting', color: '#33A8FF', usageCount: 8 },
    { id: 'tag3', name: 'Research', color: '#A233FF', usageCount: 12 },
    { id: 'tag4', name: 'Planning', color: '#33FF57', usageCount: 6 },
    { id: 'tag5', name: 'Coding', color: '#FFD133', usageCount: 20 },
    { id: 'tag6', name: 'Reading', color: '#FF33A8', usageCount: 9 }
  ];
  
  // Tag form state
  let isAddingTag = false;
  let editingTag: typeof tags[0] | null = null;
  let newTag = {
    id: '',
    name: '',
    color: '#33A8FF',
    usageCount: 0
  };
  
  // Available colors
  const colorOptions = [
    '#FF5733', // Red-Orange
    '#33A8FF', // Light Blue
    '#A233FF', // Purple
    '#33FF57', // Green
    '#FFD133', // Yellow
    '#FF33A8', // Pink
    '#33FFC1', // Teal
    '#9E8866', // Brown
    '#66739E', // Slate Blue
    '#9E6672'  // Mauve
  ];
  
  // Show edit form
  function editTag(tag: typeof tags[0]) {
    editingTag = { ...tag };
    isAddingTag = false;
  }
  
  // Show add form
  function showAddForm() {
    newTag = {
      id: `tag${tags.length + 1}`,
      name: '',
      color: colorOptions[Math.floor(Math.random() * colorOptions.length)],
      usageCount: 0
    };
    isAddingTag = true;
    editingTag = null;
  }
  
  // Cancel editing
  function cancelEdit() {
    editingTag = null;
    isAddingTag = false;
  }
  
  // Save tag changes
  function saveTagChanges() {
    if (editingTag) {
      const index = tags.findIndex(p => p.id === editingTag?.id);
      if (index !== -1) {
        tags[index] = { ...editingTag };
        tags = [...tags]; // Trigger reactivity
      }
      editingTag = null;
    }
  }
  
  // Add new tag
  function addTag() {
    if (newTag.name.trim()) {
      tags = [...tags, { ...newTag }];
      isAddingTag = false;
    }
  }
  
  // Delete tag
  function deleteTag(id: string) {
    const tag = tags.find(t => t.id === id);
    if (tag && tag.usageCount > 0) {
      if (!confirm(`This tag is used in ${tag.usageCount} time entries. Are you sure you want to delete it?`)) {
        return;
      }
    }
    tags = tags.filter(t => t.id !== id);
  }
  
  // Sort tags
  let sortOption = 'name-asc';
  
  $: sortedTags = [...tags].sort((a, b) => {
    if (sortOption === 'name-asc') {
      return a.name.localeCompare(b.name);
    } else if (sortOption === 'name-desc') {
      return b.name.localeCompare(a.name);
    } else if (sortOption === 'usage-asc') {
      return a.usageCount - b.usageCount;
    } else if (sortOption === 'usage-desc') {
      return b.usageCount - a.usageCount;
    }
    return 0;
  });
  
  // Search functionality
  let searchQuery = '';
  
  $: filteredTags = sortedTags.filter(tag => 
    tag.name.toLowerCase().includes(searchQuery.toLowerCase())
  );
</script>

<div class="min-h-screen bg-gradient-to-br from-amber-50 to-amber-100">
  <!-- Header -->
  <header class="bg-gradient-to-r from-amber-600 to-amber-800 text-white p-6 shadow-lg">
    <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
      <div class="flex items-center mb-4 md:mb-0">
        <a href="/timetunes" class="flex items-center no-underline text-white">
          <TimetunesLogo size={50} />
          <h1 class="text-3xl font-bold ml-4">TimeTunes</h1>
        </a>
      </div>
      <div class="flex items-center space-x-4">
        <a href="/timetunes" class="hover:text-amber-200 transition-colors">Timer</a>
        <a href="/timetunes#dashboard" class="hover:text-amber-200 transition-colors">Dashboard</a>
        <a href="/timetunes/reports" class="hover:text-amber-200 transition-colors">Reports</a>
        <a href="/timetunes/projects" class="hover:text-amber-200 transition-colors">Projects</a>
        <a href="/timetunes/tags" class="text-amber-200 font-medium transition-colors border-b-2 border-amber-200 pb-1">Tags</a>
      </div>
    </div>
  </header>
  
  <main class="container mx-auto p-6">
    <!-- Tag Management Header -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Tags</h1>
        <button 
          on:click={showAddForm}
          class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add Tag
        </button>
      </div>
    </section>
    
    <!-- Tag Management Section -->
    <section class="bg-white rounded-2xl p-6 shadow-lg mb-8">
      <!-- Tag Filter & Sort -->
      <div class="flex flex-col md:flex-row justify-between mb-6 gap-4">
        <div class="relative flex-grow max-w-md">
          <input 
            type="text" 
            bind:value={searchQuery}
            placeholder="Search tags..." 
            class="w-full p-2 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
          />
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <div class="flex items-center">
          <label for="sort" class="text-sm font-medium text-gray-500 mr-2 whitespace-nowrap">Sort by:</label>
          <select 
            id="sort" 
            bind:value={sortOption}
            class="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent text-sm"
          >
            <option value="name-asc">Name (A-Z)</option>
            <option value="name-desc">Name (Z-A)</option>
            <option value="usage-desc">Most Used</option>
            <option value="usage-asc">Least Used</option>
          </select>
        </div>
      </div>
      
      <!-- Tag List -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each filteredTags as tag (tag.id)}
          <div class="border border-gray-200 rounded-lg p-4 hover:bg-amber-50 transition-colors">
            <div class="flex items-start justify-between">
              <div class="flex items-center">
                <div class="w-6 h-6 rounded-full mr-3" style={`background-color: ${tag.color}`}></div>
                <h3 class="font-medium">{tag.name}</h3>
              </div>
              
              <div class="flex gap-2">
                <button 
                  on:click={() => editTag(tag)}
                  class="text-gray-400 hover:text-amber-600 p-1" 
                  title="Edit Tag"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                </button>
                
                <button 
                  on:click={() => deleteTag(tag.id)}
                  class="text-gray-400 hover:text-red-600 p-1"
                  title="Delete Tag"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="text-sm text-gray-500 mt-2">
              Used in {tag.usageCount} {tag.usageCount === 1 ? 'entry' : 'entries'}
            </div>
            
            {#if tag.usageCount > 0}
              <div class="mt-2 flex">
                <div class="h-2 bg-amber-200 rounded-full" style={`width: ${Math.min(tag.usageCount / 20 * 100, 100)}%`}></div>
              </div>
            {/if}
          </div>
        {:else}
          <div class="col-span-full text-center py-8 text-gray-500">
            {searchQuery ? 'No tags match your search criteria.' : 'No tags yet. Add your first tag to get started!'}
          </div>
        {/each}
      </div>
    </section>
    
    <!-- Tag Edit Form (Modal) -->
    {#if editingTag}
      <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-2xl p-6 shadow-2xl max-w-md w-full mx-4">
          <h2 class="text-xl font-bold mb-6 text-gray-800">Edit Tag</h2>
          
          <div class="space-y-4">
            <div>
              <label for="edit-name" class="block text-sm font-medium text-gray-700 mb-1">Tag Name</label>
              <input 
                id="edit-name"
                type="text" 
                bind:value={editingTag.name}
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                placeholder="Tag name"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Color</label>
              <div class="flex flex-wrap gap-2">
                {#each colorOptions as color}
                  <button 
                    on:click={() => editingTag!.color = color}
                    class="w-8 h-8 rounded-full flex items-center justify-center border-2"
                    style={`background-color: ${color}; border-color: ${editingTag.color === color ? 'black' : 'transparent'}`}
                  >
                    {#if editingTag.color === color}
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    {/if}
                  </button>
                {/each}
              </div>
            </div>
            
            <div class="text-sm text-gray-500 mt-2">
              This tag is used in {editingTag.usageCount} {editingTag.usageCount === 1 ? 'entry' : 'entries'}
            </div>
          </div>
          
          <div class="flex justify-end mt-6 space-x-3">
            <button 
              on:click={cancelEdit}
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button 
              on:click={saveTagChanges}
              class="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    {/if}
    
    <!-- Add Tag Form (Modal) -->
    {#if isAddingTag}
      <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-2xl p-6 shadow-2xl max-w-md w-full mx-4">
          <h2 class="text-xl font-bold mb-6 text-gray-800">Add New Tag</h2>
          
          <div class="space-y-4">
            <div>
              <label for="new-name" class="block text-sm font-medium text-gray-700 mb-1">Tag Name</label>
              <input 
                id="new-name"
                type="text" 
                bind:value={newTag.name}
                class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                placeholder="Tag name"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Color</label>
              <div class="flex flex-wrap gap-2">
                {#each colorOptions as color}
                  <button 
                    on:click={() => newTag.color = color}
                    class="w-8 h-8 rounded-full flex items-center justify-center border-2"
                    style={`background-color: ${color}; border-color: ${newTag.color === color ? 'black' : 'transparent'}`}
                  >
                    {#if newTag.color === color}
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    {/if}
                  </button>
                {/each}
              </div>
            </div>
          </div>
          
          <div class="flex justify-end mt-6 space-x-3">
            <button 
              on:click={cancelEdit}
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button 
              on:click={addTag}
              class="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
            >
              Add Tag
            </button>
          </div>
        </div>
      </div>
    {/if}
  </main>
  
  <!-- Footer -->
  <footer class="bg-gray-800 text-white py-8 mt-16">
    <div class="container mx-auto px-6">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-4 md:mb-0">
          <TimetunesLogo size={40} />
          <p class="mt-2 text-gray-400">Time tracking that works for you</p>
        </div>
        
        <div class="flex space-x-8">
          <div>
            <h4 class="font-semibold mb-3">Product</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">Features</a></li>
              <li><a href="#" class="hover:text-white">Pricing</a></li>
              <li><a href="#" class="hover:text-white">Apps</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3">Resources</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">Blog</a></li>
              <li><a href="#" class="hover:text-white">Help Center</a></li>
              <li><a href="#" class="hover:text-white">Contact</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-semibold mb-3">Company</h4>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white">About Us</a></li>
              <li><a href="#" class="hover:text-white">Careers</a></li>
              <li><a href="#" class="hover:text-white">Legal</a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-700 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-400">© 2025 TimeTunes. All rights reserved.</p>
        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd"></path>
            </svg>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
            </svg>
          </a>
          <a href="#" class="text-gray-400 hover:text-white">
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd"></path>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</div>

<style>
  /* Additional styles for TimeTunes */
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
  }
</style>