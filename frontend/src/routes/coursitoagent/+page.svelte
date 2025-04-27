<script>
  import { onMount } from 'svelte';
  import { fade, fly, slide } from 'svelte/transition';
  import CoursitoLogo from '../../components/logos/coursitoLogo.svelte';

  // API configuration
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
  
  // State management
  let youtubeUrl = '';
  let isLoading = false;
  let errorMessage = '';
  let processingStatus = '';
  let apiAvailable = true;
  
  // Results
  let transcript = '';
  let notes = [];
  let flashcards = [];
  let questions = [];
  
  // UI state
  let activeTab = 'notes';
  let currentFlashcardIndex = 0;
  let showFlashcardAnswer = false;
  let selectedQuestionIndex = 0;
  let showQuestionExplanation = false;

  // Check if API is available on component mount
  onMount(async () => {
    try {
      // Simple health check to ensure API is reachable
      const response = await fetch(`${API_BASE_URL}/api/v1/coursito/process-youtube`, { 
        method: 'OPTIONS',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).catch(error => {
        console.error("API health check failed:", error);
        apiAvailable = false;
        return { ok: false };
      });
      
      apiAvailable = response.ok;
    } catch (error) {
      console.error("API connectivity error:", error);
      apiAvailable = false;
    }
  });
  
  async function processYoutubeVideo() {
    if (!youtubeUrl) {
      errorMessage = 'Please enter a YouTube URL';
      return;
    }
    
    try {
      isLoading = true;
      processingStatus = 'Downloading and processing video... (this may take a few minutes)';
      errorMessage = '';
      
      // Make sure URL is properly formatted
      let cleanUrl = youtubeUrl;
      if (!cleanUrl.startsWith('http://') && !cleanUrl.startsWith('https://')) {
        cleanUrl = 'https://' + cleanUrl;
      }
      
      const response = await fetch(`${API_BASE_URL}/api/v1/coursito/process-youtube`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ url: cleanUrl })
      });
      
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          errorData = { detail: `Server error (${response.status})` };
        }
        throw new Error(errorData.detail || `Failed to process YouTube video: ${response.statusText}`);
      }
      
      const result = await response.json();
      
      transcript = result.transcript;
      notes = result.notes;
      flashcards = result.flashcards;
      questions = result.questions || [];
      
      // Reset UI states
      activeTab = 'notes';
      currentFlashcardIndex = 0;
      showFlashcardAnswer = false;
      selectedQuestionIndex = 0;
      showQuestionExplanation = false;
      
    } catch (error) {
      console.error('Error processing YouTube video:', error);
      errorMessage = error.message || 'Failed to connect to the server. Please check your network connection and try again.';
    } finally {
      isLoading = false;
      processingStatus = '';
    }
  }
  
  function nextFlashcard() {
    if (currentFlashcardIndex < flashcards.length - 1) {
      currentFlashcardIndex++;
      showFlashcardAnswer = false;
    }
  }
  
  function prevFlashcard() {
    if (currentFlashcardIndex > 0) {
      currentFlashcardIndex--;
      showFlashcardAnswer = false;
    }
  }
  
  function toggleFlashcardAnswer() {
    showFlashcardAnswer = !showFlashcardAnswer;
  }
  
  function nextQuestion() {
    if (selectedQuestionIndex < questions.length - 1) {
      selectedQuestionIndex++;
      showQuestionExplanation = false;
    }
  }
  
  function prevQuestion() {
    if (selectedQuestionIndex > 0) {
      selectedQuestionIndex--;
      showQuestionExplanation = false;
    }
  }
  
  function toggleQuestionExplanation() {
    showQuestionExplanation = !showQuestionExplanation;
  }
  
  function getAlphabetLetter(index) {
    return String.fromCharCode(97 + index); // 97 is ASCII for 'a'
  }
</script>

<svelte:head>
  <title>Coursito Agent | Learn from YouTube Videos</title>
</svelte:head>

