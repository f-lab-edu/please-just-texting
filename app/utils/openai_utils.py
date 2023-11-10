from openai import OpenAI
from settings import settings

client = OpenAI(
    api_key=settings.openai_api_key,
)

# temporary conversation
conversation = settings.conversation

messages = [
    {
        "role": "system",
        "content": "너는 회의 발화 내용을 읽고 일정을 잡아주는 비서 시스템이야.\
       앞으로 문장이 주어질 텐데, 그 문장에서 일정으로 추가해야하는 유저의 특정 일자 제목과 예상되는 일자의 아젠다 그리고 마지막으로 일자(YYYY-MM-DD) 형식으로 추출해야 해야해.\
       상대적 일자 (내일, 다음주, 어제, 그저께 등은 오늘 일자 '2023-11-01' 기준으로 계산해줘.)",
    },
    {"role": "user", "content": conversation},
]

response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

print(response.choices[0].message.content.strip())
