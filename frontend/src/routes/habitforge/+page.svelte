<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import HabitforgeIcon from '../../components/icons/habitforgeIcon.svelte';
    
    // Habit data store
    const habits = writable([
        { 
            id: 1, 
            name: 'Morning Meditation', 
            description: 'Practice mindfulness for 10 minutes',
            cue: 'After brushing teeth',
            action: 'Sit on meditation cushion and use Headspace app',
            reward: 'Cup of coffee after completion',
            streakCount: 5,
            completedDates: [
                new Date(new Date().setDate(new Date().getDate() - 1)),
                new Date(new Date().setDate(new Date().getDate() - 2)),
                new Date(new Date().setDate(new Date().getDate() - 3)),
                new Date(new Date().setDate(new Date().getDate() - 5)),
                new Date(new Date().setDate(new Date().getDate() - 6))
            ],
            targetDays: [0, 1, 2, 3, 4, 5, 6], // All days
            reflections: [
                { date: new Date(new Date().setDate(new Date().getDate() - 7)), text: 'Felt more focused throughout the day' }
            ]
        },
        { 
            id: 2, 
            name: 'Read 20 Pages', 
            description: 'Read non-fiction books',
            cue: 'After dinner',
            action: 'Sit in reading chair with book',
            reward: 'Mark progress in reading journal',
            streakCount: 3,
            completedDates: [
                new Date(new Date().setDate(new Date().getDate() - 1)),
                new Date(new Date().setDate(new Date().getDate() - 2)),
                new Date(new Date().setDate(new Date().getDate() - 3))
            ],
            targetDays: [1, 3, 5], // Mon, Wed, Fri
            reflections: []
        },
        { 
            id: 3, 
            name: 'Workout', 
            description: '30 minute strength training',
            cue: 'Gym clothes laid out night before',
            action: 'Follow planned workout routine',
            reward: 'Protein shake and marking progress',
            streakCount: 0,
            completedDates: [
                new Date(new Date().setDate(new Date().getDate() - 8)),
                new Date(new Date().setDate(new Date().getDate() - 15))
            ],
            targetDays: [0, 2, 4], // Sun, Tue, Thu
            reflections: []
        }
    ]);

    // Selected habit for detailed view
    let selectedHabit = writable(null);
    
    // UI State
    let activeTab = writable('dashboard');
    let showAddHabitModal = writable(false);
    let showReflectionModal = writable(false);
    let showReviewModal = writable(false);
    
    // Calculate today's date
    const today = new Date();
    const formattedToday = `${today.toLocaleDateString('en-US', { weekday: 'long' })}, ${today.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}`;
    
    // Calculate momentum score (example implementation)
    function calculateMomentumScore(habit) {
        const streakMultiplier = habit.streakCount * 2;
        const reflectionBonus = habit.reflections.length * 5;
        const completionRate = habit.completedDates.length > 0 ? 50 : 0;
        return Math.min(100, streakMultiplier + reflectionBonus + completionRate);
    }
    
    // Toggle habit completion for today
    function toggleHabitCompletion(habitId) {
        habits.update(habitsList => {
            return habitsList.map(habit => {
                if (habit.id === habitId) {
                    // Check if we've already completed the habit today
                    const todayString = new Date().toDateString();
                    const alreadyCompletedToday = habit.completedDates.some(date => date.toDateString() === todayString);
                    
                    if (alreadyCompletedToday) {
                        // Remove today from completed dates
                        habit.completedDates = habit.completedDates.filter(date => date.toDateString() !== todayString);
                        habit.streakCount = Math.max(0, habit.streakCount - 1);
                    } else {
                        // Add today to completed dates
                        habit.completedDates.push(new Date());
                        habit.streakCount += 1;
                    }
                }
                return habit;
            });
        });
    }
    
    // Check if a habit is completed today
    function isCompletedToday(habit) {
        const todayString = new Date().toDateString();
        return habit.completedDates.some(date => date.toDateString() === todayString);
    }

    onMount(() => {
        // Load data from localStorage if available
        const savedHabits = localStorage.getItem('habitforge-habits');
        if (savedHabits) {
            const parsedHabits = JSON.parse(savedHabits, (key, value) => {
                // Convert date strings back to Date objects
                if (key === 'completedDates' || key === 'date') {
                    return Array.isArray(value) 
                        ? value.map(dateStr => new Date(dateStr))
                        : new Date(value);
                }
                return value;
            });
            habits.set(parsedHabits);
        }

        // Save habits to localStorage whenever they change
        const unsubscribe = habits.subscribe(value => {
            localStorage.setItem('habitforge-habits', JSON.stringify(value));
        });

        return unsubscribe;
    });
