<script>
  import { onMount } from 'svelte';
  import CogitoHubLogo from '../../components/logos/cogitohubLogo.svelte';
  import { slide, fade, fly } from 'svelte/transition';
  import { flip } from 'svelte/animate';
  
  // Updated user profile data
  let currentUser = {
    id: 1,
    name: "Smruthi Kadagadkai",
    avatar: "/api/placeholder/50/50",
    title: "PhD Candidate, Computer Science",
    university: "MS Ramaiah Institute of Technology",
    connections: 243,
    courses: [
      { id: 1, name: "Advanced Machine Learning" },
      { id: 2, name: "Data Visualization" },
      { id: 3, name: "Research Methods" }
    ]
  };

  // Updated posts/threads data with new names
  let posts = [
    {
      id: 1,
      author: {
        id: 2,
        name: "Prof. Badrinath",
        avatar: "/api/placeholder/50/50",
        title: "Professor of AI"
      },
      content: "Just published a new paper on transformer architectures in NLP. Check it out and let me know your thoughts!",
      link: "https://example.com/paper123",
      upvotes: 45,
      comments: 8,
      timestamp: "2 hours ago",
      tags: ["AI", "NLP", "Research"],
      course: "Advanced Machine Learning",
      isUpvoted: false,
      isSaved: true
    },
    {
      id: 2,
      author: {
        id: 3,
        name: "Chirag Chintaal",
        avatar: "/api/placeholder/50/50",
        title: "Research Assistant"
      },
      content: "Looking for study group partners for the upcoming Data Visualization project. Anyone interested?",
      upvotes: 12,
      comments: 15,
      timestamp: "5 hours ago",
      tags: ["Study Group", "Project"],
      course: "Data Visualization",
      isUpvoted: true,
      isSaved: false
    },
    {
      id: 3,
      author: {
        id: 4,
        name: "Aditya Raj",
        avatar: "/api/placeholder/50/50",
        title: "Graduate Research Assistant"
      },
      content: "New research databases added to our digital collection. Access now available for all students and faculty.",
      link: "https://library.example.edu/databases",
      upvotes: 32,
      comments: 3,
      timestamp: "1 day ago",
      tags: ["Resources", "Research", "Library"],
      course: null,
      isUpvoted: false,
      isSaved: false
    }
  ];

  // Course resources
  let resources = [
    {
      id: 1,
      title: "Introduction to Machine Learning",
      type: "PDF",
      course: "Advanced Machine Learning",
      author: "Prof. Robert Chen",
      uploadDate: "Jan 15, 2025",
      downloads: 128
    },
    {
      id: 2,
      title: "Data Visualization Techniques",
      type: "Video",
      course: "Data Visualization",
      author: "Dr. Lisa Johnson",
      uploadDate: "Feb 3, 2025",
      views: 89
    },
    {
      id: 3,
      title: "Research Paper Template",
      type: "DOCX",
      course: "Research Methods",
      author: "Prof. Michael Smith",
      uploadDate: "Mar 12, 2025",
      downloads: 56
    }
  ];

  // Discussion forums
  let discussions = [
    {
      id: 1,
      title: "Week 3 Assignment Discussion",
      course: "Advanced Machine Learning",
      lastPost: "2 hours ago",
      participants: 15,
      totalPosts: 47
    },
    {
      id: 2,
      title: "Final Project Planning",
      course: "Data Visualization",
      lastPost: "Yesterday",
      participants: 8,
      totalPosts: 23
    },
    {
      id: 3,
      title: "Literature Review Tips",
      course: "Research Methods",
      lastPost: "3 days ago",
      participants: 12,
      totalPosts: 38
    }
  ];

  // Updated recommendations with new names
  let peopleRecommendations = [
    {
      id: 5,
      name: "Dr. Sneha",
      avatar: "/api/placeholder/50/50",
      title: "Associate Professor",
      university: "IIT Bangalore",
      mutualConnections: 3
    },
    {
      id: 6,
      name: "Vijay Singhania",
      avatar: "/api/placeholder/50/50",
      title: "Technical Recruiter",
      university: "Google India",
      mutualConnections: 7
    }
  ];

  // State variables
  let activeTab = "feed";
  let showMobileMenu = false;
  let newPostContent = "";
  let searchQuery = "";
  let showNotifications = false;
  let isCreatingNewPost = false;
  let postImagePreview = null;
  let newPostTags = [];
  let newPostTag = "";
  let showCommentSection = {};
  let commentInputs = {};
  let filteredPosts = [];
  let filterType = "all";
  let sortOrder = "recent";
  let isLoading = false;

  // Notifications
  let notifications = [
    { id: 1, content: "Prof. Badrinath mentioned you in a comment", time: "5m ago", read: false },
    { id: 2, content: "Chirag Chintaal shared a new resource", time: "1h ago", read: false },
    { id: 3, content: "New application deadline for Research Grant", time: "3h ago", read: true }
  ];
  
  // Handle post submission with enhanced features
  function submitPost() {
    if (newPostContent.trim() === "") return;
    
    isLoading = true;
    
    setTimeout(() => {
      const newPost = {
        id: posts.length + 1,
        author: currentUser,
        content: newPostContent,
        image: postImagePreview,
        upvotes: 0,
        comments: [],
        timestamp: "Just now",
        tags: [...newPostTags],
        course: null,
        isUpvoted: false,
        isSaved: false
      };
      
      posts = [newPost, ...posts];
      filteredPosts = applyFilters(posts);
      newPostContent = "";
      postImagePreview = null;
      newPostTags = [];
      isCreatingNewPost = false;
      isLoading = false;
    }, 800);
  }
  
  // Filter and sort posts
  function applyFilters(allPosts) {
    let filtered = [...allPosts];
    
    // Apply type filter
    if (filterType !== "all") {
      if (filterType === "questions") {
        filtered = filtered.filter(post => post.content.includes("?"));
      } else if (filterType === "resources") {
        filtered = filtered.filter(post => post.link);
      } else if (filterType === "course") {
        filtered = filtered.filter(post => post.course);
      }
    }
    
    // Apply sorting
    if (sortOrder === "recent") {
      filtered.sort((a, b) => {
        if (a.timestamp === "Just now") return -1;
        if (b.timestamp === "Just now") return 1;
        return 0; // In a real app, convert timestamps to Date objects for proper comparison
      });
    } else if (sortOrder === "popular") {
      filtered.sort((a, b) => b.upvotes - a.upvotes);
    }
    
    return filtered;
  }
  
  // Handle file upload for post
  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      postImagePreview = e.target.result;
    };
    reader.readAsDataURL(file);
  }
  
  // Add tag to new post
  function addTag() {
    if (!newPostTag.trim() || newPostTags.includes(newPostTag.trim())) return;
    newPostTags = [...newPostTags, newPostTag.trim()];
    newPostTag = "";
  }
  
  // Remove tag from new post
  function removeTag(tag) {
    newPostTags = newPostTags.filter(t => t !== tag);
  }
  
  // Toggle comment section
  function toggleCommentSection(postId) {
    showCommentSection[postId] = !showCommentSection[postId];
  }
  
  // Add comment to post
  function addComment(postId) {
    if (!commentInputs[postId] || !commentInputs[postId].trim()) return;
    
    posts = posts.map(post => {
      if (post.id === postId) {
        return {
          ...post,
          comments: [...post.comments || [], {
            id: Date.now(),
            author: currentUser,
            content: commentInputs[postId],
            timestamp: "Just now"
          }]
        };
      }
      return post;
    });
    
    filteredPosts = applyFilters(posts);
    commentInputs[postId] = "";
  }
  
  // Mark notification as read
  function markAsRead(id) {
    notifications = notifications.map(notification => {
      if (notification.id === id) {
        return { ...notification, read: true };
      }
      return notification;
    });
  }
  
  // Handle upvote
  function toggleUpvote(postId) {
    posts = posts.map(post => {
      if (post.id === postId) {
        const upvoteChange = post.isUpvoted ? -1 : 1;
        return {
          ...post,
          isUpvoted: !post.isUpvoted,
          upvotes: post.upvotes + upvoteChange
        };
      }
      return post;
    });
  }
    
  // Handle save
  function toggleSave(postId) {
    posts = posts.map(post => {
      if (post.id === postId) {
        return {
          ...post,
          isSaved: !post.isSaved
        };
      }
      return post;
    });
  }
    
  // Handle search
  function handleSearch() {
    console.log(`Searching for: ${searchQuery}`);
    // Actual implementation would filter posts, resources, etc.
  }
    
  // Handle connection request
  function connectWith(personId) {
    peopleRecommendations = peopleRecommendations.filter(person => person.id !== personId);
  }
  
  $: unreadNotifications = notifications.filter(n => !n.read).length;
  $: filteredPosts = applyFilters(posts);
  
  onMount(() => {
    console.log("Component mounted");
  });
