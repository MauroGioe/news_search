FROM ollama/ollama

WORKDIR /app
COPY ./run-ollama.sh ./

RUN chmod +x run-ollama.sh
ENTRYPOINT ["/bin/sh", "./run-ollama.sh"]