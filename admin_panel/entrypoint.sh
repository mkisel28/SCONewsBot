#!/usr/bin/env bash


echo "Applying migrations..."
python manage.py migrate --noinput


echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
