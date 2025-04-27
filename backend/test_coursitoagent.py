#!/usr/bin/env python3
import os
import json
from app.core.coursitoagent import CoursitoAgent

def test_process_youtube_url():
    """Test the processing of a YouTube URL"""
    # Check if the API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        return
    
    # Sample YouTube URL (short educational video)
    url = "https://www.youtube.com/watch?v=PHe0bXAIuk0"  # "How The Economic Machine Works" by Ray Dalio (30 mins)
    
    print(f"Processing URL: {url}")
    agent = CoursitoAgent()
    
    try:
        # Process the URL
        result = agent.process_youtube_url(url)
        
        # Print the result
        print("\n=== TRANSCRIPT PREVIEW ===")
        print(result["transcript"][:200] + "...\n")
        
        print("=== NOTES PREVIEW ===")
        for note in result["notes"][:2]:
            print(f"- {note['title']}")
        print("...\n")
        
        print("=== FLASHCARDS PREVIEW ===")
        for card in result["flashcards"][:2]:
            print(f"Q: {card['question']}")
            print(f"A: {card['answer']}\n")
        print("...\n")
        
        # Save the full result to a file
        with open("coursitoagent_result.json", "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"Full result saved to coursitoagent_result.json")
        return True
    
    except Exception as e:
        print(f"Error processing URL: {str(e)}")
        return False

if __name__ == "__main__":
    test_result = test_process_youtube_url()
    print(f"\nTest {'successful' if test_result else 'failed'}")