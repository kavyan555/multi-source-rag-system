import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key missing in .env")

genai.configure(api_key=api_key)

# stable working model 
model = genai.GenerativeModel("gemini-flash-latest")


def ask_llm(context, query):
    prompt = f"""
Answer ONLY from the given context.
If answer is not present, say "Not found in provided documents".
Be concise and clear.

Context:
{context}

Question:
{query}
"""

    response = model.generate_content(prompt)

    return response.text if response.text else "No response generated"