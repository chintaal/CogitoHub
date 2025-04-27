from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import json
import sys
import time
from enum import Enum

# Add KnowledgeBaseParsing directory to path for importing modules
KBP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "KnowledgeBaseParsing")
sys.path.append(KBP_DIR)

# Import RAG utilities
from query_chunked import get_embedding, rag_query

# Import OpenAI
import openai
from dotenv import load_dotenv
import hashlib
from functools import lru_cache

# Load environment variables
load_dotenv()

# Set your API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Simple cache for query results
query_cache = {}

# Set the correct path to the database - use the one in KnowledgeBaseParsing directory
DEFAULT_DB_PATH = os.path.join(KBP_DIR, "fast_embed_db")

router = APIRouter(prefix="/coachpilot", tags=["coachpilot"])

class ContentFormat(str, Enum):
    CHECKLIST = "checklist"
    KANBAN = "kanban"
    TIMELINE = "timeline"
    MINDMAP = "mindmap"
    ACTION_PLAN = "action_plan"
    DAILY_ROUTINE = "daily_routine"
    COMPARISON_TABLE = "comparison_table"
    SMART_GOALS = "smart_goals"

class CoachRequest(BaseModel):
    query: str = Field(..., description="The coaching query or topic to address")
    formats: List[ContentFormat] = Field(
        default=[ContentFormat.ACTION_PLAN], 
        description="The desired content formats to generate"
    )
    top_k: int = Field(default=5, description="Number of book chunks to retrieve")
    max_tokens: int = Field(default=2000, description="Maximum tokens in the response")
    include_sources: bool = Field(default=True, description="Whether to include book sources in the response")
    db_path: str = Field(default=DEFAULT_DB_PATH, description="Path to vector database")
    detailed_response: bool = Field(default=False, description="Whether to include detailed explanations in the response")

class BookSource(BaseModel):
    title: str
    relevance: float
    chunks_used: int
    key_insights: List[str]

class ContentSection(BaseModel):
    format: ContentFormat
    title: str
    content: Dict[str, Any]
    description: Optional[str] = None

class CoachResponse(BaseModel):
    query: str
    summary: str
    sections: List[ContentSection]
    sources: Optional[List[BookSource]] = None
    execution_time: float

