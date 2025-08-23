import random
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from read_file import read_taboo_words
from ai_moderator import check_description
from ai_guesser import guess_object

app = FastAPI()

taboo_dict = read_taboo_words()

class GetWordRequest(BaseModel):
    used_words: List[str]

class DescriptionCheckRequest(BaseModel):
    target_word: str
    description: str

class GuessRequest(BaseModel):
    description: str

@app.get("/")
def read_root():
    return {"message": "Taboo AI Backend is running!"}

@app.post("/api/get-word")
def get_word(request: GetWordRequest):
    all_words = list(taboo_dict.keys())
    available_words = [word for word in all_words if word not in request.used_words]

    if not available_words:
        return {"error": "All words have been used!"}

    target_word = random.choice(available_words)
    return {"word": target_word, "taboo": taboo_dict[target_word]}

@app.post("/api/check-description")
def check_desc_endpoint(request: DescriptionCheckRequest):
    result_json_str = check_description(taboo_dict, request.target_word, request.description)
    return json.loads(result_json_str)

@app.post("/api/guess-word")
def guess_word_endpoint(request: GuessRequest):
    guess = guess_object(request.description)
    return {"guess": guess}