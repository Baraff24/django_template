FROM python:3.11

# Environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the paths for static, media, and log files
ENV STATIC_ROOT=/data/static/
ENV MEDIA_ROOT=/data/media/
ENV LOG_ROOT=/app/logs/

# Install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-dev build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

# Create necessary directories for static, media, and logs
RUN mkdir -p $STATIC_ROOT $MEDIA_ROOT $LOG_ROOT

# Set the working directory
WORKDIR /app

# Copy the necessary files into the container
COPY ./scripts /scripts/
COPY ./app .
COPY ./templates /templates/

# Create a non-root user for celery and ensure permissions
RUN adduser --disabled-password --gecos '' celeryuser \
    && chown -R celeryuser /app $STATIC_ROOT $MEDIA_ROOT $LOG_ROOT

RUN chmod +x /scripts/docker/starter_celery.sh

# Set entrypoint and default command
ENTRYPOINT ["/scripts/docker/wait-for-it.sh", "database:5432" , "-s", "--"]
CMD ["/scripts/docker/starter.sh"]