</script>

<svelte:head>
    <title>HabitForge | Build Better Habits</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
    <!-- Header -->
    <header class="bg-gray-800/50 backdrop-blur-sm sticky top-0 z-10 border-b border-gray-700">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center gap-4">
                <HabitforgeIcon size={48} />
                <h1 class="text-2xl font-bold">HabitForge</h1>
            </div>
            <div class="text-right">
                <p class="text-sm text-gray-400">{formattedToday}</p>
                <button 
                    class="mt-2 bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
                    on:click={() => $showAddHabitModal = true}
                >
                    Add New Habit
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-4">
        <!-- Tabs Navigation -->
        <div class="flex border-b border-gray-700 mb-6">
            <button 
                class="px-4 py-2 font-medium {$activeTab === 'dashboard' ? 'border-b-2 border-indigo-500 text-white' : 'text-gray-400 hover:text-white'}"
                on:click={() => $activeTab = 'dashboard'}
            >
                Dashboard
            </button>
            <button 
                class="px-4 py-2 font-medium {$activeTab === 'weekly' ? 'border-b-2 border-indigo-500 text-white' : 'text-gray-400 hover:text-white'}"
                on:click={() => $activeTab = 'weekly'}
            >
                Weekly Planner
            </button>
            <button 
                class="px-4 py-2 font-medium {$activeTab === 'analytics' ? 'border-b-2 border-indigo-500 text-white' : 'text-gray-400 hover:text-white'}"
                on:click={() => $activeTab = 'analytics'}
            >
                Analytics
            </button>
        </div>

        <!-- Dashboard Tab -->
        {#if $activeTab === 'dashboard'}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Feature 1: Daily Habit Tracker Grid with Streaks -->
                <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                    <h2 class="text-xl font-bold mb-4">Today's Habits</h2>
                    
                    {#each $habits as habit (habit.id)}
                        <div class="mb-4 p-4 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors">
                            <div class="flex justify-between items-center">
                                <div>
                                    <h3 class="font-semibold text-lg">{habit.name}</h3>
                                    <p class="text-sm text-gray-400">{habit.description}</p>
                                </div>
                                
                                <!-- Checkbox to mark habit completion -->
                                <button 
                                    class="w-8 h-8 rounded-full flex items-center justify-center transition-all {isCompletedToday(habit) ? 'bg-green-500 text-white' : 'bg-gray-600 text-gray-300'}"
                                    on:click={() => toggleHabitCompletion(habit.id)}
                                >
                                    {#if isCompletedToday(habit)}
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                                        </svg>
                                    {/if}
                                </button>
                            </div>
                            
                            <!-- Streak counter -->
                            <div class="mt-2 flex items-center text-sm">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500 mr-1" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" />
                                </svg>
                                <span>{habit.streakCount} day streak</span>
                                
                                <!-- Feature 6: Milestone Badges -->
                                {#if habit.streakCount >= 7}
                                    <span class="ml-2 px-2 py-1 bg-indigo-600 rounded-full text-xs">Week 1 🎉</span>
                                {/if}
                                {#if habit.streakCount >= 21}
                                    <span class="ml-2 px-2 py-1 bg-purple-600 rounded-full text-xs">21 Days 🔥</span>
                                {/if}
                                {#if habit.streakCount >= 60}
                                    <span class="ml-2 px-2 py-1 bg-amber-600 rounded-full text-xs">60 Days 🏆</span>
                                {/if}
                            </div>
                            
                            <!-- Feature 8: Momentum Score -->
                            <div class="mt-3">
                                <p class="text-xs text-gray-400 mb-1">Momentum Score</p>
                                <div class="w-full bg-gray-600 rounded-full h-2.5">
                                    <div 
                                        class="bg-gradient-to-r from-blue-500 to-indigo-600 h-2.5 rounded-full" 
                                        style="width: {calculateMomentumScore(habit)}%"
                                    ></div>
                                </div>
                            </div>
                        </div>
                    {/each}
                    
                    {#if $habits.length === 0}
                        <p class="text-gray-400 text-center py-4">No habits created yet. Click "Add New Habit" to get started!</p>
                    {/if}
                </div>

                <!-- Feature 7: Weekly Planning Preview -->
                <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold">Weekly Schedule</h2>
                        <button 
                            class="text-sm text-indigo-400 hover:text-indigo-300"
                            on:click={() => $activeTab = 'weekly'}
                        >
                            View Full Calendar
                        </button>
                    </div>
                    
                    <div class="grid grid-cols-7 gap-1 text-center mb-2">
                        {#each ['S', 'M', 'T', 'W', 'T', 'F', 'S'] as day}
                            <div class="text-xs text-gray-400">{day}</div>
                        {/each}
                    </div>
                    
                    {#each $habits as habit (habit.id)}
                        <div class="mb-3">
                            <p class="text-sm mb-1 truncate">{habit.name}</p>
                            <div class="grid grid-cols-7 gap-1">
                                {#each Array(7).fill(0).map((_, i) => i) as dayIndex}
                                    <div 
                                        class="h-6 rounded-sm border {habit.targetDays.includes(dayIndex) ? 'border-indigo-500 bg-indigo-900/30' : 'border-gray-700 bg-gray-800/30'}"
                                    ></div>
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- Feature 5: Habit Loop Breakdown -->
                <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                    <h2 class="text-xl font-bold mb-4">Habit Loop Design</h2>
                    
                    {#if $habits.length > 0}
                        {#each $habits.slice(0, 1) as habit (habit.id)}
                            <div class="mb-4">
                                <h3 class="font-semibold text-lg mb-3">{habit.name}</h3>
                                
                                <div class="flex justify-between gap-3 mb-2">
                                    <!-- Cue -->
                                    <div class="flex-1 bg-gray-700/50 rounded-lg p-3">
                                        <p class="text-xs text-indigo-400 font-medium">CUE</p>
                                        <p class="mt-1">{habit.cue}</p>
                                    </div>
                                    
                                    <!-- Action -->
                                    <div class="flex-1 bg-gray-700/50 rounded-lg p-3">
                                        <p class="text-xs text-green-400 font-medium">ACTION</p>
                                        <p class="mt-1">{habit.action}</p>
                                    </div>
                                    
                                    <!-- Reward -->
                                    <div class="flex-1 bg-gray-700/50 rounded-lg p-3">
                                        <p class="text-xs text-amber-400 font-medium">REWARD</p>
                                        <p class="mt-1">{habit.reward}</p>
                                    </div>
                                </div>
                            </div>
                        {/each}
                        
                        <div class="flex justify-center mt-4">
                            <button 
                                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors"
                                on:click={() => $selectedHabit = $habits[0]}
                            >
                                Edit Habit Loop
                            </button>
                        </div>
                        
                        <!-- Feature 4: Habit Stacking Suggestions -->
                        <div class="mt-6 border-t border-gray-700 pt-4">
                            <h3 class="text-lg font-medium mb-3">Habit Stacking Suggestions</h3>
                            
                            <div class="bg-gray-700/30 rounded-lg p-3">
                                <p class="text-sm">After <span class="text-indigo-400">{$habits[0].name}</span>, try:</p>
                                <ul class="mt-2 space-y-2">
                                    <li class="flex items-center gap-2">
                                        <span class="w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
                                        <span>Drink a glass of water</span>
                                    </li>
                                    <li class="flex items-center gap-2">
                                        <span class="w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
                                        <span>Journal for 2 minutes</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    {:else}
                        <p class="text-gray-400 text-center py-4">Add your first habit to see the habit loop design!</p>
                    {/if}
                </div>
            </div>
            
            <!-- Feature 3: Reflection Section -->
            <div class="mt-8 bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold">Weekly Reflection</h2>
                    <button 
                        class="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
                        on:click={() => $showReflectionModal = true}
                    >
                        Add Reflection
                    </button>
                </div>
                
                {#if $habits.some(h => h.reflections && h.reflections.length > 0)}
                    <div class="space-y-4">
                        {#each $habits as habit (habit.id)}
                            {#if habit.reflections && habit.reflections.length > 0}
                                {#each habit.reflections as reflection}
                                    <div class="bg-gray-700/30 rounded-lg p-4">
                                        <div class="flex justify-between mb-2">
                                            <p class="font-semibold">{habit.name}</p>
                                            <p class="text-xs text-gray-400">{reflection.date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</p>
                                        </div>
                                        <p class="text-gray-300">{reflection.text}</p>
                                    </div>
                                {/each}
                            {/if}
                        {/each}
                    </div>
                {:else}
                    <p class="text-gray-400 text-center py-4">No reflections yet. Add your first reflection to track your habit journey!</p>
                {/if}
            </div>
            
            <!-- Feature 10: Automatic Habit Review Preview -->
            <div class="mt-8 bg-indigo-900/30 rounded-xl p-6 border border-indigo-800 shadow-lg">
                <div class="flex items-start">
                    <div class="flex-shrink-0 bg-indigo-600 rounded-lg p-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    
                    <div class="ml-4">
                        <h2 class="text-xl font-bold mb-2">Weekly Review Available</h2>
                        <p class="text-gray-300">Get insights on your progress and suggestions for improvement.</p>
                        
                        <button 
                            class="mt-4 bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
                            on:click={() => $showReviewModal = true}
                        >
                            View Weekly Review
                        </button>
                    </div>
                </div>
            </div>
        {/if}
        
        <!-- Weekly Planning Tab -->
        {#if $activeTab === 'weekly'}
            <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                <h2 class="text-xl font-bold mb-6">Weekly Planner</h2>
                
                <!-- Days of week header -->
                <div class="grid grid-cols-7 gap-3 mb-4">
                    {#each ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] as day, index}
                        <div class="text-center p-2 rounded-lg {index === new Date().getDay() ? 'bg-indigo-900/50 font-medium' : ''}">{day}</div>
                    {/each}
                </div>
                
                <!-- Habit schedule grid -->
                {#each $habits as habit (habit.id)}
                    <div class="mb-6">
                        <div class="flex items-center mb-2">
                            <h3 class="font-medium">{habit.name}</h3>
                            <span class="ml-2 px-2 py-0.5 rounded-full text-xs bg-gray-700">{habit.streakCount} day streak</span>
                        </div>
                        
                        <div class="grid grid-cols-7 gap-3">
                            {#each Array(7).fill(0).map((_, i) => i) as dayIndex}
                                <div 
                                    class="border rounded-lg p-3 min-h-20 flex flex-col items-center justify-center cursor-pointer transition-all {habit.targetDays.includes(dayIndex) ? 'border-indigo-500 bg-indigo-900/30' : 'border-gray-700'}"
                                >
                                    {#if habit.targetDays.includes(dayIndex)}
                                        <div class="w-4 h-4 rounded-full bg-indigo-500 mb-2"></div>
                                        <span class="text-xs text-center">Scheduled</span>
                                    {:else}
                                        <div class="w-4 h-4 rounded-full border border-gray-500 mb-2"></div>
                                        <span class="text-xs text-gray-500 text-center">Tap to schedule</span>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
        
        <!-- Analytics Tab -->
        {#if $activeTab === 'analytics'}
            <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700 shadow-lg">
                <h2 class="text-xl font-bold mb-6">Habit Analytics</h2>
                
                <!-- Placeholder for charts - Feature 2 -->
                <div class="mb-8">
                    <h3 class="text-lg font-medium mb-3">Completion Rate</h3>
                    <div class="bg-gray-700/50 rounded-lg p-4 h-64 flex items-center justify-center">
                        <p class="text-gray-400">Chart visualization would go here.<br>Using Chart.js or similar library.</p>
                    </div>
                </div>
                
                <!-- Feature 9: Focus Mode Preview -->
                <div class="mt-8">
                    <h3 class="text-lg font-medium mb-3">Focus Sessions</h3>
                    <div class="bg-gray-700/30 rounded-lg p-6">
                        <div class="text-center">
                            <p class="text-2xl font-bold mb-2">Pomodoro Timer</p>
                            <p class="text-gray-400 mb-4">Focus on your habits with timed sessions</p>
                            
                            <div class="flex justify-center gap-4 mb-6">
                                <button class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors">
                                    25 min Focus
                                </button>
                                <button class="px-4 py-2 bg-indigo-600/50 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors">
                                    5 min Break
                                </button>
                            </div>
                            
                            <div class="text-sm text-gray-400">
                                <p>Focus mode blocks distractions and helps you stay on track</p>
                                <p>Link it to specific habits like "Deep Work" or "Reading"</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </main>
</div>

<!-- Modals -->
<!-- Add Habit Modal - Feature 5: Trigger → Action → Reward Tracker -->
{#if $showAddHabitModal}
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-gray-800 rounded-xl border border-gray-700 shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-bold">Create New Habit</h2>
                    <button 
                        class="text-gray-400 hover:text-white"
                        on:click={() => $showAddHabitModal = false}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                
                <!-- Habit Form -->
                <form on:submit|preventDefault={() => {
                    habits.update(habitsList => {
                        const newHabit = {
                            id: habitsList.length > 0 ? Math.max(...habitsList.map(h => h.id)) + 1 : 1,
                            name: document.getElementById('habit-name').value,
                            description: document.getElementById('habit-description').value,
                            cue: document.getElementById('habit-cue').value,
                            action: document.getElementById('habit-action').value,
                            reward: document.getElementById('habit-reward').value,
                            streakCount: 0,
                            completedDates: [],
                            targetDays: Array.from(document.querySelectorAll('input[name="targetDays"]:checked')).map(el => parseInt(el.value)),
                            reflections: []
                        };
                        return [...habitsList, newHabit];
                    });
                    $showAddHabitModal = false;
                }}>
                    <div class="space-y-4">
                        <!-- Basic Info -->
                        <div>
                            <label for="habit-name" class="block text-sm font-medium text-gray-300 mb-1">Habit Name</label>
                            <input 
                                type="text" 
                                id="habit-name" 
                                class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                placeholder="e.g. Morning Meditation"
                                required
                            />
                        </div>
                        
                        <div>
                            <label for="habit-description" class="block text-sm font-medium text-gray-300 mb-1">Description</label>
                            <textarea 
                                id="habit-description" 
                                rows="2" 
                                class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                placeholder="Brief description of your habit"
                            ></textarea>
                        </div>
                        
                        <!-- Habit Loop (Cue, Action, Reward) -->
                        <div class="border-t border-gray-700 pt-4 mt-6">
                            <h3 class="text-lg font-medium mb-4">Habit Loop Design</h3>
                            
                            <div>
                                <label for="habit-cue" class="block text-sm font-medium text-indigo-400 mb-1">Cue (What triggers this habit?)</label>
                                <input 
                                    type="text" 
                                    id="habit-cue" 
                                    class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                    placeholder="e.g. After brushing teeth"
                                    required
                                />
                                <p class="text-xs text-gray-400 mt-1">The cue is what reminds you to perform the habit</p>
                            </div>
                            
                            <div class="mt-4">
                                <label for="habit-action" class="block text-sm font-medium text-green-400 mb-1">Action (What will you do?)</label>
                                <input 
                                    type="text" 
                                    id="habit-action" 
                                    class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                    placeholder="e.g. Meditate for 10 minutes"
                                    required
                                />
                                <p class="text-xs text-gray-400 mt-1">Be specific about the exact action you'll take</p>
                            </div>
                            
                            <div class="mt-4">
                                <label for="habit-reward" class="block text-sm font-medium text-amber-400 mb-1">Reward (How will you reinforce this habit?)</label>
                                <input 
                                    type="text" 
                                    id="habit-reward" 
                                    class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                    placeholder="e.g. Cup of coffee after completion"
                                    required
                                />
                                <p class="text-xs text-gray-400 mt-1">The reward helps your brain associate positive feelings with this habit</p>
                            </div>
                        </div>
                        
                        <!-- Weekly Schedule -->
                        <div class="border-t border-gray-700 pt-4 mt-6">
                            <h3 class="text-lg font-medium mb-4">Weekly Schedule</h3>
                            <p class="text-sm text-gray-400 mb-4">Select the days you want to perform this habit:</p>
                            
                            <div class="grid grid-cols-7 gap-2">
                                {#each ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as day, i}
                                    <label class="flex flex-col items-center">
                                        <input type="checkbox" name="targetDays" value={i} class="sr-only peer" />
                                        <div class="w-10 h-10 rounded-lg flex items-center justify-center cursor-pointer border border-gray-600 peer-checked:bg-indigo-600 peer-checked:border-indigo-500 transition-colors">
                                            {day}
                                        </div>
                                    </label>
                                {/each}
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-8 flex justify-end gap-3">
                        <button 
                            type="button"
                            class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-md text-sm font-medium transition-colors"
                            on:click={() => $showAddHabitModal = false}
                        >
                            Cancel
                        </button>
                        <button 
                            type="submit"
                            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors"
                        >
                            Create Habit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
{/if}

<!-- Reflection Modal - Feature 3: Reflection Prompts -->
{#if $showReflectionModal}
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-gray-800 rounded-xl border border-gray-700 shadow-xl max-w-xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-bold">Habit Reflection</h2>
                    <button 
                        class="text-gray-400 hover:text-white"
                        on:click={() => $showReflectionModal = false}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                
                <!-- Reflection Form -->
                <form on:submit|preventDefault={() => {
                    const habitId = parseInt(document.getElementById('reflection-habit').value);
                    const reflectionText = document.getElementById('reflection-text').value;
                    
                    habits.update(habitsList => {
                        return habitsList.map(habit => {
                            if (habit.id === habitId) {
                                habit.reflections = [
                                    { date: new Date(), text: reflectionText },
                                    ...(habit.reflections || [])
                                ];
                            }
                            return habit;
                        });
                    });
                    $showReflectionModal = false;
                }}>
                    <div class="space-y-4">
                        <!-- Habit Selection -->
                        <div>
                            <label for="reflection-habit" class="block text-sm font-medium text-gray-300 mb-1">Select Habit</label>
                            <select 
                                id="reflection-habit" 
                                class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                required
                            >
                                {#each $habits as habit}
                                    <option value={habit.id}>{habit.name}</option>
                                {/each}
                            </select>
                        </div>
                        
                        <!-- Reflection Prompts -->
                        <div class="bg-gray-700/30 rounded-lg p-4 my-4">
                            <p class="text-sm font-medium mb-2">Reflection Prompts:</p>
                            <ul class="text-sm text-gray-300 space-y-2">
                                <li>• What worked well with this habit?</li>
                                <li>• What challenges did you face?</li>
                                <li>• How could you improve your habit performance?</li>
                                <li>• How did this habit make you feel?</li>
                            </ul>
                        </div>
                        
                        <!-- Reflection Text -->
                        <div>
                            <label for="reflection-text" class="block text-sm font-medium text-gray-300 mb-1">Your Reflection</label>
                            <textarea 
                                id="reflection-text" 
                                rows="5" 
                                class="w-full bg-gray-700 border-gray-600 rounded-md text-white px-3 py-2" 
                                placeholder="Share your thoughts and insights about this habit..."
                                required
                            ></textarea>
                        </div>
                    </div>
                    
                    <div class="mt-6 flex justify-end gap-3">
                        <button 
                            type="button"
                            class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-md text-sm font-medium transition-colors"
                            on:click={() => $showReflectionModal = false}
                        >
                            Cancel
                        </button>
                        <button 
                            type="submit"
                            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors"
                        >
                            Save Reflection
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
{/if}

<!-- Weekly Review Modal - Feature 10: Automatic Habit Review -->
{#if $showReviewModal}
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-gray-800 rounded-xl border border-gray-700 shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-bold">Weekly Habit Review</h2>
                    <button 
                        class="text-gray-400 hover:text-white"
                        on:click={() => $showReviewModal = false}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                
                <!-- Weekly Summary -->
                <div class="mb-8">
                    <div class="bg-indigo-900/30 rounded-xl p-5 border border-indigo-800 mb-6">
                        <h3 class="text-lg font-semibold mb-3">Summary: April 5 - April 12, 2025</h3>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                            <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                <p class="text-3xl font-bold text-green-500">78%</p>
                                <p class="text-sm text-gray-400">Habit Completion Rate</p>
                            </div>
                            
                            <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                <p class="text-3xl font-bold text-amber-500">5</p>
                                <p class="text-sm text-gray-400">Day Best Streak</p>
                            </div>
                            
                            <div class="bg-gray-800/50 rounded-lg p-4 text-center">
                                <p class="text-3xl font-bold text-indigo-500">3</p>
                                <p class="text-sm text-gray-400">Reflections Written</p>
                            </div>
                        </div>
                        
                        <div class="bg-gray-800/50 rounded-lg p-4">
                            <p class="font-medium mb-2">Key Insights:</p>
                            <ul class="text-gray-300 space-y-1">
                                <li>• You hit 78% of your goals this week - great job!</li>
                                <li>• Morning Meditation has a 5-day streak - keep it going!</li>
                                <li>• You missed your Workout habit 2 times - maybe adjust the schedule?</li>
                                <li>• Your reflections mention feeling more focused - mindfulness is working!</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Habit Breakdown -->
                <h3 class="text-lg font-semibold mb-3">Habit Breakdown</h3>
                
                {#each $habits as habit}
                    <div class="mb-4 p-4 bg-gray-700/30 rounded-lg">
                        <div class="flex justify-between">
                            <div>
                                <h4 class="font-medium">{habit.name}</h4>
                                <p class="text-sm text-gray-400">{habit.description}</p>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold">
                                    {Math.round((habit.completedDates.filter(date => {
                                        const sevenDaysAgo = new Date();
                                        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
                                        return date > sevenDaysAgo;
                                    }).length / 7) * 100)}%
                                </p>
                                <p class="text-xs text-gray-400">completion</p>
                            </div>
                        </div>
                        
                        <!-- Last 7 days grid -->
                        <div class="mt-3">
                            <p class="text-xs text-gray-400 mb-1">Last 7 days:</p>
                            <div class="flex gap-1">
                                {#each Array(7).fill(0).map((_, i) => {
                                    const date = new Date();
                                    date.setDate(date.getDate() - (6 - i));
                                    return {
                                        date: date,
                                        completed: habit.completedDates.some(d => d.toDateString() === date.toDateString())
                                    };
                                }) as day, i}
                                    <div class="w-8 h-8 rounded-md flex items-center justify-center text-xs {day.completed ? 'bg-green-700' : 'bg-gray-800'}" title={day.date.toLocaleDateString()}>
                                        {day.date.getDate()}
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </div>
                {/each}
                
                <!-- Next Week Goals -->
                <div class="mt-8 bg-indigo-900/30 rounded-lg p-5 border border-indigo-800">
                    <h3 class="text-lg font-semibold mb-3">Next Week's Goals</h3>
                    <ul class="space-y-3">
                        <li class="flex items-start gap-3">
                            <div class="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center text-xs">1</div>
                            <p>Increase your "Morning Meditation" streak to 10 days</p>
                        </li>
                        <li class="flex items-start gap-3">
                            <div class="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center text-xs">2</div>
                            <p>Write at least 2 reflections for "Read 20 Pages" habit</p>
                        </li>
                        <li class="flex items-start gap-3">
                            <div class="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center text-xs">3</div>
                            <p>Try habit stacking: Add "Drink water" after your "Workout" habit</p>
                        </li>
                    </ul>
                </div>
                
                <div class="mt-6 flex justify-end">
                    <button 
                        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md text-sm font-medium transition-colors"
                        on:click={() => $showReviewModal = false}
                    >
                        Close Review
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    /* Additional custom styles could go here if needed */
</style>