FROM python:3.9-slim


WORKDIR /app
COPY ./requirements.txt ./
COPY ./web_app.py ./
COPY ./web_scraper.py ./

EXPOSE 8501

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright

# Install system dependencies
RUN apt-get update && apt-get install -y

RUN pip install playwright
RUN python -m playwright install --with-deps chromium

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "./web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]