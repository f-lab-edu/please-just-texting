import os

import openai
from dotenv import load_dotenv

# load .env file
load_dotenv()

conversation = os.getenv("CONVERSATION")

# API key setting
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "이 문장에서 약속 날짜를 년-월-일 형식으로 추출해줘."},
    {"role": "user", "content": conversation},
    {
        "role": "system",
        "content": "생각: 대화내역을 통해 참여자들이 만나려고 하는 일정을 파악하려한다. 행동: 일정과 관련되어 보이는 키워드와 문맥을 파악한다. 관찰: 참여자들 중 대다수가 참여의사를 밝히는 날짜를 파악한다.",
    },
]

response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

print(response.choices[0].message["content"].strip())
