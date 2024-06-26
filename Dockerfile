FROM python:3.11

ENV CONF_HOST 0.0.0.0
ENV CONF_PORT 8000
ENV PYTHONPATH /src

WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt

CMD ["python3", "app/main.py"]
