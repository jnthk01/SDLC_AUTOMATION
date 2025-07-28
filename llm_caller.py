import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_flash1_5(query):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Explain how AI works in a few words"
    )
    return response.text

def gemini_1_5_pro(query):
    response = client.models.generate_content(
        model="gemini-1.5-pro", contents="Explain how AI works in a few words"
    )
    return response.text