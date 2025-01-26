FROM python:3.9-slim

WORKDIR /app
COPY ./requirements.txt ./
COPY ./web_app.py ./
COPY ./web_scraper.py ./

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["streamlit", "run", "./web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]