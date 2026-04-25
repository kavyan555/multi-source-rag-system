import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

def ask_llm(context, query):
    prompt = f"""
    Answer ONLY from the given context.

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)
    return response.text