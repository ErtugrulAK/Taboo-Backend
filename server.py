import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from read_file import read_taboo_words

app = FastAPI()

taboo_dict = read_taboo_words()

class GetWordRequest(BaseModel):
    used_words: List[str]

@app.get("/")
def read_root():
    return {"message": "The code runs successfully"}

@app.post("/api/get-word")
def get_word(request: GetWordRequest):
    all_words = list(taboo_dict.keys())
    available_words = [word for word in all_words if word not in request.used_words]

    if not available_words:
        return {"error": "All words have been used!"}

    target_word = random.choice(available_words)
    return {"word": target_word, "taboo": taboo_dict[target_word]}