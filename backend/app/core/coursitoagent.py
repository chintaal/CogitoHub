import os
import json
import tempfile
import subprocess
import time
from typing import Dict, Any, List, Optional, Tuple
import openai
import logging
from dotenv import load_dotenv
from pathlib import Path
import math
from pydub import AudioSegment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoursitoAgent:
    """
    CoursitoAgent handles YouTube video processing:
    - Downloads audio from YouTube URLs using yt-dlp
    - Transcribes audio using GPT-4o
    - Generates notes and flashcards from the transcript
    """
    
    def __init__(self):
        """Initialize the CoursitoAgent with API key from environment variables or .env file"""
        # Try to load API key from environment first
        self.api_key = os.environ.get("OPENAI_API_KEY")
        
        # If not found in environment, try to load from .env file
        if not self.api_key:
            logger.info("OpenAI API key not found in environment variables, checking .env file")
            # Try different possible locations for the .env file
            env_paths = [
                Path(__file__).parent.parent.parent.parent / ".env",  # /backend/app/core -> /backend/.env
                Path(__file__).parent.parent.parent.parent.parent / ".env",  # /backend/app/core -> /.env
            ]
            
            for env_path in env_paths:
                if env_path.exists():
                    logger.info(f"Found .env file at {env_path}")
                    load_dotenv(dotenv_path=env_path)
                    self.api_key = os.environ.get("OPENAI_API_KEY")
                    if self.api_key:
                        logger.info("Successfully loaded OpenAI API key from .env file")
                        break
        
        if not self.api_key:
            logger.warning("OpenAI API key not found in environment variables or .env file")
        else:
            openai.api_key = self.api_key
            
    def download_audio(self, url: str) -> str:
        """
        Download audio from a YouTube URL using yt-dlp
        
        Args:
            url: YouTube URL
            
        Returns:
            Path to the downloaded audio file
        """
        logger.info(f"Downloading audio from URL: {url}")
        
        # Create a temporary directory for the audio file
        temp_dir = tempfile.mkdtemp()
        output_file = os.path.join(temp_dir, "audio.mp3")
        
        try:
            # Use yt-dlp to download the audio
            command = [
                "yt-dlp",
                "-x",                      # Extract audio
                "--audio-format", "mp3",   # Convert to mp3
                "--audio-quality", "0",    # Best quality
                "--no-playlist",           # Don't download playlists if URL is part of one
                "-o", output_file,         # Output file
                url                        # URL to download from
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(f"Download complete: {output_file}")
            return output_file
        
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading audio: {e.stderr}")
            raise RuntimeError(f"Failed to download audio: {e.stderr}")
            
    def split_audio_file(self, audio_file_path: str, max_size_mb: int = 24) -> List[str]:
        """
        Split an audio file into smaller chunks to avoid payload size limits
        
        Args:
            audio_file_path: Path to the audio file
            max_size_mb: Maximum size of each chunk in MB (default: 24MB to stay under the 25MB limit)
            
        Returns:
            List of paths to the audio chunks
        """
        logger.info(f"Splitting audio file: {audio_file_path}")
        
        # Get file size
        file_size = os.path.getsize(audio_file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # If file is already small enough, return it as is
        if file_size_mb <= max_size_mb:
            logger.info("Audio file is small enough, no splitting needed")
            return [audio_file_path]
        
        # Calculate number of chunks needed
        num_chunks = math.ceil(file_size_mb / max_size_mb)
        logger.info(f"Splitting audio into {num_chunks} chunks (file size: {file_size_mb:.2f} MB)")
        
        # Load the audio file
        audio = AudioSegment.from_mp3(audio_file_path)
        
        # Calculate duration of each chunk
        total_duration_ms = len(audio)
        chunk_duration_ms = total_duration_ms // num_chunks
        
        # Create chunks
        chunk_files = []
        temp_dir = os.path.dirname(audio_file_path)
        
        for i in range(num_chunks):
            start_time = i * chunk_duration_ms
            end_time = (i + 1) * chunk_duration_ms if i < num_chunks - 1 else total_duration_ms
            
            # Extract chunk
            chunk = audio[start_time:end_time]
            
            # Save chunk to file
            chunk_path = os.path.join(temp_dir, f"audio_chunk_{i+1}.mp3")
            chunk.export(chunk_path, format="mp3")
            chunk_files.append(chunk_path)
            
            chunk_size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
            logger.info(f"Created chunk {i+1}/{num_chunks}, size: {chunk_size_mb:.2f} MB")
        
        return chunk_files
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper model with retry mechanism
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcription text
        """
        logger.info(f"Transcribing audio file: {audio_file_path}")
        
        # Check file size and split if necessary
        file_size = os.path.getsize(audio_file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # OpenAI's limit is 25MB
        if file_size_mb > 24:
            logger.info(f"Audio file is too large ({file_size_mb:.2f} MB), splitting into chunks")
            audio_chunks = self.split_audio_file(audio_file_path)
            
            # Transcribe each chunk and combine
            full_transcript = ""
            for i, chunk_path in enumerate(audio_chunks):
                logger.info(f"Transcribing chunk {i+1}/{len(audio_chunks)}")
                chunk_transcript = self._transcribe_single_file(chunk_path)
                full_transcript += chunk_transcript + " "
                
                # Clean up chunk file if it's not the original
                if chunk_path != audio_file_path:
                    try:
                        os.remove(chunk_path)
                    except Exception as e:
                        logger.warning(f"Error cleaning up chunk file: {str(e)}")
            
            return full_transcript.strip()
        else:
            # For smaller files, just transcribe directly
            return self._transcribe_single_file(audio_file_path)
    
    def _transcribe_single_file(self, audio_file_path: str) -> str:
        """
        Helper method to transcribe a single audio file with retries
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcription text
        """
        max_retries = 5
        retry_delay = 1  # Start with 1 second delay
        
        for attempt in range(max_retries):
            try:
                with open(audio_file_path, "rb") as audio_file:
                    # Call OpenAI API for transcription
                    client = openai.OpenAI()
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-transcribe",  # Using Whisper model for transcription
                        file=audio_file,
                        response_format="text"
                    )
                
                logger.info(f"Transcription complete for file: {os.path.basename(audio_file_path)}")
                return transcript
            
            except Exception as e:
                logger.error(f"Error transcribing audio (attempt {attempt+1}/{max_retries}): {str(e)}")
                
                # Check if we should retry
                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                    
                    # Need to reopen the file for the next attempt
                    if not os.path.exists(audio_file_path):
                        logger.error("Audio file no longer exists, cannot retry.")
                        raise RuntimeError("Audio file no longer exists, cannot retry transcription.")
                else:
                    # Max retries reached, give up
                    logger.error("Max retries reached for transcription.")
                    raise RuntimeError(f"Failed to transcribe audio after {max_retries} attempts: {str(e)}")
    
    def generate_notes_and_flashcards(self, transcript: str) -> Dict[str, Any]:
        """
        Generate formatted notes and flashcards from the transcript using GPT-4o
        
        Args:
            transcript: Transcription text
            
        Returns:
            Dictionary containing notes and flashcards
        """
        logger.info("Generating notes and flashcards")
        
        max_retries = 3
        retry_delay = 2  # Start with 2 second delay
        
        for attempt in range(max_retries):
            try:
                # Call GPT-4o to generate notes and flashcards
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert educator. Your task is to convert a lecture transcript into professionally formatted notes and flashcards."},
                        {"role": "user", "content": f"""Here is a transcript of a lecture or educational content:
                        
{transcript}

Please provide:
1. A structured set of notes summarizing key concepts
2. A set of flashcards with questions on the front and answers on the back

Format your response as a JSON with the following structure:
{{
  "notes": [
    {{
      "title": "Section title",
      "content": "Detailed notes for this section"
    }}
  ],
  "flashcards": [
    {{
      "question": "Question text",
      "answer": "Answer text"
    }}
  ]
}}"""}
                    ]
                )
                
                content = response.choices[0].message.content
                
                # Extract JSON from the response
                try:
                    # Try to parse the entire response as JSON
                    result = json.loads(content)
                except json.JSONDecodeError:
                    # If that fails, try to extract JSON from the text
                    import re
                    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group(1))
                    else:
                        # If no JSON pattern is found, try to extract it differently
                        json_match = re.search(r'\{[\s\S]*\}', content)
                        if json_match:
                            result = json.loads(json_match.group(0))
                        else:
                            raise ValueError("Could not extract JSON from the response")
                
                logger.info("Generated notes and flashcards successfully")
                return result
            
            except Exception as e:
                logger.error(f"Error generating notes and flashcards (attempt {attempt+1}/{max_retries}): {str(e)}")
                
                # Check if we should retry
                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                else:
                    # Max retries reached, give up
                    logger.error("Max retries reached for generating notes and flashcards.")
                    raise RuntimeError(f"Failed to generate notes and flashcards after {max_retries} attempts: {str(e)}")
    
    def generate_question_bank(self, transcript: str) -> List[Dict[str, Any]]:
        """
        Generate a question bank from the transcript using GPT-4o
        
        Args:
            transcript: Transcription text
            
        Returns:
            List of questions with options and answers
        """
        logger.info("Generating question bank")
        
        max_retries = 3
        retry_delay = 2  # Start with 2 second delay
        
        for attempt in range(max_retries):
            try:
                # Call GPT-4o to generate questions
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert educator designing assessment questions. Create diverse question types including multiple choice, true/false, and short answer questions."},
                        {"role": "user", "content": f"""Here is a transcript of educational content:
                        
{transcript}

Create a comprehensive question bank with various question types. For each question include:
1. The question text
2. Question type (multiple-choice, true/false, short-answer)
3. For multiple choice: provide 4 options (a,b,c,d)
4. The correct answer
5. A brief explanation of why the answer is correct

Format your response as a JSON array with the following structure:
[
  {{
    "question": "Question text",
    "type": "multiple-choice|true-false|short-answer",
    "options": ["option a", "option b", "option c", "option d"],  // Only for multiple-choice
    "correct_answer": "The correct answer",
    "explanation": "Explanation why this is the correct answer"
  }}
]"""}
                    ]
                )
                
                content = response.choices[0].message.content
                
                # Extract JSON from the response
                try:
                    # Try to parse the entire response as JSON
                    result = json.loads(content)
                except json.JSONDecodeError:
                    # If that fails, try to extract JSON from the text
                    import re
                    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group(1))
                    else:
                        # If no JSON pattern is found, try to extract it differently
                        json_match = re.search(r'\[[\s\S]*\]', content)
                        if json_match:
                            result = json.loads(json_match.group(0))
                        else:
                            raise ValueError("Could not extract JSON from the response")
                
                logger.info(f"Generated question bank with {len(result)} questions successfully")
                return result
            
            except Exception as e:
                logger.error(f"Error generating question bank (attempt {attempt+1}/{max_retries}): {str(e)}")
                
                # Check if we should retry
                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                else:
                    # Max retries reached, give up
                    logger.error("Max retries reached for generating question bank.")
                    raise RuntimeError(f"Failed to generate question bank after {max_retries} attempts: {str(e)}")
    
    def process_youtube_url(self, url: str) -> Dict[str, Any]:
        """
        Process a YouTube URL to generate transcript, notes, flashcards, and question bank
        
        Args:
            url: YouTube URL
            
        Returns:
            Dictionary containing transcript, notes, flashcards, and question bank
        """
        try:
            # Strip any playlist parameters from the URL
            clean_url = url.split("&list=")[0] if "&list=" in url else url
            
            # Download audio
            audio_path = self.download_audio(clean_url)
            
            # Transcribe audio
            transcript = self.transcribe_audio(audio_path)
            
            # Generate notes and flashcards
            result = self.generate_notes_and_flashcards(transcript)
            
            # Generate question bank
            questions = self.generate_question_bank(transcript)
            
            # Add transcript and questions to the result
            result["transcript"] = transcript
            result["questions"] = questions
            
            # Clean up the temporary audio file
            try:
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            except Exception as e:
                logger.warning(f"Error cleaning up temporary files: {str(e)}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error processing YouTube URL: {str(e)}")
            raise RuntimeError(f"Failed to process YouTube URL: {str(e)}")