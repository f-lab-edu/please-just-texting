FROM python:3.11

ENV CONF_HOST 0.0.0.0
ENV CONF_PORT 8000

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# A command for running FastAPI app.
CMD ["python3", "app/main.py"]

