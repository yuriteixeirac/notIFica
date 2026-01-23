FROM python:3.14.0-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt 
COPY . /app/

EXPOSE 8000
