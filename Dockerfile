FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    chromium-driver \
    chromium

# Set environment variables (optional if passed via --env-file)
ENV CHROME_BINARY=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver


WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app/scraper_server.py"]
