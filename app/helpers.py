import json
import os 
import logging
from pprint import pprint

from openai import OpenAI
from dotenv import load_dotenv
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
)

from strings import *
from google import genai

load_dotenv()
client = OpenAI()


def test_gemini(transcript: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = grammar_word_prompt.replace("{transcript}", json.dumps(transcript, ensure_ascii=False, indent=2)).replace("{proficiency_level}", "advanced")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        
        if not response:
            print("No response from Gemini")
            return {"error": "No response from Gemini API"}
        
        print("Raw API response:", response.text)
        
        # Check if the response text is empty
        if not response.text:
            return {"error": "Empty response text from Gemini API"}
        
        # Extract JSON from markdown code blocks if present
        response_text = response.text
        if response_text.strip().startswith("```json") and response_text.strip().endswith("```"):
            # Extract the JSON part between the markdown code block markers
            json_text = response_text.strip()[7:-3].strip()  # Remove ```json at start and ``` at end
            print("Extracted JSON text:", json_text[:100] + "..." if len(json_text) > 100 else json_text)
        else:
            json_text = response_text
        
        # Try to parse response as JSON
        try:
            result = json.loads(json_text)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            # Return the raw text response if it's not JSON
            return {"raw_response": response_text, "error": "Failed to parse as JSON"}
            
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return {"error": f"API error: {str(e)}"}


async def analyze_transcript_openai(transcript: str) -> dict:
    prompt = grammar_word_prompt.replace("{transcript}", json.dumps(transcript, ensure_ascii=False, indent=2)).replace("{proficiency_level}", "advanced")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
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
        # Create API instance as per documentation
        ytt_api = YouTubeTranscriptApi()
        
        try:
            # First try to get Korean transcript
            print(f"Attempting to fetch Korean transcript for video {video_id}")
            fetched_transcript = ytt_api.fetch(video_id)
            print(f"Found Korean transcript for video {video_id}")
            # Convert to raw data format (list of dictionaries) for compatibility
            return fetched_transcript.to_raw_data()
        except NoTranscriptFound:
            logging.info(f"No Korean subtitles found for video: {video_id}. Trying any available language.")
            print(f"No Korean subtitles found. Trying any available language.")
            # If Korean not available, try any language
            fetched_transcript = ytt_api.fetch(video_id)
            print(f"Found transcript in another language for video {video_id}")
            return fetched_transcript.to_raw_data()

    except NoTranscriptFound:
        logging.info(f"No subtitles found in any language for video: {video_id}")
        print(f"No subtitles found in any language for video: {video_id}")
        return None
    except TranscriptsDisabled:
        logging.info(f"Transcripts are disabled for video: {video_id}")
        print(f"Transcripts are disabled for video: {video_id}")
        return None
    except Exception as e:
        logging.error(f"Error fetching transcript for video {video_id}: {str(e)}")
        print(f"Error fetching transcript: {str(e)}")
        return None


async def main():
    transcript = await get_transcript("3YBYF7JRI1Y")
    if transcript:
        grammar_and_vocab = await analyze_transcript_openai(json.dumps(transcript))
        pprint(grammar_and_vocab)
    else:
        logging.info("No transcript found for the given video ID.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
