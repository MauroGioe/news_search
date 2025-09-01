FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y python3-pip

WORKDIR /app
COPY ./requirements.txt ./
COPY ./web_app.py ./
COPY ./web_scraper.py ./

EXPOSE 8501

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright

# Install system dependencies
#RUN apt-get update && apt-get install -y
#RUN apt-get update
#RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

RUN pip install --no-cache-dir -r requirements.txt
RUN PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright python3 -m playwright install --with-deps chromium



ENTRYPOINT ["streamlit", "run", "./web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]