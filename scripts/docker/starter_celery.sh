#!/usr/bin/env bash
set -euo pipefail

exec celery -A config worker --loglevel=info --events
