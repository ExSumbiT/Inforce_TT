#!/bin/bash

python manage.py makemigrations employee restaurant --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000