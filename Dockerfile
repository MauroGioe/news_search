FROM python:3.9-slim
FROM ollama/ollama

WORKDIR /app
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run-ollama.sh

EXPOSE 12000