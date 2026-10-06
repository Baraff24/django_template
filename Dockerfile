FROM python:3.14.8-slim-trixie

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings.development \
    STATIC_ROOT=/vol/staticfiles \
    MEDIA_ROOT=/vol/mediafiles \
    LOG_ROOT=/data/logs

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --require-hashes -r /tmp/requirements.txt \
    && pip check \
    && rm /tmp/requirements.txt

COPY ./scripts /scripts/
COPY pyproject.toml /pyproject.toml
COPY ./app /app/
COPY ./templates /templates/

RUN adduser --disabled-password --gecos '' celeryuser \
    && mkdir -p "$STATIC_ROOT" "$MEDIA_ROOT" "$LOG_ROOT" /data/celery \
    && chown -R celeryuser /app /data/celery "$STATIC_ROOT" "$MEDIA_ROOT" "$LOG_ROOT" \
    && chmod +x /scripts/docker/*.sh

EXPOSE 8000
CMD ["/scripts/docker/starter.sh"]
