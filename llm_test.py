import os
import time

from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()


def test_gemini(transcript: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=transcript,
    )

    print(response.text)


def test_openai(transcript: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": transcript},
        ],
        stream=True,
    )

    # Process the streaming response
    collected_content = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content_chunk = chunk.choices[0].delta.content
            collected_content += content_chunk
            print(content_chunk, end="", flush=True)  # Print each chunk as it arrives

    print()  # Add a newline at the end
    return collected_content


def main():
    start = time.time()
    response = test_openai("Why is the sky blue?")
    print("\nFull response collected:")
    print(response)
    print(f"Time taken: {time.time() - start}")


if __name__ == "__main__":
    main()
