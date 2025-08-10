import json
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers import *

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /api/grammar-and-vocabulary/3HFuXBBVP24


@app.get("/api/grammar-and-vocabulary/{id}")
async def read_root(id: str):
    transcript = await get_transcript(id)
    if transcript:
        # Call the test_gemini function with proper error handling
        result = test_gemini(transcript)
        return result
    else:
        return {"error": "No transcript found for this video ID"}


@app.post("/api/grammar-and-vocabulary/questions")
async def read_root(data: str):
    if data:
        questions = await get_questions(data)
    return questions


@app.post("/api/grammar-and-vocabulary/summary")
async def read_root(data: str):
    if data:
        summary = await get_summary(data)
    return summary


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
