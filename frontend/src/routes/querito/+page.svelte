<script>
    import { onMount } from 'svelte';
    let darkMode = false;
    let cogees = Math.floor(Math.random() * 1000) + 1;
    let dropdownOpen = false;
    let modalOpen = false;
    let toastVisible = false;

    function toggleDropdown() {
        dropdownOpen = !dropdownOpen;
    }

    function openModal() {
        modalOpen = true;
    }

    function closeModal() {
        modalOpen = false;
    }

    function submitQuery() {
        modalOpen = false;
        toastVisible = true;
        setTimeout(() => {
            toastVisible = false;
        }, 3000);
    }

    let floatingButton;

    onMount(() => {
        const interval = setInterval(() => {
            if (floatingButton) {
                floatingButton.classList.add('animate-bounce');
                setTimeout(() => {
                    floatingButton.classList.remove('animate-bounce');
                }, 1000);
            }
        }, 5000);

        return () => clearInterval(interval);
    });
</script>

<!-- Floating Button with improved animation and styling -->
<button 
	bind:this={floatingButton}
	aria-label="Create new query"
	class="fixed bottom-10 right-10 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300 z-50 flex items-center justify-center w-14 h-14"
	on:click={openModal}>
	<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
		<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
	</svg>
</button>

<!-- Modal with improved styling -->
{#if modalOpen}
<div class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50">
	<div class="bg-white rounded-xl shadow-2xl p-6 w-full max-w-lg mx-4 transform transition-all duration-300 scale-100">
		<div class="flex justify-between items-center mb-6">
			<h2 class="text-xl font-bold text-gray-800">New Query</h2>
			<button 
				on:click={closeModal}
				class="text-gray-400 hover:text-gray-600 transition-colors"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
		<form on:submit|preventDefault={submitQuery} class="space-y-6">
			<div>
				<label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
				<input 
					id="title" 
					type="text" 
					class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all" 
					required 
					placeholder="What's your question?"
				/>
			</div>
			<div>
				<label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
				<textarea 
					id="description" 
					class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all" 
					rows="4" 
					required
					placeholder="Provide more details about your question..."
				></textarea>
			</div>
			<div>
				<label for="tags" class="block text-sm font-medium text-gray-700 mb-1">Tags</label>
				<input 
					id="tags" 
					type="text" 
					placeholder="e.g., javascript, react, web-development" 
					class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all" 
				/>
			</div>
			<div class="flex justify-end space-x-3">
				<button 
					type="button" 
					class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
					on:click={closeModal}
				>
					Cancel
				</button>
				<button 
					type="submit" 
					class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-lg hover:from-indigo-700 hover:to-indigo-800 transform hover:scale-105 transition-all"
				>
					Submit Query
				</button>
			</div>
		</form>
	</div>
</div>
{/if}

<!-- Toast Notification with improved styling -->
{#if toastVisible}
<div class="fixed bottom-6 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-lg shadow-xl flex items-center space-x-3 z-50">
	<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
		<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
	</svg>
	<span>Query submitted successfully!</span>
</div>
{/if}

<!-- Navigation Bar with improved styling -->
<nav class="sticky top-0 bg-white border-b border-gray-200 font-sans z-40 shadow-sm">
	<div class="max-w-7xl mx-auto">
		<div class="flex justify-between items-center h-16 px-4 sm:px-6 lg:px-8">
			<!-- Left: Logo -->
			<div class="flex items-center">
				<img 
					src="/src/lib/Images/querito.png" 
					alt="Querito Logo" 
					class="h-10 w-auto transform transition-transform duration-200 hover:scale-110" 
				/>
			</div>

			<!-- Center: Page Title -->
			<h1 class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-indigo-800">
				Querito - Real-Time Knowledge Exchange
			</h1>

			<!-- Right: Cogees -->
			<div class="relative">
				<button 
					class="flex items-center space-x-2 bg-gray-50 px-4 py-2 rounded-lg hover:bg-gray-100 transition-all duration-200"
					on:click={toggleDropdown}
				>
					<img src="/src/lib/Images/Cogee-coin.png" alt="Cogee Coin" class="h-8 w-8" />
					<span class="text-lg font-semibold text-gray-800">{cogees}</span>
				</button>

				<!-- Enhanced Dropdown -->
				{#if dropdownOpen}
    <div 
        class="absolute right-0 mt-2 w-56 bg-white shadow-xl rounded-xl overflow-hidden transform transition-all duration-200 ease-out z-50 border border-gray-100"
    >
        <div class="p-4 bg-gradient-to-r from-indigo-50 to-indigo-100">
            <p class="text-sm font-medium text-gray-600">Your Balance</p>
            <p class="text-2xl font-bold text-indigo-600">{cogees} Cogees</p>
        </div>
        <div class="p-2">
			<button 
				class="flex items-center space-x-2 px-4 py-3 hover:bg-gray-50 rounded-lg transition-colors w-full text-left"
				on:click={() => { /* Add reward view logic */ }}
				aria-label="View My Rewards"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500" viewBox="0 0 20 20" fill="currentColor">
					<path d="M10 2a6 6 0 00-6 6v14h12V8a6 6 0 00-6-6z" />
				</svg>
				<span class="text-gray-700">View My Rewards</span>
			<button 
				class="flex items-center space-x-2 px-4 py-3 hover:bg-gray-50 rounded-lg transition-colors w-full text-left"
				on:click={() => { /* Add bonus claim logic */ }}
				aria-label="Claim Bonuses"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-500" viewBox="0 0 20 20" fill="currentColor"></svg>
					<path fill-rule="evenodd" d="M5 2a2 2 0 00-2 2v14l3.5-2 3.5 2 3.5-2 3.5 2V4a2 2 0 00-2-2H5zm4.707 3.707a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L8.414 9H10a3 3 0 013 3v1a1 1 0 102 0v-1a5 5 0 00-5-5H8.414l1.293-1.293z" clip-rule="evenodd" />
				</svg>
				<span class="text-gray-700">Claim Bonuses</span>
			</button>
            </button>
        </div>
    </div>
{/if}
			</div>
		</div>
	</div>
</nav>

<!-- Main Content -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
	<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
		<!-- Filter Panel with improved styling -->
		<div class="col-span-1 space-y-6">
			<div class="bg-white rounded-xl shadow-sm p-6">
				<h2 class="text-lg font-semibold text-gray-800 mb-4">Filter Discussions</h2>
				
				<div class="space-y-4">
					<!-- Search Bar -->
					<div class="relative">
						<input 
							type="text" 
							placeholder="Search queries" 
							class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
						/>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" viewBox="0 0 20 20" fill="currentColor">
							<path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
						</svg>
					</div>

					<!-- Topic Badges -->
					<div class="flex flex-wrap gap-2">
						<button class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 transition-colors">
							Math
						</button>
						<button class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 transition-colors">
							AI
						</button>
						<button class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 transition-colors">
							History
						</button>
					</div>

					<!-- Filter Options -->
					<div class="space-y-3">
						<label class="flex items-center space-x-3">
							<input type="checkbox" class="form-checkbox h-5 w-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
							<span class="text-gray-700">Show AI Answers</span>
						</label>
						<label class="flex items-center space-x-3">
							<input type="checkbox" class="form-checkbox h-5 w-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500" />
							<span class="text-gray-700">Show Only Mentor-Verified</span>
						</label>
					</div>

					<button class="w-full py-2 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-lg hover:from-indigo-700 hover:to-indigo-800 transform hover:scale-105 transition-all">
						Apply Filters
					</button>
				</div>
			</div>
		</div>

		<!-- Discussion Feed with improved post styling -->
		<main class="col-span-1 md:col-span-2 space-y-6">
			<!-- Example Post 1 -->
			<div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-all">
				<div class="space-y-4">
					<div>
						<h3 class="text-xl font-bold text-gray-800">What is the difference between AI and Machine Learning?</h3>
						<p class="text-sm text-gray-500 mt-1">Asked by Chirag A Chintaal• 2 hours ago</p>
					</div>
					
					<!-- Tags -->
					<div class="flex flex-wrap gap-2">
						<span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">AI</span>
						<span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">Machine Learning</span>
					</div>
					
					<!-- Answer Stats -->
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-6">
							<div class="flex items-center space-x-2">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd" />
								</svg>
								<span class="text-gray-600">0 Answers</span>
							</div>
							<div class="flex items-center space-x-2">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
									<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
									<path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
								</svg>
								<span class="text-gray-600">1 views</span>
							</div>
						</div>
						
						<button class="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white px-4 py-2 rounded-lg hover:from-indigo-700 hover:to-indigo-800 transform hover:scale-105 transition-all">
							Answer
						</button>
					</div>

					<!-- Reward Badge -->
					<div class="flex items-center space-x-2 bg-gradient-to-r from-cyan-50 to-blue-50 px-4 py-2 rounded-lg">
						<img src="/src/lib/Images/Cogee-coin.png" alt="Cogee Coin" class="h-5 w-5" />
						<p class="text-cyan-600 font-semibold">+10 Cogees for best answer!</p>
					</div>
				</div>
			</div>

			<!-- Example Post 2 -->
			<div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-all">
				<div class="space-y-4">
					<div>
						<h3 class="text-xl font-bold text-gray-800">How does blockchain technology work?</h3>
						<p class="text-sm text-gray-500 mt-1">Asked by Smruthi S Kadagadkai • 2 hours ago</p>
					</div>
					
					<!-- Tags -->
					<div class="flex flex-wrap gap-2">
						<span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">Blockchain</span>
						<span class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">Technology</span>
					</div>
					
					<!-- Answer Stats -->
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-6">
							<div class="flex items-center space-x-2">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd" />
								</svg>
								<span class="text-gray-600">0 Answers</span>
							</div>
							<div class="flex items-center space-x-2">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
									<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
									<path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
								</svg>
								<span class="text-gray-600">2 views</span>
							</div>
						</div>
						
						<button class="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white px-4 py-2 rounded-lg hover:from-indigo-700 hover:to-indigo-800 transform hover:scale-105 transition-all">
							Answer
						</button>
					</div>

					<!-- Reward Badge -->
					<div class="flex items-center space-x-2 bg-gradient-to-r from-cyan-50 to-blue-50 px-4 py-2 rounded-lg">
						<img src="/src/lib/Images/Cogee-coin.png" alt="Cogee Coin" class="h-5 w-5" />
						<p class="text-cyan-600 font-semibold">+10 Cogees for best answer!</p>
					</div>
				</div>
			</div>
		</main>

		<!-- Right Sidebar with improved styling -->
		<aside class="col-span-1 space-y-6">
			<!-- Top Cogees Earners -->
			<div class="bg-white rounded-xl shadow-sm p-6">
				<h2 class="text-lg font-semibold text-gray-800 mb-6">Top Cogees Earners</h2>
				<ul class="space-y-6">
					<li>
						<div class="flex items-center space-x-4 mb-2">
							<img src="/src/lib/Images/user1.png" alt="Avatar 1" class="h-10 w-10 rounded-full ring-2 ring-indigo-100" />
							<div>
								<p class="font-semibold text-gray-800">Smruthi S Kadagadkai</p>
								<p class="text-sm text-cyan-600 font-bold">+1200 Cogees</p>
							</div>
						</div>
						<div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
							<div class="bg-gradient-to-r from-indigo-500 to-indigo-600 h-2 rounded-full" style="width: 90%;"></div>
						</div>
					</li>
					<li>
						<div class="flex items-center space-x-4 mb-2">
							<img src="/src/lib/Images/user1.png" alt="Avatar 2" class="h-10 w-10 rounded-full ring-2 ring-indigo-100" />
							<div>
								<p class="font-semibold text-gray-800">Chirag A Chintaal</p>
								<p class="text-sm text-cyan-600 font-bold">+950 Cogees</p>
							</div>
						</div>
						<div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
							<div class="bg-gradient-to-r from-indigo-500 to-indigo-600 h-2 rounded-full" style="width: 75%;"></div>
						</div>
					</li>
					<li>
						<div class="flex items-center space-x-4 mb-2">
							<img src="/src/lib/Images/user1.png" alt="Avatar 3" class="h-10 w-10 rounded-full ring-2 ring-indigo-100" />
							<div>
								<p class="font-semibold text-gray-800">Charlie Brown</p>
								<p class="text-sm text-cyan-600 font-bold">+870 Cogees</p>
							</div>
						</div>
						<div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
							<div class="bg-gradient-to-r from-indigo-500 to-indigo-600 h-2 rounded-full" style="width: 65%;"></div>
						</div>
					</li>
				</ul>
			</div>

			<!-- My Stats -->
			<div class="bg-white rounded-xl shadow-sm p-6">
				<h2 class="text-lg font-semibold text-gray-800 mb-4">My Stats</h2>
				<div class="space-y-4">
					<div class="flex items-center justify-between p-3 bg-gradient-to-r from-indigo-50 to-indigo-100 rounded-lg">
						<div class="flex items-center space-x-3">
							<img src="/src/lib/Images/Cogee-coin.png" alt="Cogee Coin" class="h-8 w-8" />
							<div>
								<p class="text-sm text-gray-600">Total Cogees</p>
								<p class="text-2xl font-bold text-indigo-600">{cogees}</p>
							</div>
						</div>
					</div>

					<!-- Badges Section -->
					<div class="space-y-2">
						<h3 class="text-sm font-medium text-gray-700">Badges Earned</h3>
						<div class="flex flex-wrap gap-2">
							<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
								<svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
									<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
								</svg>
								Top Contributor
							</span>
							<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
								<svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
									<path d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.368zm1.414-1.414L6.524 5.11a6 6 0 018.367 8.367zM18 10a8 8 0 11-16 0 8 8 0 0116 0z"/>
								</svg>
								Mentor
							</span>
							<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
								<svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
									<path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
								</svg>
								AI Expert
							</span>
							<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
								<svg class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
									<path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zm0 16a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
								</svg>
								Early Adopter
							</span>
						</div>
					</div>
				</div>
			</div>
		</aside>
	</div>
</div>

<!-- Unique Interactive Bottom Bar -->
<div class="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-indigo-900 via-indigo-800 to-indigo-900 backdrop-blur-lg bg-opacity-95 text-white py-2 z-40 border-t border-indigo-700/30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
            <!-- Left Section: Community Stats -->
            <div class="flex items-center space-x-8">
                <div class="flex items-center space-x-2">
                    <div class="relative">
                        <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-200" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
                        </svg>
                    </div>
                    <span class="text-indigo-200">3 Members</span>
                </div>
                <div class="flex items-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-200" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-indigo-200">RVU Sub-Hub</span>
                </div>
            </div>

            <!-- Center Section: Quick Actions -->
            <div class="flex items-center space-x-4">
                <button class="hover:bg-indigo-700/50 px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-300 group-hover:text-white transition-colors" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                        <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-indigo-300 group-hover:text-white transition-colors">Draft</span>
                </button>
                <button class="hover:bg-indigo-700/50 px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-300 group-hover:text-white transition-colors" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-indigo-300 group-hover:text-white transition-colors">Analytics</span>
                </button>
                <button class="hover:bg-indigo-700/50 px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-2 group">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-300 group-hover:text-white transition-colors" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                    </svg>
                    <span class="text-indigo-300 group-hover:text-white transition-colors">Share</span>
                </button>
            </div>

            <!-- Right Section: Theme & Help -->
            <div class="flex items-center space-x-6">
				<!-- Theme Toggle with Animation -->
				<button 
					aria-label="Toggle dark mode"
					class="relative w-12 h-6 rounded-full bg-indigo-700/50 flex items-center transition-colors duration-300 focus:outline-none"
					class:bg-indigo-600={darkMode}
					on:click={() => darkMode = !darkMode}
				>
                    <div class="absolute left-0.5 transform transition-transform duration-500"
                         class:translate-x-6={darkMode}>
                        <div class="w-5 h-5 rounded-full bg-white shadow-md flex items-center justify-center">
                            {#if darkMode}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                                </svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
                                </svg>
                            {/if}
                        </div>
                    </div>
                </button>
				<!-- Help Button with Custom Ping Animation -->
				<button class="relative group" aria-label="Get help">
					<div class="absolute -top-1 -right-1 w-2 h-2">
						<div class="absolute w-full h-full bg-cyan-400 rounded-full animate-ping"></div>
						<div class="absolute w-full h-full bg-cyan-500 rounded-full"></div>
					</div>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-300 group-hover:text-white transition-colors" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1z" clip-rule="evenodd" />
					</svg>
				</button>
            </div>
        </div>
    </div>
</div>

<style>
    /* Add any additional styles here */
</style>