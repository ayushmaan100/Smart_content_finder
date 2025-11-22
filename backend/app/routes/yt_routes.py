"""YouTube-related API routes.

This module exposes an endpoint that accepts a YouTube video URL, fetches its
transcript or content via the service layer, and returns an AI-generated summary.
"""

# APIRouter groups related endpoints that are later mounted in the main app under a prefix.
from fastapi import APIRouter
# BaseModel helps validate and parse incoming JSON payloads with a defined schema.
from pydantic import BaseModel
# Business logic for processing a YouTube URL and generating a summary.
from app.services.yt_service import process_youtube_link

# Create a router instance dedicated to YouTube endpoints.
router = APIRouter()

class VideoLink(BaseModel):
    """
    Input schema for the summarize endpoint.

    Attributes
    ----------
    url : str
        The full YouTube video URL to summarize.
    """
    url: str

@router.post("/summarize")
async def summarize_youtube(data: VideoLink):
    """
    Summarize the content of a YouTube video.

    Request body (application/json):
    {
      "url": "https://www.youtube.com/watch?v=..."
    }

    Returns:
    - JSON object with a single key "summary" containing the generated summary text.
    """
    # Delegate to the service layer to retrieve transcript/content and summarize it.
    summary = await process_youtube_link(data.url)
    # Wrap the result in a simple JSON payload.
    return {"summary": summary}
