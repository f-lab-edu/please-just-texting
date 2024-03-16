# type: ignore
from openai import OpenAI
from settings import settings

client = OpenAI(
    api_key=settings.openai_api_key,
)


def getResponseFromOpenai(message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": '너는 user가 제시한 message에서 전체 대화 내역을 파악하여 일정 정보를 한개를 제공해야해. \
                        최종 만남 일정을 "YYYY-MM-DD" 그리고 일정 제목, 마지막으로 일자 내용로 추출해야돼.\
                        일정 내용에는 만남 장소, 만남 일정, 참여 인원에 대해서 요약해줘.\
                        정보를 추출했으면 {"date": "{최종 만남 일정 / STRING}", "title": "{일정 제목 / STRING}", "description": "{일정 내용 / STRING}"} 형태로 키를 잡아서 제공해줘.\
                        키는 반드시 소문자 알파벳이야. 일정 내용는 60자를 넘어가면 안돼',
        },
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content.strip()
