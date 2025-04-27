from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any, Optional
from app.core.coursitoagent import CoursitoAgent

router = APIRouter(
    prefix="/coursito",
    tags=["Coursito"]
)

class YoutubeUrlRequest(BaseModel):
    url: HttpUrl
    
class ProcessResponse(BaseModel):
    transcript: str
    notes: list
    flashcards: list

@router.options("/process-youtube")
async def options_process_youtube():
    """
    Handle OPTIONS requests for CORS preflight checks.
    """
    return Response(status_code=200)

@router.post("/process-youtube", response_model=Dict[str, Any])
async def process_youtube_video(request: YoutubeUrlRequest):
    """
    Process a YouTube video URL to generate transcript, notes, and flashcards.
    """
    try:
        agent = CoursitoAgent()
        result = agent.process_youtube_url(str(request.url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))