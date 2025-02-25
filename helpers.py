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

from prompt import *


load_dotenv()
client = OpenAI()


async def analyze_transcript_openai(transcript: str) -> dict:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": grammar_word_prompt},
            {"role": "user", "content": transcript},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)

async def get_summary(data: str) -> dict:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": summary_prompt},
            {"role": "user", "content": data},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)

async def get_questions(data: str) -> dict:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": question_prompt},
            {"role": "user", "content": data},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(completion.choices[0].message.content)




async def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"])
        return transcript

    except NoTranscriptFound:
        logging.info(f"No Korean subtitles found for video: {video_id}")
        return None
    except TranscriptsDisabled:
        logging.info(f"Transcripts are disabled for video: {video_id}")
        return None




async def main():
    transcript = await get_transcript("3HFuXBBVP24")
    if transcript:
        grammar_and_vocab = await analyze_transcript_openai(json.dumps(transcript))
        pprint(grammar_and_vocab)
    else:
        logging.info("No transcript found for the given video ID.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
