import os

import openai
from dotenv import load_dotenv

# load .env file
load_dotenv()

# API key setting
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="gpt-3.5-turbo", prompt="message", max_tokens=150
)

print(response.choices[0].text.strip())
