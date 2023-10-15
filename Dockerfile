FROM python:3.11

ENV CONF_HOST 0.0.0.0
ENV CONF_PORT 8000

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# FastAPI 앱 실행 명령어
CMD ["uvicorn", "main:app", "--host", "{CONF_HOST}", "--port", "${CONF_PORT}"]

