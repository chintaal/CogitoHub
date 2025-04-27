<script>
  import { onMount, onDestroy } from 'svelte';
  import { user } from '../../lib/stores/authStore';
  import { 
    initChatRoom, 
    getChatMessages, 
    sendChatMessage, 
    leaveChatRoom 
  } from '../../lib/firebase/realtimeDb';
  
  export let roomId;
  export let roomName = '';
  export let roomType = 'group'; // 'direct', 'group', 'class', 'project'
  
  let loading = true;
  let error = '';
  let messageText = '';
  let messagesContainer;
  let messages = [];
  let unsubscribe;
  
  // Handle messages subscription
  onMount(async () => {
    if (!roomId) {
      error = 'Invalid room ID';
      loading = false;
      return;
    }
    
    try {
      // Initialize chat room
      await initChatRoom(roomId);
      
      // Subscribe to messages
      const messageStore = getChatMessages(roomId);
      unsubscribe = messageStore.subscribe(messageData => {
        messages = messageData;
        loading = false;
        
        // Scroll to bottom after render
        setTimeout(scrollToBottom, 100);
      });
    } catch (err) {
      console.error('Error initializing chat room:', err);
      error = err.message || 'Error loading chat room';
      loading = false;
    }
  });
  
  // Clean up on destroy
  onDestroy(() => {
    if (unsubscribe) unsubscribe();
    if (roomId) leaveChatRoom(roomId);
  });
  
  // Scroll to bottom of messages
  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }
  
  // Send message
  async function handleSendMessage() {
    if (!messageText.trim() || !$user) return;
    
    try {
      await sendChatMessage(roomId, messageText, $user.uid);
      messageText = '';
    } catch (err) {
      console.error('Error sending message:', err);
      error = err.message || 'Error sending message';
    }
  }
  
  // Format timestamp
  function formatTimestamp(timestamp) {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  
  // Format date for day separators
  function formatDate(timestamp) {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    // Check if same day
    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } 
    // Check if yesterday
    else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } 
    // Otherwise return formatted date
    else {
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      });
    }
  }
  
  // Group messages by sender for better UI
  $: groupedMessages = messages.reduce((groups, message) => {
    // Create a message date string for day separators
    const messageDate = message.timestamp 
      ? new Date(message.timestamp).toDateString()
      : 'Unknown';
    
    // Create a group key based on sender and timestamp proximity
    const lastGroup = groups.length > 0 ? groups[groups.length - 1] : null;
    const isSystem = message.isSystem;
    
    // Start a new group if:
    // 1. It's a system message
    // 2. There's no previous group
    // 3. The sender changed
    // 4. The previous message was more than 5 minutes ago
    // 5. The date changed (day separator)
    const needNewGroup = 
      isSystem || 
      !lastGroup || 
      lastGroup.senderId !== message.senderId || 
      (message.timestamp && lastGroup.lastTimestamp && 
       (message.timestamp - lastGroup.lastTimestamp > 5 * 60 * 1000)) ||
      (message.timestamp && 
       new Date(message.timestamp).toDateString() !== new Date(lastGroup.lastTimestamp).toDateString());
      
    // Add date separator if day changed
    if (lastGroup && message.timestamp && 
        new Date(message.timestamp).toDateString() !== new Date(lastGroup.lastTimestamp).toDateString()) {
      groups.push({
        isDateSeparator: true,
        date: message.timestamp,
        messages: []
      });
    }
    
    if (needNewGroup) {
      groups.push({
        senderId: message.senderId,
        senderName: message.senderName,
        senderPhoto: message.senderPhoto,
        isSystem: isSystem,
        lastTimestamp: message.timestamp,
        messages: [message]
      });
    } else {
      // Add to existing group
      lastGroup.messages.push(message);
      lastGroup.lastTimestamp = message.timestamp;
    }
    
    return groups;
  }, []);
  
  // Handle keydown for sending message
  function handleKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  }
</script>

