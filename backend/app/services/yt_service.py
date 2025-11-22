"""
Service functions for handling YouTube video processing and summarization.

Flow:
1) Parse a YouTube URL to extract a video ID (basic approach based on "v=")
2) Fetch the video's transcript using youtube-transcript-api
3) Concatenate all transcript text
4) Send the text to the AI layer to produce a summary

Notes/limitations (not handled here):
- This simplistic video ID parsing works for URLs containing "?v=..." but not all
    variants (e.g., youtu.be/<id>, embed URLs, shorts). Consider a more robust parser
    if you need full coverage.
- Some videos may not have transcripts (disabled by uploader, live streams, etc.) or
    may require language selection/fallbacks.
- youtube-transcript-api may raise exceptions (e.g., when transcripts are unavailable).
    Upstream callers should handle and map them to user-friendly API responses.
"""

# Library used to fetch video transcripts without the YouTube Data API.
from youtube_transcript_api import YouTubeTranscriptApi
# App's AI service responsible for turning raw text into a concise summary
from app.services.ai_service import generate_summary

async def process_youtube_link(url: str) -> str:
    """
    Generate a summary for a YouTube video given its URL.

    Parameters
    ----------
    url : str
        The YouTube video URL. Expected to contain a "v=" query parameter.

    Returns
    -------
    str
        The generated summary of the video's transcript.

    Implementation details
    ----------------------
    - Extracts the video ID by splitting on "v=" and taking the last segment.
      This is intentionally simple; more robust parsing may be required for
      short links or other URL formats.
    - Fetches the transcript as a list of items with "text" fields.
    - Joins all transcript text into a single string for summarization.
    """

    # Extract a video ID in a minimal way for standard watch URLs.
    video_id = url.split("v=")[-1]
    # Retrieve transcript segments (each item typically contains 'text', 'start', 'duration').
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

    # Combine all transcript pieces into one block of text for the AI summarizer.
    text = " ".join([item["text"] for item in transcript_data])
    # Call the AI service to produce a concise summary of the transcript.
    summary = generate_summary(text)

    return summary
