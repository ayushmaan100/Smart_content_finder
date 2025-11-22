"""
AI service layer for generating summaries from raw text using OpenAI models.

Responsibilities:
- Load environment configuration (API key) via python-dotenv
- Provide a simple function `generate_summary(text)` that calls OpenAI's chat API

Notes:
- This module expects the environment variable `OPENAI_API_KEY` to be set.
- Model name can be adjusted as needed; it is currently set to "gpt-4o-mini".
- Upstream callers should handle exceptions from the OpenAI SDK (e.g., auth/network errors).
"""

# OpenAI Python SDK for making Chat Completions requests
import openai
# Standard library for reading environment variables
import os
# Load variables from a .env file into environment (supports local development)
from dotenv import load_dotenv
load_dotenv()

# Configure the OpenAI API key from environment. Ensure OPENAI_API_KEY is set.
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(text: str) -> str:
    """
    Generate a structured summary tailored for college students.

    Parameters
    ----------
    text : str
        The raw content to summarize (e.g., PDF text, YouTube transcript).

    Returns
    -------
    str
        A formatted summary produced by the OpenAI chat completion API.

    Notes
    -----
    - This function makes a synchronous API call. If used in an async context,
      consider offloading to a worker thread or using an async HTTP client.
    - Any exceptions from the OpenAI SDK will propagate to the caller.
    """

    prompt = f"""
    Summarize this educational content for a college student.

    Output format:
    - Section-wise summary
    - Key points
    - Definitions or formulas
    - Important takeaways

    Content:
    {text}
    """

    # Send the prompt as a single user message to the selected chat model.
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the assistant message content from the first choice and return it.
    return response["choices"][0]["message"]["content"]