@router.post("/generate", response_model=CoachResponse)
async def generate_coach_content(request: CoachRequest = Body(...)):
    """
    Generate structured coaching content based on a query using the book knowledge base.
    """
    start_time = time.time()
    
    try:
        # Create a cache key based on the request parameters
        cache_key = f"{request.query}_{','.join(sorted([f.value for f in request.formats]))}"
        cache_key += f"_{request.top_k}_{request.include_sources}_{request.detailed_response}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # Check if we have a cached response
        if cache_key in query_cache:
            print("Using cached response")
            cached_response = query_cache[cache_key]
            # Update execution time for the cached response
            cached_response.execution_time = time.time() - start_time
            return cached_response
        
        # Print the database path for debugging
        print(f"Using database path: {request.db_path}")
        
        # Check if the database exists
        if not os.path.exists(request.db_path):
            # If not, try to use the default path
            if request.db_path != DEFAULT_DB_PATH and os.path.exists(DEFAULT_DB_PATH):
                print(f"Specified database path {request.db_path} not found, using default path instead: {DEFAULT_DB_PATH}")
                request.db_path = DEFAULT_DB_PATH
            else:
                available_paths = []
                # Check if the database exists in KnowledgeBaseParsing directory
                kbp_path = os.path.join(KBP_DIR, "fast_embed_db")
                if os.path.exists(kbp_path):
                    available_paths.append(kbp_path)
                
                # Check if there's a database in the chunked_vector_db path
                chunked_path = os.path.join(KBP_DIR, "chunked_vector_db")
                if os.path.exists(chunked_path):
                    available_paths.append(chunked_path)
                
                if available_paths:
                    request.db_path = available_paths[0]
                    print(f"Using alternative database path: {request.db_path}")
                else:
                    raise ValueError(f"No vector database found at {request.db_path} or any alternative locations")
        
        # 1. Retrieve relevant book chunks using RAG
        rag_results = rag_query(
            query=request.query,
            top_k=request.top_k,
            model="gpt-4o",
            db_path=request.db_path,
            embedding_model="text-embedding-3-small",
            return_raw_results=True  # Get raw results instead of formatted output
        )
        
        # 2. Extract book sources and content
        book_sources = []
        context_text = ""
        
        for book_title, chunks in rag_results["sources"].items():
            # Only use the most relevant content from each book to reduce token usage
            # Sort chunks by relevance and limit to most relevant ones
            sorted_chunks = sorted(chunks, key=lambda x: x["relevance"], reverse=True)
            # Use at most 3 chunks per book to limit token usage
            limited_chunks = sorted_chunks[:3]
            
            source = {
                "title": book_title,
                "relevance": max(chunk["relevance"] for chunk in chunks),
                "chunks_used": len(limited_chunks),
                "content": "\n".join([chunk["content"] for chunk in limited_chunks])
            }
            
            context_text += f"Book: {book_title}\n{source['content']}\n\n"
            
            # Add to book sources if requested
            if request.include_sources:
                book_sources.append({
                    "title": book_title,
                    "relevance": source["relevance"],
                    "chunks_used": source["chunks_used"],
                    "key_insights": []  # Will be populated later
                })
        
        # 3. Generate structured content using GPT-4o
        sections = []
        system_prompt = create_system_prompt(request.formats, request.detailed_response, request.include_sources)
        
        # 4. Make a single API call for both content and insights
        combined_prompt = f"Context from books:\n{context_text}\n\n"
        combined_prompt += f"User query: {request.query}\n\n"
        combined_prompt += f"Generate structured content in JSON format for the formats: {', '.join([f.value for f in request.formats])}.\n\n"
        
        if request.include_sources:
            combined_prompt += f"Additionally, for each book source, extract 3-5 key insights that are most relevant to the query.\n"
            combined_prompt += f"Include these insights in a 'book_insights' object where each key is the book title and the value is an array of insight strings.\n\n"
        
        combined_prompt += "Your response must be valid JSON."
        
        # Single API call
        main_response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": combined_prompt}
            ],
            max_tokens=request.max_tokens,
            response_format={"type": "json_object"}
        )
        
        # 5. Parse the response
        structured_content = json.loads(main_response.choices[0].message.content)
        
        # Create summary
        summary = structured_content.get("summary", "No summary generated.")
        
        # Process each section
        for format_type in request.formats:
            format_key = format_type.value
            if format_key in structured_content:
                sections.append(
                    ContentSection(
                        format=format_type,
                        title=structured_content[format_key].get("title", f"{format_key.title()} Plan"),
                        content=structured_content[format_key].get("content", {}),
                        description=structured_content[format_key].get("description", None)
                    )
                )
        
        # Process book insights if included
        if request.include_sources and book_sources and "book_insights" in structured_content:
            insights = structured_content["book_insights"]
            
            # Match insights to book sources
            for book_source in book_sources:
                book_title = book_source["title"]
                if book_title in insights:
                    book_source["key_insights"] = insights[book_title]
                else:
                    # Try to find a close match
                    for insight_key in insights:
                        if book_title.lower() in insight_key.lower() or insight_key.lower() in book_title.lower():
                            book_source["key_insights"] = insights[insight_key]
                            break
        
        execution_time = time.time() - start_time
        
        # 7. Construct and return the response
        response = CoachResponse(
            query=request.query,
            summary=summary,
            sections=sections,
            sources=book_sources if request.include_sources else None,
            execution_time=execution_time
        )
        
        # Cache the response
        query_cache[cache_key] = response
        
        # Limit cache size to prevent memory issues
        if len(query_cache) > 100:  # Limit cache to 100 entries
            # Remove the oldest entry
            oldest_key = next(iter(query_cache))
            del query_cache[oldest_key]
            
        return response
    
    except Exception as e:
        print(f"Error in generate_coach_content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating coach content: {str(e)}")

