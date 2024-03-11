#!/bin/sh

echo "Effectuer les migrations de la base de données..."
python manage.py makemigrations && python manage.py migrate

echo "Lancer le serveur"

gunicorn sba.wsgi:application --workers=2 --timeout 120 --bind=0.0.0.0:8001