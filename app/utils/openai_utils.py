from openai import OpenAI
from settings import settings

client = OpenAI(
    api_key=settings.openai_api_key,
)


def getResponseFromOpenai(message):
    messages = [
        {
            "role": "system",
            "content": "asistant는 회의 발화 내용을 읽고 일정을 잡아주는 비서 시스템이야.\
       앞으로 문장이 주어질 텐데, 그 문장에서 일정으로 추가해야하는 유저의 특정 일자 제목과 예상되는 일자의 아젠다 그리고 마지막으로 일자(YYYY-MM-DD) 형식으로 추출해야 해야해.\
       상대적 일자 (내일, 다음주, 어제, 그저께 등은 오늘 일자 '2023-11-12' 기준으로 계산해줘.)",
        },
        {"role": "user", "content": message},
        {
            "role": "assistant",
            "content": "user가 제시한 대화내역에서 일정과 관련된 내용을 'YYYY-MM-DD' 그리고 일자 제목, 마지막으로 일자 아젠다를 각각 뽑는다.\
    정보를 추출했으면 date: {일정날짜 / STRING}, title: {일정 제목 / STRING}, description: {일정 아젠다 / STRING} 형태로 키를 잡아서 제공해줘.\
    키는 반드시 소문자 알파벳이야. 일정 아젠다는 20자를 넘어가면 안돼",
        },
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content.strip()
