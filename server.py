import random
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from read_file import read_taboo_words
from ai_moderator import check_description
from ai_guesser import guess_object

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    taboo_dict = read_taboo_words()
except (FileNotFoundError, ValueError) as e:
    print(f"FATAL: {e}")
    exit()


class GetWordRequest(BaseModel):
    used_words: List[str]

class DescriptionCheckRequest(BaseModel):
    target_word: str
    description: str

class GuessRequest(BaseModel):
    description: str

@app.get("/")
async def read_root():
    return {"message": "Taboo AI Backend is running!"}

@app.post("/api/get-word")
async def get_word(request: GetWordRequest):
    all_words = list(taboo_dict.keys())
    available_words = [word for word in all_words if word not in request.used_words]

    if not available_words:
        return {"error": "All words have been used!"}

    target_word = random.choice(available_words)
    return {"word": target_word, "taboo": taboo_dict[target_word]}

@app.post("/api/check-description")
async def check_desc_endpoint(request: DescriptionCheckRequest):
    result_json_str = check_description(taboo_dict, request.target_word, request.description)
    return json.loads(result_json_str)

@app.post("/api/guess-word")
async def guess_word_endpoint(request: GuessRequest):
    try:
        guess = await guess_object(request.description)
        return {"guess": guess}
    except Exception as e:
        print(f"Error in guess_word_endpoint: {e}")
        raise HTTPException(status_code=503, detail="AI service is currently unavailable.")