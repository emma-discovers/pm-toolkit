"""
Quiz Generator using Google Gemini API (Free Tier)
==================================================

A simple script that generates quiz questions from a given topic or text
using Google's free Gemini API.

Setup:
    1. Get a free API key at https://aistudio.google.com/apikey (no credit card needed).
    2. Install the SDK: pip install google-genai
    3. Run: python quiz-generator.py --topic "Python loops" --num 3

"""

import argparse
import os
from google import genai


def generate_quiz(topic: str, num_questions: int = 3) -> str:
    """Generate quiz questions using Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY environment variable.")

    client = genai.Client(api_key=api_key)

    prompt = f"""Generate {num_questions} multiple-choice quiz questions about: {topic}.

For each question, provide:
- The question text
- 4 answer options (A, B, C, D)
- The correct answer
- A brief explanation

Format as clean Markdown."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


def main():
    parser = argparse.ArgumentParser(description="Generate quiz questions with Gemini.")
    parser.add_argument("--topic", required=True, help="Topic for the quiz")
    parser.add_argument("--num", type=int, default=3, help="Number of questions")
    args = parser.parse_args()

    result = generate_quiz(args.topic, args.num)
    print(result)


if __name__ == "__main__":
    main()
