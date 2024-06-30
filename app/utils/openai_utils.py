# type: ignore
from app.settings import settings
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from openai import OpenAI

client = OpenAI(
    api_key=settings.openai_api_key,
)

env = Environment(loader=FileSystemLoader("./app/prompts"), autoescape=select_autoescape(["jinja"]))


def getResponseFromOpenai(message: str) -> str:
    template = env.get_template("openai_prompt.jinja")
    prompt = template.render()

    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content.strip()
