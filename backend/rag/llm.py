import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def model(prompt):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file.")

    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    
    return response_text