<main class="min-h-screen bg-gradient-to-b from-white to-gray-50 text-gray-900">
  <div class="background-decoration">
    <div class="bg-blob-1"></div>
    <div class="bg-blob-2"></div>
    <div class="bg-blob-3"></div>
  </div>

  <header in:fly={{ y: -20, duration: 500 }}>
    <div class="header-content">
      <div class="logo-container">
        <CoursitoLogo size={70} src="src/assets/Logos/coursito-full.png" />
        <div class="title-container">
          <h1 class="gradient-text">Coursito Agent</h1>
          <p class="subtitle">Transform YouTube videos into comprehensive learning materials</p>
        </div>
      </div>
    </div>
  </header>
  
  <section class="input-section" in:fly={{ y: -10, duration: 600, delay: 200 }}>
    <div class="card">
      <div class="card-content">
        <h2>Enter a YouTube URL</h2>
        <p class="card-description">The Coursito Agent will download and process the video to create personalized learning materials.</p>
        
        {#if !apiAvailable}
          <div class="api-status-warning" in:fade={{ duration: 200 }}>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>Server connection issue: Make sure the API server is running at <code>{API_BASE_URL}</code></span>
          </div>
        {/if}
        
        <form on:submit|preventDefault={processYoutubeVideo}>
          <div class="input-group">
            <input 
              type="url" 
              bind:value={youtubeUrl} 
              placeholder="https://www.youtube.com/watch?v=..." 
              disabled={isLoading}
              class="url-input"
            />
            <button type="submit" disabled={isLoading || !apiAvailable} class="primary-button">
              {#if isLoading}
                <span class="button-spinner"></span>
                <span>Processing...</span>
              {:else}
                <span>Process Video</span>
              {/if}
            </button>
          </div>
          
          {#if errorMessage}
            <div class="error-message" in:fade={{ duration: 200 }}>
              {errorMessage}
            </div>
          {/if}
          
          {#if processingStatus}
            <div class="processing-status" in:fade={{ duration: 200 }}>
              <div class="spinner"></div>
              <p>{processingStatus}</p>
            </div>
          {/if}
        </form>
      </div>
    </div>
  </section>
  
  {#if transcript || notes.length > 0 || flashcards.length > 0 || questions.length > 0}
    <section class="results-section" in:fly={{ y: 20, duration: 800, delay: 300 }}>
      <div class="tabs">
        <button 
          class:active={activeTab === 'notes'} 
          on:click={() => activeTab = 'notes'}
        >
          <span>Notes</span>
        </button>
        <button 
          class:active={activeTab === 'flashcards'} 
          on:click={() => activeTab = 'flashcards'}
        >
          <span>Flashcards</span>
        </button>
        <button 
          class:active={activeTab === 'questions'} 
          on:click={() => activeTab = 'questions'}
        >
          <span>Question Bank</span>
        </button>
        <button 
          class:active={activeTab === 'transcript'} 
          on:click={() => activeTab = 'transcript'}
        >
          <span>Transcript</span>
        </button>
      </div>
      
      <div class="tab-content">
        {#if activeTab === 'notes'}
          <div class="notes-container">
            {#if notes.length === 0}
              <div class="empty-state">
                <p>No notes available yet.</p>
              </div>
            {:else}
              {#each notes as note, i}
                <div class="note-card" in:fly={{ y: 20, duration: 300, delay: i * 100 }}>
                  <h3>{note.title}</h3>
                  <div class="note-content">
                    {#each note.content.split('\n') as paragraph}
                      <p>{paragraph}</p>
                    {/each}
                  </div>
                </div>
              {/each}
            {/if}
          </div>
        {:else if activeTab === 'flashcards'}
          <div class="flashcards-container">
            {#if flashcards.length === 0}
              <div class="empty-state">
                <p>No flashcards available yet.</p>
              </div>
            {:else}
              <div class="flashcard-navigation">
                <span class="card-count">Card {currentFlashcardIndex + 1} of {flashcards.length}</span>
                <div class="navigation-buttons">
                  <button on:click={prevFlashcard} disabled={currentFlashcardIndex === 0} class="nav-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M15 18l-6-6 6-6"/></svg>
                    <span>Previous</span>
                  </button>
                  <button on:click={nextFlashcard} disabled={currentFlashcardIndex === flashcards.length - 1} class="nav-button">
                    <span>Next</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M9 18l6-6-6-6"/></svg>
                  </button>
                </div>
              </div>
              
              <div class="flashcard" on:click={toggleFlashcardAnswer}>
                <div class="flashcard-inner" class:flipped={showFlashcardAnswer}>
                  <div class="flashcard-front">
                    <div class="flashcard-label">Question</div>
                    <p class="flashcard-content">{flashcards[currentFlashcardIndex].question}</p>
                    <div class="flashcard-hint">Tap to reveal answer</div>
                  </div>
                  <div class="flashcard-back">
                    <div class="flashcard-label">Answer</div>
                    <p class="flashcard-content">{flashcards[currentFlashcardIndex].answer}</p>
                    <div class="flashcard-hint">Tap to hide answer</div>
                  </div>
                </div>
              </div>
            {/if}
          </div>
        {:else if activeTab === 'questions'}
          <div class="questions-container">
            {#if questions.length === 0}
              <div class="empty-state">
                <p>No questions available yet.</p>
              </div>
            {:else}
              <div class="question-navigation">
                <span class="card-count">Question {selectedQuestionIndex + 1} of {questions.length}</span>
                <div class="navigation-buttons">
                  <button on:click={prevQuestion} disabled={selectedQuestionIndex === 0} class="nav-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M15 18l-6-6 6-6"/></svg>
                    <span>Previous</span>
                  </button>
                  <button on:click={nextQuestion} disabled={selectedQuestionIndex === questions.length - 1} class="nav-button">
                    <span>Next</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M9 18l6-6-6-6"/></svg>
                  </button>
                </div>
              </div>
              
              <div class="question-card">
                <div class="question-type-badge">{questions[selectedQuestionIndex].type}</div>
                <h3 class="question-text">{questions[selectedQuestionIndex].question}</h3>
                
                {#if questions[selectedQuestionIndex].type === 'multiple-choice' && questions[selectedQuestionIndex].options}
                  <div class="options-list">
                    {#each questions[selectedQuestionIndex].options as option, i}
                      <div class="option" 
                          class:correct={showQuestionExplanation && 
                                        questions[selectedQuestionIndex].correct_answer === option}>
                        <span class="option-letter">{getAlphabetLetter(i)}</span> 
                        <span class="option-text">{option}</span>
                        {#if showQuestionExplanation && questions[selectedQuestionIndex].correct_answer === option}
                          <span class="option-correct-mark">✓</span>
                        {/if}
                      </div>
                    {/each}
                  </div>
                {:else if questions[selectedQuestionIndex].type === 'true-false'}
                  <div class="options-list">
                    <div class="option" 
                        class:correct={showQuestionExplanation && 
                                      questions[selectedQuestionIndex].correct_answer === 'True'}>
                        <span class="option-letter">a</span>
                        <span class="option-text">True</span>
                        {#if showQuestionExplanation && questions[selectedQuestionIndex].correct_answer === 'True'}
                          <span class="option-correct-mark">✓</span>
                        {/if}
                    </div>
                    <div class="option"
                        class:correct={showQuestionExplanation && 
                                      questions[selectedQuestionIndex].correct_answer === 'False'}>
                        <span class="option-letter">b</span>
                        <span class="option-text">False</span>
                        {#if showQuestionExplanation && questions[selectedQuestionIndex].correct_answer === 'False'}
                          <span class="option-correct-mark">✓</span>
                        {/if}
                    </div>
                  </div>
                {/if}
                
                <div class="question-actions">
                  <button class="reveal-button" on:click={toggleQuestionExplanation}>
                    {showQuestionExplanation ? 'Hide Answer' : 'Show Answer'}
                  </button>
                </div>
                
                {#if showQuestionExplanation}
                  <div class="question-explanation" in:slide={{duration: 300}}>
                    <div class="explanation-title">
                      <span>Correct Answer:</span> 
                      <span class="correct-text">{questions[selectedQuestionIndex].correct_answer}</span>
                    </div>
                    <p class="explanation-content">{questions[selectedQuestionIndex].explanation}</p>
                  </div>
                {/if}
              </div>
            {/if}
          </div>
        {:else if activeTab === 'transcript'}
          <div class="transcript-container">
            {#if !transcript}
              <div class="empty-state">
                <p>No transcript available yet.</p>
              </div>
            {:else}
              <div class="transcript-content">
                {#each transcript.split('\n\n') as paragraph}
                  <p>{paragraph}</p>
                {/each}
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </section>
  {/if}
</main>

<style>
  /* Base styles */
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    padding: 0;
    line-height: 1.5;
  }
  
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    position: relative;
    overflow-x: hidden;
  }
  
  /* Background decorations */
  .background-decoration {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
    opacity: 0.8;
  }
  
  .bg-blob-1 {
    position: absolute;
    top: -10%;
    right: -10%;
    width: 60vw;
    height: 60vw;
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(135, 206, 235, 0.15) 0%, rgba(135, 206, 235, 0) 70%);
    filter: blur(50px);
    animation: float 20s ease-in-out infinite alternate;
  }
  
  .bg-blob-2 {
    position: absolute;
    bottom: -10%;
    left: -10%;
    width: 70vw;
    height: 70vw;
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(147, 112, 219, 0.15) 0%, rgba(147, 112, 219, 0) 70%);
    filter: blur(60px);
    animation: float 15s ease-in-out infinite alternate-reverse;
  }
  
  .bg-blob-3 {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 50vw;
    height: 50vw;
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0) 70%);
    filter: blur(40px);
    animation: pulse 10s ease-in-out infinite;
  }
  
  @keyframes float {
    0% { transform: translate(0, 0) rotate(0deg); }
    100% { transform: translate(2%, 2%) rotate(5deg); }
  }
  
  @keyframes pulse {
    0%, 100% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.7; }
    50% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.9; }
  }
  
  /* Header styles */
  header {
    margin-bottom: 2rem;
    padding: 1rem 0;
  }
  
  .header-content {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .logo-container {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .title-container {
    display: flex;
    flex-direction: column;
  }
  
  h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    line-height: 1.1;
  }
  
  .gradient-text {
    background: linear-gradient(135deg, #4f6df5 0%, #a835ec 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #6e6e73;
    margin: 0.5rem 0 0 0;
  }
  
  /* Card styles */
  .card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  }
  
  .card h2 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
    color: #1d1d1f;
  }
  
  .card-description {
    font-size: 1.1rem;
    color: #6e6e73;
    margin-bottom: 1.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  
  /* Form elements */
  .input-group {
    display: flex;
    gap: 10px;
    margin-top: 1.5rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .url-input {
    flex: 1;
    padding: 16px 20px;
    font-size: 1rem;
    background: #f5f5f7;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    transition: all 0.3s;
    color: #1d1d1f;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  }
  
  .url-input:focus {
    outline: none;
    border-color: #4f6df5;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(79, 109, 245, 0.2);
  }
  
  .primary-button {
    padding: 0 24px;
    font-size: 1rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4f6df5 0%, #a835ec 100%);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-width: 160px;
  }
  
  .primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 109, 245, 0.3);
  }
  
  .primary-button:active {
    transform: translateY(0);
  }
  
  .primary-button:disabled {
    background: #d1d1d6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  .button-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 2px solid white;
    animation: spin 0.8s linear infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  /* Status messages */
  .error-message {
    color: #ff453a;
    margin-top: 1rem;
    padding: 0.75rem;
    background: rgba(255, 69, 58, 0.1);
    border-radius: 12px;
    font-size: 0.95rem;
    animation: fade-in 0.3s ease;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .processing-status {
    display: flex;
    align-items: center;
    margin-top: 1rem;
    padding: 0.75rem;
    background: rgba(10, 132, 255, 0.1);
    border-radius: 12px;
    gap: 12px;
    animation: fade-in 0.3s ease;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .spinner {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(0, 122, 255, 0.3);
    border-radius: 50%;
    border-top-color: #0a84ff;
    animation: spin 1s linear infinite;
  }
  
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  /* Tab navigation */
  .tabs {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
    gap: 8px;
    justify-content: center;
  }
  
  .tabs button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    color: #1d1d1f;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  
  .tabs button:hover {
    background: rgba(255, 255, 255, 0.8);
    transform: translateY(-2px);
  }
  
  .tabs button.active {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    color: #4f6df5;
    font-weight: 600;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    transform: translateY(-3px);
  }
  
  /* Tab content */
  .tab-content {
    padding: 2rem;
    min-height: 400px;
    transition: all 0.3s ease;
    border-radius: 20px;
    margin-bottom: 4rem;
    background: white;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  /* Empty state */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem;
    color: #8e8e93;
  }
  
  /* Notes styling */
  .notes-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .note-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 4px solid #4f6df5;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  }
  
  .note-card:hover {
    transform: translateX(5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  }
  
  .note-card h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #1d1d1f;
    font-size: 1.4rem;
    font-weight: 600;
  }
  
  .note-content {
    color: #424245;
    line-height: 1.6;
    font-size: 1.05rem;
  }
  
  .note-content p {
    margin-bottom: 0.8rem;
  }
  
  /* Flashcard styling */
  .flashcards-container,
  .questions-container {
    padding: 1rem 0;
  }
  
  .flashcard-navigation,
  .question-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .card-count {
    font-size: 0.95rem;
    color: #8e8e93;
    font-weight: 500;
  }
  
  .navigation-buttons {
    display: flex;
    gap: 12px;
  }
  
  .nav-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.05);
    padding: 8px 16px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    color: #1d1d1f;
    font-weight: 500;
  }
  
  .nav-button:hover:not(:disabled) {
    background: #f5f5f7;
    transform: translateY(-2px);
  }
  
  .nav-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .nav-icon {
    width: 16px;
    height: 16px;
  }
  
  .flashcard {
    perspective: 2000px;
    height: 360px;
    cursor: pointer;
    margin-bottom: 2rem;
  }
  
  .flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s cubic-bezier(0.645, 0.045, 0.355, 1);
    transform-style: preserve-3d;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }
  
  .flashcard-inner.flipped {
    transform: rotateY(180deg);
  }
  
  .flashcard-front, .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 20px;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
  }
  
  .flashcard-front {
    background: linear-gradient(135deg, #fff 0%, #f5f5f7 100%);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .flashcard-back {
    background: linear-gradient(135deg, #f5f5f7 0%, #e1e1e6 100%);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transform: rotateY(180deg);
  }
  
  .flashcard-label {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #4f6df5;
    margin-bottom: 1.5rem;
    font-weight: 600;
  }
  
  .flashcard-content {
    flex: 1;
    font-size: 1.3rem;
    line-height: 1.5;
    color: #1d1d1f;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin: 0;
  }
  
  .flashcard-hint {
    text-align: center;
    font-size: 0.9rem;
    color: #8e8e93;
    margin-top: 1.5rem;
    font-weight: 500;
  }
  
  /* Question bank styling */
  .question-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .question-type-badge {
    position: absolute;
    top: -12px;
    left: 24px;
    background: linear-gradient(135deg, #4f6df5 0%, #a835ec 100%);
    color: white;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .question-text {
    font-size: 1.3rem;
    margin: 1rem 0 2rem;
    line-height: 1.5;
    color: #1d1d1f;
  }
  
  .options-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 2rem;
  }
  
  .option {
    display: flex;
    align-items: center;
    background: #f5f5f7;
    padding: 16px;
    border-radius: 12px;
    border-left: 3px solid transparent;
    transition: all 0.3s;
  }
  
  .option:hover {
    transform: translateX(5px);
    background: #eeeeef;
  }
  
  .option.correct {
    border-left: 3px solid #30d158;
    background: rgba(48, 209, 88, 0.1);
  }
  
  .option-letter {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: white;
    border-radius: 50%;
    margin-right: 12px;
    font-weight: 600;
    color: #4f6df5;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .option-text {
    flex: 1;
    color: #1d1d1f;
  }
  
  .option-correct-mark {
    margin-left: 12px;
    color: #30d158;
    font-size: 1.2rem;
  }
  
  .question-actions {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0;
  }
  
  .reveal-button {
    background: linear-gradient(135deg, #4f6df5 0%, #a835ec 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .reveal-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(79, 109, 245, 0.3);
  }
  
  .question-explanation {
    background: #f5f5f7;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .explanation-title {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
    font-weight: 600;
    color: #1d1d1f;
  }
  
  .correct-text {
    color: #30d158;
    font-weight: 700;
  }
  
  .explanation-content {
    color: #424245;
    line-height: 1.6;
    margin: 0;
    font-size: 1.05rem;
  }
  
  /* Transcript styling */
  .transcript-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #d1d1d6 #f5f5f7;
  }
  
  .transcript-container::-webkit-scrollbar {
    width: 8px;
  }
  
  .transcript-container::-webkit-scrollbar-track {
    background: #f5f5f7;
    border-radius: 10px;
  }
  
  .transcript-container::-webkit-scrollbar-thumb {
    background-color: #d1d1d6;
    border-radius: 10px;
  }
  
  .transcript-content {
    line-height: 1.7;
    color: #424245;
    font-size: 1.05rem;
  }
  
  .transcript-content p {
    margin-bottom: 1.2rem;
  }
  
  .api-status-warning {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem auto;
    padding: 0.75rem 1rem;
    background: rgba(255, 204, 0, 0.1);
    border: 1px solid rgba(255, 204, 0, 0.3);
    color: #ff9500;
    border-radius: 12px;
    font-size: 0.95rem;
    max-width: 800px;
  }
  
  .api-status-warning code {
    background: rgba(255, 255, 255, 0.2);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.9em;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    h1 {
      font-size: 2.2rem;
    }
    
    .input-group {
      flex-direction: column;
    }
    
    .url-input, .primary-button {
      width: 100%;
    }
    
    .tabs {
      flex-wrap: wrap;
      gap: 8px;
    }
    
    .tabs button {
      flex: 1;
      min-width: 45%;
      padding: 10px;
    }
    
    .card, .tab-content {
      padding: 1.5rem;
    }
    
    .flashcard {
      height: 280px;
    }
    
    .flashcard-front, .flashcard-back {
      padding: 1.5rem;
    }
    
    .logo-container {
      flex-direction: column;
      align-items: center;
      text-align: center;
      margin-bottom: 1rem;
    }
    
    .header-content {
      flex-direction: column;
    }
  }
</style>