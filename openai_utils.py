import os

import openai

# API key setting
openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.Completion.create(
    model="gpt-3.5-turbo", prompt="message", max_tokens=150
)

print(response.choices[0].text.strip())
