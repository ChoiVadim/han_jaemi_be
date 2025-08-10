from dotenv import load_dotenv
import os
import time
import sys
from pprint import pprint
import json
import logging
from pprint import pprint

from openai import OpenAI
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
)


from google import genai
from openai import OpenAI

from strings import *

load_dotenv()


def test_gemini(prompt: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return json.loads(response.text)


def test_openai(prompt: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"])
        return transcript

    except NoTranscriptFound:
        logging.info(f"No Korean subtitles found for video: {video_id}")
        return None
    except TranscriptsDisabled:
        logging.info(f"Transcripts are disabled for video: {video_id}")
        return None

def main():
    start = time.time()
    transcript = get_transcript("3HFuXBBVP24")
    print(transcript)
    if transcript:
        prompt = grammar_word_prompt.replace("{transcript}", json.dumps(transcript, ensure_ascii=False, indent=2)).replace("{proficiency_level}", "advanced")
        pprint(prompt)

        response = test_gemini(prompt)
        pprint(response)

        print(f"Time taken: {time.time() - start}")


if __name__ == "__main__":
    main()
