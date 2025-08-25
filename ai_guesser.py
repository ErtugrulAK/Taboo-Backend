import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name=model_name)

async def guess_object(description: str) -> str:
    try:
        chat = model.start_chat()
        response = await chat.send_message_async(
            f"Guess two possible objects that might be described in this sentence: '{description}'. "
            "Only respond with two guesses, separated by a comma. Do not explain anything."
        )
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred with the AI Guesser: {e}")
        return "Error: Could not get a guess from the AI."