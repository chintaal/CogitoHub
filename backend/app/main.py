from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v1 import coachpilot, coursito

app = FastAPI(
    title="Cogito API",
    description="AI Coaching API that leverages book knowledge",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(coachpilot.router, prefix="/api/v1")
app.include_router(coursito.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint to verify the API is running."""
    return {
        "name": "Cogito API",
        "description": "AI Coaching platform powered by book knowledge",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
