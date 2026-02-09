import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY", "")

client = genai.Client(api_key=api_key)

async def guess_object(description: str) -> str:
    if not description or len(description.strip()) < 3:
        return "Description too short."

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=f"Guess: '{description}'. Two words only, comma separated."
        )
        
        if response and response.text:
            return response.text.strip()
        return "AI could not provide a response."

    except Exception as e:
        print(f"Cost-Oriented AI Error: {e}")
        try:
            alt = client.models.generate_content(
                model="models/gemini-flash-lite-latest",
                contents=f"Guess: '{description}'. Two words."
            )
            return alt.text.strip()
        except:
            return "Guess could not be retrieved."