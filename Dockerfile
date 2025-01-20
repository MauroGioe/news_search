FROM python:3.9-slim

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app
COPY ./requirements.txt ./
COPY ./run-ollama.sh ./

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run-ollama.sh

EXPOSE 12000