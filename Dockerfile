FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV STATIC_ROOT /data/static/
ENV MEDIA_ROOT /data/media/
ENV LOG_ROOT /data/log/

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-dev build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

WORKDIR /app
COPY ./scripts /scripts/
COPY ./app .

ENTRYPOINT ["/scripts/docker/wait-for-it.sh", "database:5432" , "-s", "--"]
CMD ["/scripts/docker/starter.sh"]