<div class="flex flex-col h-full bg-white rounded-lg shadow-sm overflow-hidden">
  <!-- Chat Header -->
  <div class="p-3 border-b bg-gray-50 flex items-center justify-between">
    <div class="flex items-center">
      <div class="mr-2">
        {#if roomType === 'direct'}
          <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white">
            {roomName.charAt(0)}
          </div>
        {:else if roomType === 'group'}
          <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white">
            {roomName.charAt(0)}
          </div>
        {:else if roomType === 'class'}
          <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
        {:else if roomType === 'project'}
          <div class="w-10 h-10 bg-amber-500 rounded-full flex items-center justify-center text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        {/if}
      </div>
      <div>
        <h3 class="font-medium">{roomName || 'Chat Room'}</h3>
      </div>
    </div>
    
    <div>
      <button type="button" aria-label="Menu options" class="p-1 rounded-full hover:bg-gray-200 text-gray-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
        </svg>
      </button>
    </div>
  </div>
  
  <!-- Chat Messages -->
  <div 
    bind:this={messagesContainer}
    class="flex-1 overflow-y-auto p-4 space-y-4"
    style="max-height: calc(100% - 120px);"
  >
    {#if loading}
      <div class="flex justify-center py-6">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    {:else if error}
      <div class="bg-red-50 text-red-700 p-4 rounded">
        {error}
      </div>
    {:else if groupedMessages.length === 0}
      <div class="text-center py-10">
        <div class="text-gray-400 mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <p class="text-gray-500">No messages yet</p>
        <p class="text-sm text-gray-400 mt-1">Be the first to send a message!</p>
      </div>
    {:else}
      {#each groupedMessages as group}
        {#if group.isDateSeparator}
          <!-- Date Separator -->
          <div class="flex justify-center">
            <div class="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full">
              {formatDate(group.date)}
            </div>
          </div>
        {:else if group.isSystem}
          <!-- System Message -->
          <div class="flex justify-center">
            <div class="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-full max-w-xs text-center">
              {group.messages[0].text}
            </div>
          </div>
        {:else}
          <!-- User Message Group -->
          <div class="flex {group.senderId === $user?.uid ? 'justify-end' : 'justify-start'}">
            <div class="max-w-[80%]">
              <!-- User Info -->
              {#if group.senderId !== $user?.uid}
                <div class="flex items-center mb-1">
                  <img 
                    src={group.senderPhoto || `https://ui-avatars.com/api/?name=${encodeURIComponent(group.senderName || 'User')}`} 
                    alt={group.senderName} 
                    class="w-6 h-6 rounded-full mr-1"
                  />
                  <span class="text-xs font-medium text-gray-700">{group.senderName}</span>
                </div>
              {/if}
              
              <!-- Messages -->
              <div class="space-y-1">
                {#each group.messages as message}
                  <div class={`rounded-lg px-4 py-2 inline-block ${
                    message.senderId === $user?.uid
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    <p class="whitespace-pre-line break-words">{message.text}</p>
                  </div>
                {/each}
                
                <!-- Message Time -->
                <div class={`text-xs text-gray-500 ${group.senderId === $user?.uid ? 'text-right' : 'text-left'}`}>
                  {formatTimestamp(group.lastTimestamp)}
                </div>
              </div>
            </div>
          </div>
        {/if}
      {/each}
    {/if}
  </div>
  
  <!-- Message Input -->
  <div class="p-3 border-t">
    {#if error}
      <div class="bg-red-50 text-red-700 text-sm p-2 rounded mb-2">
        {error}
      </div>
    {/if}
    
    <form on:submit|preventDefault={handleSendMessage} class="flex items-end">
      <div class="flex-1 bg-gray-100 rounded-lg overflow-hidden">
        <textarea
          bind:value={messageText}
          on:keydown={handleKeydown}
          placeholder="Type a message..."
          class="w-full p-3 bg-transparent border-none focus:outline-none resize-none"
          style="max-height: 120px;"
          rows="1"
        ></textarea>
      </div>
      
      <button 
        type="submit"
        aria-label="Send message"
        class="ml-2 bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 focus:outline-none disabled:opacity-50"
        disabled={!messageText.trim() || loading}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </form>
  </div>
</div>