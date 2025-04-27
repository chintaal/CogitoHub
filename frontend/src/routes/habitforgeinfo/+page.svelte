<script>
  import HabitforgeLogo from '../../components/logos/habitforgeLogo.svelte';
  import HabitforgeIcon from '../../components/icons/habitforgeIcon.svelte';
</script>

<div class="bg-gradient-to-br from-indigo-900 via-purple-900 to-indigo-800 min-h-screen text-white">
  <!-- Hero Section -->
  <section class="container mx-auto px-4 pt-20 pb-16">
    <div class="flex flex-col items-center text-center mb-12">
      <div class="mb-6 transform hover:scale-105 transition-transform duration-500">
        <HabitforgeLogo size={80} showText={false} />
      </div>
      <h1 class="text-5xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 to-purple-200">
        Not a Habit Tracker. A Human Upgrade Engine.
      </h1>
      <p class="text-xl md:text-2xl text-indigo-200 max-w-3xl mx-auto italic">
        "Other apps help you cross off a to-do. HabitForge reprograms your behavior at the identity level."
      </p>
      <div class="mt-8">
        <a href="/habitforge" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors duration-300 shadow-lg hover:shadow-xl">
          Transform Your Habits
        </a>
      </div>
    </div>
  </section>

  <!-- Competitor Comparison -->
  <section class="bg-indigo-800/50 py-16">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold mb-12 text-center">Why <span class="text-indigo-300">HabitForge</span> Stands Apart</h2>
      
      <div class="grid md:grid-cols-3 gap-8 mb-12">
        <!-- Microsoft To Do -->
        <div class="bg-indigo-900/60 p-6 rounded-lg">
          <h3 class="text-2xl font-bold mb-4 text-gray-300">Microsoft To Do:</h3>
          <ul class="space-y-3 text-lg">
            <li class="flex items-center">
              <span class="text-xl mr-2">✅</span> Check.
            </li>
            <li class="flex items-center">
              <span class="text-xl mr-2">❌</span> Miss.
            </li>
            <li class="flex items-center">
              <span class="text-xl mr-2">🔁</span> Try again.
            </li>
          </ul>
          <p class="mt-4 text-indigo-200 font-medium">
            That's it. No progress. No growth. No feedback loop. Just task management wearing a productivity badge.
          </p>
        </div>
        
        <!-- Habitica -->
        <div class="bg-indigo-900/60 p-6 rounded-lg">
          <h3 class="text-2xl font-bold mb-4 text-gray-300">Habitica:</h3>
          <p class="text-lg mb-4">Gamified? Sure.</p>
          <p class="text-lg mb-4">But is leveling up your RPG avatar the same as leveling up <em>yourself</em>?</p>
          <p class="mt-4 text-indigo-200 font-medium">
            The cartoon dragons don't fix your 2AM doomscrolling. The pixel armor doesn't help you build that meditation habit.
          </p>
        </div>
        
        <!-- HabitForge -->
        <div class="bg-gradient-to-br from-indigo-600 to-purple-700 p-6 rounded-lg shadow-lg">
          <div class="flex items-center mb-4">
            <HabitforgeIcon size={30} />
            <h3 class="text-2xl font-bold ml-2">HabitForge:</h3>
          </div>
          <ul class="space-y-3 text-lg">
            <li class="flex items-center">
              <span class="text-xl mr-2">🧬</span> Identity-based habits
            </li>
            <li class="flex items-center">
              <span class="text-xl mr-2">📊</span> Visualized momentum
            </li>
            <li class="flex items-center">
              <span class="text-xl mr-2">🤖</span> AI-powered optimization
            </li>
            <li class="flex items-center">
              <span class="text-xl mr-2">🔄</span> Real habit loop building
            </li>
          </ul>
          <p class="mt-4 text-white font-medium">
            It's not about checkmarks. It's about transforming who you are—one small win at a time.
          </p>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Feature Comparison Table -->
  <section class="py-16">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold mb-12 text-center">What Makes <span class="text-indigo-300">HabitForge</span> Unstoppable</h2>
      
      <div class="overflow-x-auto">
        <table class="min-w-full bg-indigo-900/40 rounded-lg overflow-hidden">
          <thead>
            <tr class="border-b border-indigo-700">
              <th class="py-4 px-6 text-left text-lg">Feature</th>
              <th class="py-4 px-6 text-center text-lg">HabitForge</th>
              <th class="py-4 px-6 text-center text-lg">Microsoft To Do</th>
              <th class="py-4 px-6 text-center text-lg">Habitica</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b border-indigo-800">
              <td class="py-3 px-6">Identity-Driven Habits</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
            </tr>
            <tr class="border-b border-indigo-800">
              <td class="py-3 px-6">Streak Grid + Momentum</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
            </tr>
            <tr class="border-b border-indigo-800">
              <td class="py-3 px-6">Weekly/Monthly Visual Analytics</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
            </tr>
            <tr class="border-b border-indigo-800">
              <td class="py-3 px-6">AI-Powered Habit Optimization</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
            </tr>
            <tr class="border-b border-indigo-800">
              <td class="py-3 px-6">Keystone Habit Detection</td>
              <td class="py-3 px-6 text-center text-green-400">✅</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
              <td class="py-3 px-6 text-center text-red-400">❌</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Science Section -->
  <section class="bg-indigo-800/50 py-16">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row items-center md:items-start gap-8">
        <div class="md:w-1/2">
          <h2 class="text-3xl md:text-4xl font-bold mb-6">Your Mind is Software. <br>HabitForge is the IDE.</h2>
          <ul class="space-y-4 text-lg">
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Build habits like code modules</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Deploy routines with confidence</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Refactor your behavior in weekly sprints</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Debug failure loops with intelligent prompts</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Version-control your identity</span>
            </li>
          </ul>
        </div>
        <div class="md:w-1/2">
          <h2 class="text-3xl md:text-4xl font-bold mb-6">Based on Science. <br>Enhanced by AI.</h2>
          <ul class="space-y-4 text-lg">
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Cues. Routines. Rewards. Visualized.</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Behavioral analytics + smart habit loops</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>Weekly digest to show what worked (and why)</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-300 mr-2">→</span>
              <span>ChatGPT-powered suggestions to rewire broken patterns</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Taglines Section -->
  <section class="py-16">
    <div class="container mx-auto px-4 text-center">
      <h2 class="text-3xl md:text-4xl font-bold mb-12">Find Your Motivation</h2>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-indigo-800/50 p-6 rounded-lg hover:bg-indigo-700/60 transition-colors duration-300 hover:scale-105 transform duration-300">
          <p class="text-xl font-medium">"Build the person you were meant to be."</p>
        </div>
        <div class="bg-indigo-800/50 p-6 rounded-lg hover:bg-indigo-700/60 transition-colors duration-300 hover:scale-105 transform duration-300">
          <p class="text-xl font-medium">"Habits aren't goals. They're your future self, rehearsed daily."</p>
        </div>
        <div class="bg-indigo-800/50 p-6 rounded-lg hover:bg-indigo-700/60 transition-colors duration-300 hover:scale-105 transform duration-300">
          <p class="text-xl font-medium">"Forget checkboxes. Forge change."</p>
        </div>
        <div class="bg-indigo-800/50 p-6 rounded-lg hover:bg-indigo-700/60 transition-colors duration-300 hover:scale-105 transform duration-300">
          <p class="text-xl font-medium">"The OS for who you're becoming."</p>
        </div>
        <div class="bg-indigo-800/50 p-6 rounded-lg hover:bg-indigo-700/60 transition-colors duration-300 hover:scale-105 transform duration-300 md:col-span-2 lg:col-span-1">
          <p class="text-xl font-medium">"Craft routines. Transform identities. Repeat."</p>
        </div>
      </div>

      <div class="mt-16">
        <a href="/habitforge" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold py-4 px-10 rounded-lg text-xl transition-all duration-300 shadow-lg hover:shadow-xl">
          Start Your Transformation
        </a>
      </div>
    </div>
  </section>
</div>