def create_system_prompt(formats, detailed_response, include_sources):
    """Create a system prompt based on requested formats"""
    base_prompt = """You are CoachPilot, an advanced AI coaching assistant with deep knowledge from books on personal development, psychology, business, and more.
    
Your task is to generate highly structured, actionable content based on the knowledge in the provided book excerpts.
The content should be directly usable for frontend visualizations like checklists, kanban boards, timelines, etc.

Your response MUST be a valid JSON object with the following structure:
{
  "summary": "A brief summary of your advice and approach",
}

For each requested format, include a section with that format name, containing:
- "title": A concise, engaging title for this section
- "description": A brief explanation of this content (if applicable)
- "content": The structured content in a format suitable for the requested visualization

"""

    # Add specific instructions for each format
    format_instructions = {
        ContentFormat.CHECKLIST: """For CHECKLIST format, use:
"content": {
  "items": [
    {"id": "1", "text": "Item description", "details": "Additional details", "priority": "high/medium/low"},
    ...
  ]
}""",
        
        ContentFormat.KANBAN: """For KANBAN format, use:
"content": {
  "columns": [
    {
      "id": "todo", 
      "title": "To Do", 
      "items": [
        {"id": "1", "text": "Task description", "details": "Additional details"},
        ...
      ]
    },
    {
      "id": "doing", 
      "title": "In Progress", 
      "items": [...]
    },
    {
      "id": "done", 
      "title": "Done", 
      "items": [...]
    }
  ]
}""",
        
        ContentFormat.TIMELINE: """For TIMELINE format, use:
"content": {
  "timeUnits": "days/weeks/months",
  "events": [
    {"id": "1", "title": "Event title", "description": "Event description", "time": "Time marker", "duration": "Duration if applicable"},
    ...
  ]
}""",
        
        ContentFormat.MINDMAP: """For MINDMAP format, use:
"content": {
  "central": "Main concept",
  "branches": [
    {
      "id": "1",
      "text": "Branch concept",
      "children": [
        {"id": "1-1", "text": "Sub-concept"},
        {"id": "1-2", "text": "Sub-concept", "children": [...]}
      ]
    },
    ...
  ]
}""",
        
        ContentFormat.ACTION_PLAN: """For ACTION_PLAN format, use:
"content": {
  "goal": "Main goal",
  "steps": [
    {"id": "1", "action": "Step description", "timeframe": "Expected timeframe", "resources": ["Resource 1", "Resource 2"], "metrics": ["How to measure success"]},
    ...
  ]
}""",
        
        ContentFormat.DAILY_ROUTINE: """For DAILY_ROUTINE format, use:
"content": {
  "timeBlocks": [
    {"id": "1", "timeRange": "6:00-7:00 AM", "activity": "Activity description", "purpose": "Why this matters", "priority": 1-5},
    ...
  ]
}""",
        
        ContentFormat.COMPARISON_TABLE: """For COMPARISON_TABLE format, use:
"content": {
  "headers": ["Aspect", "Option 1", "Option 2", ...],
  "rows": [
    {"id": "1", "cells": ["Feature 1", "Value 1A", "Value 1B", ...]},
    ...
  ]
}""",
        
        ContentFormat.SMART_GOALS: """For SMART_GOALS format, use:
"content": {
  "goals": [
    {
      "id": "1",
      "goal": "Goal statement",
      "specific": "What exactly will be accomplished",
      "measurable": "How progress will be measured",
      "achievable": "Why this is attainable",
      "relevant": "Why this matters",
      "timeBound": "Deadline or timeframe"
    },
    ...
  ]
}"""
    }
    
    # Add instructions for requested formats
    for format_type in formats:
        if format_type in format_instructions:
            base_prompt += "\n\n" + format_instructions[format_type]
    
    # Add more detail for comprehensive responses
    if detailed_response:
        base_prompt += """

For each component, include detailed explanations and rationale based on the books.
Make your response comprehensive, well-structured, and directly actionable.
Include practical examples and specific techniques mentioned in the source materials.
"""
    else:
        base_prompt += """

Be concise and focused. Prioritize actionable content over lengthy explanations.
Ensure all response elements are structured for easy rendering in a frontend application.
"""
    
    if include_sources:
        base_prompt += """

Additionally, for each book source, extract 3-5 key insights that are most relevant to the query.
Include these insights in a 'book_insights' object where each key is the book title and the value is an array of insight strings.
"""
    
    base_prompt += """

Important: Ensure your entire response is a valid JSON object. Do not include any text outside the JSON structure.
Base all your recommendations directly on the book knowledge provided, citing specific books where relevant.
"""
    
    return base_prompt

# Add a simple GET endpoint for testing
@router.get("/test")
async def test_coachpilot():
    """Test endpoint to verify the CoachPilot API is running"""
    return {"status": "ok", "message": "CoachPilot API is running"}

# Add a simple POST endpoint for Postman testing
@router.post("/test-generate")
async def test_generate(request: dict = Body(...)):
    """
    Simple endpoint for testing CoachPilot with Postman
    Example request body:
    {
        "query": "How can I improve my time management?",
        "format": "action_plan"  # optional
    }
    """
    start_time = time.time()
    
    try:
        # Extract query from request
        query = request.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required")
        
        # Set default format if not provided
        format_str = request.get("format", "action_plan")
        try:
            format_enum = ContentFormat(format_str)
        except ValueError:
            # Default to action plan if invalid format
            format_enum = ContentFormat.ACTION_PLAN
        
        # Create a simplified coach request
        coach_request = CoachRequest(
            query=query,
            formats=[format_enum],
            top_k=3,  # Reduced for faster response
            max_tokens=1500,  # Reduced for faster response
            include_sources=True,
            db_path=DEFAULT_DB_PATH,
            detailed_response=False
        )
        
        # Use the existing generate_coach_content logic
        result = await generate_coach_content(coach_request)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Return a simplified response for easier testing
        return {
            "query": query,
            "format": format_str,
            "summary": result.summary,
            "processing_time_seconds": processing_time,
            "sources_count": len(result.sources) if result.sources else 0,
            "content": result.sections[0].content if result.sections else {}
        }
    
    except Exception as e:
        print(f"Error in test_generate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating test content: {str(e)}")