</script>

<!-- Updated Navigation Bar -->
<main class="bg-gray-100 min-h-screen">
  <nav class="bg-white shadow fixed top-0 left-0 right-0 z-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <CogitoHubLogo size={32} />
            <span class="ml-2 text-xl font-bold text-gray-900">CogitoHub</span>
          </div>
          <div class="hidden md:ml-6 md:flex md:space-x-8">
            <button 
              class={`px-3 py-2 text-sm font-medium ${activeTab === 'feed' ? 'text-blue-600 border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700'}`}
              on:click={() => activeTab = 'feed'}
            >
              Feed
            </button>
            <button 
              class={`px-3 py-2 text-sm font-medium ${activeTab === 'courses' ? 'text-blue-600 border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700'}`}
              on:click={() => activeTab = 'courses'}
            >
              Courses
            </button>
            <button 
              class={`px-3 py-2 text-sm font-medium ${activeTab === 'resources' ? 'text-blue-600 border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700'}`}
              on:click={() => activeTab = 'resources'}
            >
              Resources
            </button>
            <button 
              class={`px-3 py-2 text-sm font-medium ${activeTab === 'network' ? 'text-blue-600 border-b-2 border-blue-500' : 'text-gray-500 hover:text-gray-700'}`}
              on:click={() => activeTab = 'network'}
            >
              Network
            </button>
          </div>
        </div>
        <div class="flex items-center">
          <div class="flex-shrink-0 relative">
            <div class="md:hidden flex items-center">
              <button
                type="button"
                class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none"
                on:click={() => showMobileMenu = !showMobileMenu}
              >
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
            </div>
            <div class="hidden md:flex items-center space-x-4">
              <div class="relative">
                <input
                  type="text"
                  class="w-64 pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Search posts, resources, people..."
                  bind:value={searchQuery}
                  on:keydown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <div class="absolute left-3 top-2.5 text-gray-400">
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                </div>
              </div>
              
              <!-- Updated notification button with badge -->
              <div class="relative">
                <button 
                  class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100 relative"
                  on:click={() => showNotifications = !showNotifications}
                >
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
                  </svg>
                  {#if unreadNotifications > 0}
                    <span class="absolute top-0 right-0 block h-5 w-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center">
                      {unreadNotifications}
                    </span>
                  {/if}
                </button>
                
                <!-- Notification dropdown -->
                {#if showNotifications}
                  <div 
                    class="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg py-1 z-50"
                    transition:fly={{ y: -10, duration: 150 }}
                    use:clickOutside={() => showNotifications = false}
                  >
                    <div class="px-4 py-2 border-b border-gray-200">
                      <div class="flex justify-between items-center">
                        <h3 class="text-sm font-medium text-gray-900">Notifications</h3>
                        <button class="text-xs text-blue-600 hover:text-blue-800">
                          Mark all as read
                        </button>
                      </div>
                    </div>
                    
                    <div class="max-h-80 overflow-y-auto">
                      {#each notifications as notification (notification.id)}
                        <div 
                          class="px-4 py-3 hover:bg-gray-50 cursor-pointer flex items-start"
                          class:bg-blue-50={!notification.read}
                          on:click={() => markAsRead(notification.id)}
                        >
                          <div class="flex-1">
                            <p class="text-sm text-gray-800">{notification.content}</p>
                            <p class="text-xs text-gray-500 mt-1">{notification.time}</p>
                          </div>
                          {#if !notification.read}
                            <span class="h-2 w-2 bg-blue-600 rounded-full"></span>
                          {/if}
                        </div>
                      {/each}
                    </div>
                  </div>
                {/if}
              </div>
              
              <!-- Messages button -->
              <button class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
              </button>
              
              <!-- User menu dropdown -->
              <div class="relative">
                <button class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <img class="h-8 w-8 rounded-full" src={currentUser.avatar} alt="User avatar" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile menu -->
    {#if showMobileMenu}
      <div class="md:hidden bg-white border-t border-gray-200 px-2 pt-2 pb-3 space-y-1">
        <button 
          class={`block px-3 py-2 rounded-md text-base font-medium ${activeTab === 'feed' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-100'}`}
          on:click={() => { activeTab = 'feed'; showMobileMenu = false; }}
        >
          Feed
        </button>
        <button 
          class={`block px-3 py-2 rounded-md text-base font-medium ${activeTab === 'courses' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-100'}`}
          on:click={() => { activeTab = 'courses'; showMobileMenu = false; }}
        >
          Courses
        </button>
        <button 
          class={`block px-3 py-2 rounded-md text-base font-medium ${activeTab === 'resources' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-100'}`}
          on:click={() => { activeTab = 'resources'; showMobileMenu = false; }}
        >
          Resources
        </button>
        <button 
          class={`block px-3 py-2 rounded-md text-base font-medium ${activeTab === 'network' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-100'}`}
          on:click={() => { activeTab = 'network'; showMobileMenu = false; }}
        >
          Network
        </button>
        <div class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <img class="h-10 w-10 rounded-full" src={currentUser.avatar} alt="User avatar" />
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{currentUser.name}</div>
              <div class="text-sm font-medium text-gray-500">{currentUser.title}</div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </nav>

  <!-- Main content -->
  <div class="pt-16 pb-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="py-4">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- Updated Left Sidebar -->
          <div class="hidden lg:block lg:col-span-1">
            <div class="bg-white rounded-lg shadow-lg mb-6 overflow-hidden">
              <div class="p-4 border-b border-gray-200">
                <div class="flex items-center">
                  <img class="h-16 w-16 rounded-full" src={currentUser.avatar} alt="User avatar" />
                  <div class="ml-4">
                    <h2 class="text-lg font-medium text-gray-900">{currentUser.name}</h2>
                    <p class="text-sm text-gray-500">{currentUser.title}</p>
                    <p class="text-xs text-gray-500">{currentUser.university}</p>
                  </div>
                </div>
                <div class="mt-4">
                  <div class="flex justify-between">
                    <span class="text-sm text-gray-500">Connections</span>
                    <span class="text-sm font-medium text-gray-900">{currentUser.connections}</span>
                  </div>
                  <div class="flex justify-between mt-1">
                    <span class="text-sm text-gray-500">Courses</span>
                    <span class="text-sm font-medium text-gray-900">{currentUser.courses.length}</span>
                  </div>
                </div>
              </div>
              <div class="p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-2">My Courses</h3>
                <ul class="space-y-2">
                  {#each currentUser.courses as course}
                    <li>
                      <a href="#" class="text-sm text-blue-600 hover:underline">{course.name}</a>
                    </li>
                  {/each}
                </ul>
              </div>
            </div>
            
            <div class="bg-white rounded-lg shadow">
              <div class="p-4 border-b border-gray-200">
                <h3 class="text-sm font-medium text-gray-900">Upcoming Deadlines</h3>
              </div>
              <div class="p-4">
                <ul class="space-y-3">
                  <li class="flex justify-between items-center">
                    <div>
                      <p class="text-sm font-medium text-gray-900">Research Proposal</p>
                      <p class="text-xs text-gray-500">Research Methods</p>
                    </div>
                    <span class="text-xs font-medium text-red-600">Tomorrow</span>
                  </li>
                  <li class="flex justify-between items-center">
                    <div>
                      <p class="text-sm font-medium text-gray-900">Project Milestone</p>
                      <p class="text-xs text-gray-500">Data Visualization</p>
                    </div>
                    <span class="text-xs font-medium text-yellow-600">3 Days</span>
                  </li>
                  <li class="flex justify-between items-center">
                    <div>
                      <p class="text-sm font-medium text-gray-900">Final Exam</p>
                      <p class="text-xs text-gray-500">Advanced Machine Learning</p>
                    </div>
                    <span class="text-xs font-medium text-gray-600">2 Weeks</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Enhanced Main Content Area -->
          <div class="lg:col-span-2">
            <!-- Feed Tab Content with enhanced interactivity -->
            {#if activeTab === "feed"}
              <!-- Enhanced Create Post with modal -->
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4">
                  <div class="flex">
                    <img class="h-10 w-10 rounded-full" src={currentUser.avatar} alt="User avatar" />
                    <div class="ml-3 flex-1">
                      {#if !isCreatingNewPost}
                        <div 
                          class="w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-50 hover:bg-gray-100 cursor-text text-gray-500"
                          on:click={() => isCreatingNewPost = true}
                        >
                          Share a resource, ask a question, or start a discussion...
                        </div>
                      {:else}
                        <div transition:slide>
                          <textarea 
                            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                            rows="3"
                            placeholder="What would you like to share?"
                            bind:value={newPostContent}
                            autofocus
                          ></textarea>
                          
                          <!-- File upload preview -->
                          {#if postImagePreview}
                            <div class="relative mt-2 inline-block">
                              <img src={postImagePreview} alt="Upload preview" class="h-24 rounded-lg border border-gray-200">
                              <button 
                                class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                                on:click={() => postImagePreview = null}
                              >
                                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                              </button>
                            </div>
                          {/if}
                          
                          <!-- Tags input -->
                          <div class="flex flex-wrap items-center mt-2">
                            {#each newPostTags as tag (tag)}
                              <div class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-2 mb-2 flex items-center" animate:flip>
                                #{tag}
                                <button class="ml-1 text-blue-600" on:click={() => removeTag(tag)}>
                                  <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                  </svg>
                                </button>
                              </div>
                            {/each}
                            <div class="relative inline-block">
                              <input 
                                type="text" 
                                placeholder="Add tag" 
                                class="text-sm border border-gray-300 rounded-lg px-3 py-1 mr-2 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                bind:value={newPostTag}
                                on:keydown={(e) => e.key === 'Enter' && addTag()}
                              />
                              <button 
                                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 mr-2"
                                on:click={addTag}
                              >
                                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                              </button>
                            </div>
                          </div>
                          
                          <div class="mt-2 flex justify-between">
                            <div class="flex space-x-2">
                              <!-- File upload button -->
                              <label class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100 cursor-pointer">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <input type="file" class="hidden" accept="image/*" on:change={handleFileUpload}>
                              </label>
                              
                              <button class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                                </svg>
                              </button>
                              
                              <button class="p-2 rounded-full text-gray-400 hover:text-gray-500 hover:bg-gray-100">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                                </svg>
                              </button>
                            </div>
                            
                            <div class="flex space-x-2">
                              <button 
                                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                                on:click={() => {
                                  isCreatingNewPost = false;
                                  newPostContent = "";
                                  postImagePreview = null;
                                  newPostTags = [];
                                }}
                              >
                                Cancel
                              </button>
                              
                              <button 
                                class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center"
                                on:click={submitPost}
                                disabled={isLoading || !newPostContent.trim()}
                              >
                                {#if isLoading}
                                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                  </svg>
                                  Posting...
                                {:else}
                                  Post
                                {/if}
                              </button>
                            </div>
                          </div>
                        </div>
                      {/if}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Feed Controls: Filtering and Sorting -->
              <div class="bg-white rounded-lg shadow mb-4 p-3">
                <div class="flex flex-wrap justify-between items-center">
                  <div class="flex space-x-1 mb-2 sm:mb-0">
                    <button 
                      class="px-3 py-1 text-sm font-medium rounded-full {filterType === 'all' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
                      on:click={() => filterType = 'all'}
                    >
                      All
                    </button>
                    <button 
                      class="px-3 py-1 text-sm font-medium rounded-full {filterType === 'questions' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
                      on:click={() => filterType = 'questions'}
                    >
                      Questions
                    </button>
                    <button 
                      class="px-3 py-1 text-sm font-medium rounded-full {filterType === 'resources' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
                      on:click={() => filterType = 'resources'}
                    >
                      Resources
                    </button>
                    <button 
                      class="px-3 py-1 text-sm font-medium rounded-full {filterType === 'course' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
                      on:click={() => filterType = 'course'}
                    >
                      Course
                    </button>
                  </div>
                  
                  <div class="flex items-center">
                    <span class="text-sm text-gray-500 mr-2">Sort by:</span>
                    <select 
                      class="text-sm border border-gray-300 rounded-md p-1"
                      bind:value={sortOrder}
                    >
                      <option value="recent">Most Recent</option>
                      <option value="popular">Most Popular</option>
                    </select>
                  </div>
                </div>
              </div>
                
              <!-- Enhanced Posts Feed with animations and interactions -->
              {#each filteredPosts as post (post.id)}
                <div 
                  class="bg-white rounded-lg shadow mb-6"
                  transition:fade={{ duration: 300 }}
                  animate:flip={{ duration: 300 }}
                >
                  <div class="p-4">
                    <div class="flex justify-between">
                      <div class="flex">
                        <img class="h-10 w-10 rounded-full" src={post.author.avatar} alt="Author avatar" />
                        <div class="ml-3">
                          <h3 class="text-sm font-medium text-gray-900">{post.author.name}</h3>
                          <p class="text-xs text-gray-500">{post.author.title}</p>
                          <p class="text-xs text-gray-400">{post.timestamp}</p>
                        </div>
                      </div>
                      {#if post.course}
                        <span class="px-2 py-1 text-xs font-medium text-blue-800 bg-blue-100 rounded-full">
                          {post.course}
                        </span>
                      {/if}
                    </div>
                    
                    <div class="mt-3">
                      <p class="text-sm text-gray-800">{post.content}</p>
                      
                      <!-- Image preview if available -->
                      {#if post.image}
                        <div class="mt-3">
                          <img src={post.image} alt="Post attachment" class="rounded-lg max-h-80 w-auto">
                        </div>
                      {/if}
                      
                      {#if post.link}
                        <a href={post.link} class="mt-2 inline-block text-sm text-blue-600 hover:underline">
                          {post.link}
                        </a>
                      {/if}
                    </div>
                    
                    {#if post.tags && post.tags.length > 0}
                      <div class="mt-3 flex flex-wrap gap-2">
                        {#each post.tags as tag}
                          <span class="px-2 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded-full hover:bg-gray-300 cursor-pointer">
                            #{tag}
                          </span>
                        {/each}
                      </div>
                    {/if}
                    
                    <div class="mt-4 border-t border-gray-200 pt-3 flex justify-between">
                      <div class="flex space-x-4">
                        <button 
                          class={`flex items-center space-x-1 ${post.isUpvoted ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
                          on:click={() => toggleUpvote(post.id)}
                        >
                          <svg class="h-5 w-5" fill={post.isUpvoted ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                          </svg>
                          <span class="text-sm">{post.upvotes}</span>
                        </button>
                        
                        <button 
                          class="flex items-center space-x-1 text-gray-500 hover:text-gray-700"
                          on:click={() => toggleCommentSection(post.id)}
                        >
                          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                          </svg>
                          <span class="text-sm">{post.comments ? post.comments.length : 0}</span>
                        </button>
                      </div>
                      
                      <button 
                        class={`flex items-center space-x-1 ${post.isSaved ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
                        on:click={() => toggleSave(post.id)}
                      >
                        <svg class="h-5 w-5" fill={post.isSaved ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                        </svg>
                        <span class="text-sm">Save</span>
                      </button>
                    </div>
                    
                    <!-- Comment section with transitions -->
                    {#if showCommentSection[post.id]}
                      <div transition:slide>
                        <div class="mt-4 border-t border-gray-200 pt-4">
                          <!-- Comments list -->
                          {#if post.comments && post.comments.length > 0}
                            <div class="space-y-3 mb-3">
                              {#each post.comments as comment}
                                <div class="flex space-x-2">
                                  <img class="h-8 w-8 rounded-full" src={comment.author.avatar} alt="Commenter" />
                                  <div class="bg-gray-100 rounded-lg p-2 flex-1">
                                    <div class="flex justify-between items-center">
                                      <span class="text-xs font-medium text-gray-900">{comment.author.name}</span>
                                      <span class="text-xs text-gray-500">{comment.timestamp}</span>
                                    </div>
                                    <p class="text-sm text-gray-800">{comment.content}</p>
                                  </div>
                                </div>
                              {/each}
                            </div>
                          {/if}
                          
                          <!-- Comment input -->
                          <div class="flex space-x-2">
                            <img class="h-8 w-8 rounded-full" src={currentUser.avatar} alt="Your avatar" />
                            <div class="flex-1">
                              <input
                                type="text"
                                class="w-full border border-gray-300 rounded-full px-4 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Write a comment..."
                                bind:value={commentInputs[post.id]}
                                on:keydown={(e) => e.key === 'Enter' && addComment(post.id)}
                              />
                            </div>
                            <button
                              class="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-blue-700"
                              on:click={() => addComment(post.id)}
                              disabled={!commentInputs[post.id] || !commentInputs[post.id].trim()}
                            >
                              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" transform="rotate(90 12 12)" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    {/if}
                  </div>
                </div>
              {/each}
              
              <!-- Empty state for filtered posts -->
              {#if filteredPosts.length === 0}
                <div class="bg-white rounded-lg shadow p-8 text-center">
                  <svg class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  <h3 class="text-lg font-medium text-gray-900 mb-1">No posts found</h3>
                  <p class="text-gray-500">Try changing your filters or be the first to post in this category!</p>
                </div>
              {/if}
            {/if}

            <!-- Courses Tab Content -->
            {#if activeTab === "courses"}
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200">
                  <h2 class="text-lg font-medium text-gray-900">My Courses</h2>
                </div>
                <div class="p-4">
                  <div class="grid grid-cols-1 gap-4">
                    {#each currentUser.courses as course}
                      <div class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <h3 class="text-md font-medium text-gray-900">{course.name}</h3>
                        <div class="mt-3 flex justify-between">
                          <div class="flex space-x-2">
                            <button class="px-3 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-full">
                              Assignments
                            </button>
                            <button class="px-3 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full">
                              Materials
                            </button>
                            <button class="px-3 py-1 text-xs font-medium text-purple-700 bg-purple-100 rounded-full">
                              Discussions
                            </button>
                          </div>
                          <button class="text-sm text-blue-600 hover:underline">
                            View Course
                          </button>
                        </div>
                      </div>
                    {/each}
                  </div>
                </div>
              </div>
                
              <div class="bg-white rounded-lg shadow">
                <div class="p-4 border-b border-gray-200">
                  <h2 class="text-lg font-medium text-gray-900">Course Discussions</h2>
                </div>
                <div class="p-4">
                  <div class="grid grid-cols-1 gap-4">
                    {#each discussions as discussion}
                      <div class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                        <div class="flex justify-between">
                            <h3 class="text-md font-medium text-gray-900">{discussion.title}</h3>
                          <span class="px-2 py-1 text-xs font-medium text-blue-800 bg-blue-100 rounded-full">
                          {discussion.course}
                        </span>
                      </div>
                      <div class="mt-2 flex justify-between text-sm text-gray-500">
                        <div class="flex space-x-4">
                          <span>{discussion.participants} participants</span>
                          <span>{discussion.totalPosts} posts</span>
                        </div>
                        <span>Last post: {discussion.lastPost}</span>
                      </div>
                    </div>
                    {/each}
                  </div>
                </div>
              </div>
            {/if}
            
            <!-- Resources Tab Content -->
            {#if activeTab === "resources"}
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200 flex justify-between items-center">
                  <h2 class="text-lg font-medium text-gray-900">Course Materials</h2>
                  <button class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    Upload Resource
                  </button>
                </div>
                <div class="p-4">
                  <div class="flex justify-between mb-4">
                    <div class="relative w-64">
                      <input
                        type="text"
                        class="pl-10 pr-4 py-2 w-full rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Search resources..."
                      />
                      <div class="absolute left-3 top-2.5 text-gray-400">
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="flex space-x-2">
                      <button class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                        All Courses
                      </button>
                      <button class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                        Filter
                      </button>
                    </div>
                  </div>
                  <div class="overflow-hidden shadow border border-gray-200 rounded-lg">
                    <table class="min-w-full divide-y divide-gray-200">
                      <thead class="bg-gray-50">
                        <tr>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Title
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Course
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Author
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Date
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody class="bg-white divide-y divide-gray-200">
                        {#each resources as resource}
                          <tr class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                              <div class="flex items-center">
                                <div class="h-8 w-8 flex-shrink-0 bg-gray-100 rounded-lg flex items-center justify-center">
                                  {#if resource.type === "PDF"}
                                    <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                      <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"></path>
                                    </svg>
                                  {:else if resource.type === "Video"}
                                    <svg class="h-5 w-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                                      <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
                                    </svg>
                                  {:else}
                                    <svg class="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                      <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"></path>
                                    </svg>
                                  {/if}
                                </div>
                                <div class="ml-4">
                                  <div class="text-sm font-medium text-gray-900">{resource.title}</div>
                                  <div class="text-sm text-gray-500">{resource.type}</div>
                                </div>
                              </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                              <div class="text-sm text-gray-900">{resource.course}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                              <div class="text-sm text-gray-900">{resource.author}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                              <div class="text-sm text-gray-900">{resource.uploadDate}</div>
                              <div class="text-sm text-gray-500">
                                {#if resource.downloads}
                                  {resource.downloads} downloads
                                {:else if resource.views}
                                  {resource.views} views
                                {/if}
                              </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm">
                              <button class="text-blue-600 hover:text-blue-800 mr-3">Download</button>
                              <button class="text-gray-600 hover:text-gray-800">Share</button>
                            </td>
                          </tr>
                        {/each}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200">
                  <h2 class="text-lg font-medium text-gray-900">Popular Resources</h2>
                </div>
                <div class="p-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                      <div class="flex justify-between">
                        <div class="flex items-start">
                          <div class="h-10 w-10 flex-shrink-0 bg-blue-100 rounded-lg flex items-center justify-center">
                            <svg class="h-6 w-6 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 005.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
                            </svg>
                          </div>
                          <div class="ml-3">
                            <h3 class="text-sm font-medium text-gray-900">Machine Learning Fundamentals</h3>
                            <p class="text-xs text-gray-500">Comprehensive textbook - Dr. Anderson</p>
                          </div>
                        </div>
                        <span class="px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full">
                          320 Downloads
                        </span>
                      </div>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                      <div class="flex justify-between">
                        <div class="flex items-start">
                          <div class="h-10 w-10 flex-shrink-0 bg-purple-100 rounded-lg flex items-center justify-center">
                            <svg class="h-6 w-6 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                          </div>
                          <div class="ml-3">
                            <h3 class="text-sm font-medium text-gray-900">Data Visualization Best Practices</h3>
                            <p class="text-xs text-gray-500">Lecture slides - Prof. Williams</p>
                          </div>
                        </div>
                        <span class="px-2 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-full">
                          185 Views
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            {/if}
            
            <!-- Network Tab Content -->
            {#if activeTab === "network"}
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200 flex justify-between items-center">
                  <h2 class="text-lg font-medium text-gray-900">My Network</h2>
                  <button class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    Find Connections
                  </button>
                </div>
                <div class="p-4">
                  <div class="flex justify-between mb-4">
                    <div class="relative w-64">
                      <input
                        type="text"
                        class="pl-10 pr-4 py-2 w-full rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Search connections..."
                      />
                      <div class="absolute left-3 top-2.5 text-gray-400">
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="flex space-x-2">
                      <button class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                        All Connections
                      </button>
                      <button class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                        Filter
                      </button>
                    </div>
                  </div>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-lg border border-gray-200 flex items-center">
                      <img class="h-16 w-16 rounded-full" src="/api/placeholder/50/50" alt="Connection avatar" />
                      <div class="ml-4 flex-1">
                        <h3 class="text-md font-medium text-gray-900">Prof. Robert Chen</h3>
                        <p class="text-sm text-gray-500">Professor of AI</p>
                        <p class="text-sm text-gray-500">Stanford University</p>
                      </div>
                      <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">
                        Message
                      </button>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-gray-200 flex items-center">
                      <img class="h-16 w-16 rounded-full" src="/api/placeholder/50/50" alt="Connection avatar" />
                      <div class="ml-4 flex-1">
                        <h3 class="text-md font-medium text-gray-900">Dr. Lisa Johnson</h3>
                        <p class="text-sm text-gray-500">Data Science Lead</p>
                        <p class="text-sm text-gray-500">Harvard University</p>
                      </div>
                      <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">
                        Message
                      </button>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-gray-200 flex items-center">
                      <img class="h-16 w-16 rounded-full" src="/api/placeholder/50/50" alt="Connection avatar" />
                      <div class="ml-4 flex-1">
                        <h3 class="text-md font-medium text-gray-900">James Thompson</h3>
                        <p class="text-sm text-gray-500">PhD Student</p>
                        <p class="text-sm text-gray-500">Stanford University</p>
                      </div>
                      <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">
                        Message
                      </button>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-gray-200 flex items-center">
                      <img class="h-16 w-16 rounded-full" src="/api/placeholder/50/50" alt="Connection avatar" />
                      <div class="ml-4 flex-1">
                        <h3 class="text-md font-medium text-gray-900">Dr. Maria Garcia</h3>
                        <p class="text-sm text-gray-500">Research Scientist</p>
                        <p class="text-sm text-gray-500">MIT</p>
                      </div>
                      <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">
                        Message
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200">
                  <h2 class="text-lg font-medium text-gray-900">People You May Know</h2>
                </div>
                <div class="p-4">
                  <div class="grid grid-cols-1 gap-4">
                    {#each peopleRecommendations as person}
                      <div class="bg-white p-4 rounded-lg border border-gray-200 flex items-center">
                        <img class="h-16 w-16 rounded-full" src={person.avatar} alt="Person avatar" />
                        <div class="ml-4 flex-1">
                          <h3 class="text-md font-medium text-gray-900">{person.name}</h3>
                          <p class="text-sm text-gray-500">{person.title}</p>
                          <p class="text-sm text-gray-500">{person.university}</p>
                          <p class="text-xs text-gray-400">{person.mutualConnections} mutual connections</p>
                        </div>
                        <button 
                          class="px-3 py-1 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700"
                          on:click={() => connectWith(person.id)}
                        >
                          Connect
                        </button>
                      </div>
                    {/each}
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-lg shadow mb-6">
                <div class="p-4 border-b border-gray-200">
                  <h2 class="text-lg font-medium text-gray-900">Research Communities</h2>
                </div>
                <div class="p-4">
                  <div class="grid grid-cols-1 gap-4">
                    <div class="bg-white p-4 rounded-lg border border-gray-200">
                      <div class="flex justify-between">
                        <div>
                          <h3 class="text-md font-medium text-gray-900">Machine Learning Research Group</h3>
                          <p class="text-sm text-gray-500">243 members · 15 new posts this week</p>
                        </div>
                        <button class="px-3 py-1 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
                          Join
                        </button>
                      </div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-gray-200">
                      <div class="flex justify-between">
                        <div>
                          <h3 class="text-md font-medium text-gray-900">Data Visualization Community</h3>
                          <p class="text-sm text-gray-500">187 members · 8 new posts this week</p>
                        </div>
                        <button class="px-3 py-1 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
                          Join
                        </button>
                      </div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border border-gray-200">
                      <div class="flex justify-between">
                        <div>
                          <h3 class="text-md font-medium text-gray-900">Computer Science PhD Network</h3>
                          <p class="text-sm text-gray-500">472 members · 31 new posts this week</p>
                        </div>
                        <button class="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">
                          Joined
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            {/if}
          </div>
          
          <!-- Updated Right Sidebar -->
          <div class="hidden lg:block lg:col-span-1">
            <div class="bg-white rounded-lg shadow mb-6">
              <div class="p-4 border-b border-gray-200">
                <h3 class="text-sm font-medium text-gray-900">University Announcements</h3>
              </div>
              <div class="p-4">
                <ul class="space-y-3">
                  <li>
                    <a href="#" class="block hover:bg-gray-50 p-2 rounded-md">
                      <p class="text-sm font-medium text-gray-900">Spring Research Symposium</p>
                      <p class="text-xs text-gray-500">Registration open until May 15</p>
                    </a>
                  </li>
                  <li>
                    <a href="#" class="block hover:bg-gray-50 p-2 rounded-md">
                      <p class="text-sm font-medium text-gray-900">Library Extended Hours</p>
                      <p class="text-xs text-gray-500">Now open until midnight Mon-Fri</p>
                    </a>
                  </li>
                  <li>
                    <a href="#" class="block hover:bg-gray-50 p-2 rounded-md">
                      <p class="text-sm font-medium text-gray-900">New Database Access</p>
                      <p class="text-xs text-gray-500">ScienceDirect now available</p>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="bg-white rounded-lg shadow mb-6">
              <div class="p-4 border-b border-gray-200">
                <h3 class="text-sm font-medium text-gray-900">Active Discussions</h3>
              </div>
              <div class="p-4">
                <ul class="space-y-3">
                  {#each discussions as discussion}
                    <li>
                      <a href="#" class="block hover:bg-gray-50 p-2 rounded-md">
                        <p class="text-sm font-medium text-gray-900">{discussion.title}</p>
                        <div class="flex justify-between text-xs text-gray-500">
                          <span>{discussion.course}</span>
                          <span>{discussion.lastPost}</span>
                        </div>
                      </a>
                    </li>
                  {/each}
                </ul>
              </div>
            </div>
            
            <div class="bg-white rounded-lg shadow mb-6">
              <div class="p-4 border-b border-gray-200">
                <h3 class="text-sm font-medium text-gray-900">People You May Know</h3>
              </div>
              <div class="p-4">
                <ul class="space-y-4">
                  {#each peopleRecommendations as person}
                    <li class="flex">
                      <img class="h-10 w-10 rounded-full" src={person.avatar} alt="Person avatar" />
                      <div class="ml-3">
                        <p class="text-sm font-medium text-gray-900">{person.name}</p>
                        <p class="text-xs text-gray-500">{person.title}</p>
                        <button 
                          class="mt-1 text-xs text-blue-600 hover:text-blue-800"
                          on:click={() => connectWith(person.id)}
                        >
                          Connect
                        </button>
                      </div>
                    </li>
                  {/each}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Updated Footer -->
  <footer class="bg-white border-t border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="py-4 flex flex-col md:flex-row justify-between items-center">
        <div class="flex items-center">
          <CogitoHubLogo size={24} />
          <span class="ml-2 text-sm font-medium text-gray-900">CogitoHub</span>
        </div>
        <div class="mt-4 md:mt-0">
          <div class="flex space-x-6">
            <a href="#" class="text-gray-400 hover:text-gray-500">
              <span class="text-sm">About</span>
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-500">
              <span class="text-sm">Help Center</span>
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-500">
              <span class="text-sm">Privacy Policy</span>
            </a>
            <a href="#" class="text-gray-400 hover:text-gray-500">
              <span class="text-sm">Terms of Service</span>
            </a>
          </div>
        </div>
      </div>
      <div class="py-2 text-center text-xs text-gray-500">
        <p>© 2025 CogitoHub. All rights reserved.</p>
      </div>
    </div>
  </footer>
</main>

