FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY docker-entrypoint.sh docker-entrypoint.sh
COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y netcat-traditional \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]

