import os
import google.generativeai as genai
from dotenv import load_dotenv

# Project root path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(prompt):
    """
    Sends prompt to Gemini and returns response text.
    """

    response = model.generate_content(prompt)

    return response.text

if __name__ == "__main__":

    prompt = """
    Say Hello in one sentence.
    """

    print(generate_response(prompt))