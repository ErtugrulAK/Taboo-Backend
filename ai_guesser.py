import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def guess_object(description: str) -> str:
    chat = model.start_chat()
    response = chat.send_message(
        f"Guess two possible objects that might be described in this sentence: '{description}'. "
        "Only respond with two guesses, separated by a comma. Do not explain anything."
    )
    return response.text.strip()

