#!/usr/bin/env bash

echo -e "\e[34m >>> Migrating changes \e[97m"
python manage.py migrate
echo -e "\e[32m >>> migration completed \e[97m"

python manage.py runserver 0.0.0.0:8000