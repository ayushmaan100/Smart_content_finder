import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_flashcards(text: str):
    prompt = f"""
    Create exactly **10 study flashcards** from the content below.
    Format strictly:
    Q: <question>
    A: <answer>

    Content:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]


def generate_mcqs(text: str):
    prompt = f"""
    Generate **10 multiple choice questions** from the following content.
    
    For each question include:
    - 4 options (A–D)
    - Correct answer at the end.

    Format strictly:
    Q1. <question>
    A. <option>
    B. <option>
    C. <option>
    D. <option>
    Answer: <A/B/C/D>

    Content:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]
