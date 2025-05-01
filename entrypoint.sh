#!/bin/bash

echo "==> ✅ Entered entrypoint.sh"

echo "==> 🔥 Deleting old migration files (excluding __init__.py)..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
echo "==> Migrations deleted..."

echo "==> 📦 Making and applying migrations..."
python manage.py makemigrations users student teacher
python manage.py migrate users
python manage.py migrate student
python manage.py migrate teacher
python manage.py makemigrations
python manage.py migrate

echo "==> 👤 Creating superuser if not exists..."
echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create_superuser('admin@gmail.com', '12345')
" | python manage.py shell

echo "==> 🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "==> 🚀 Starting server..."
gunicorn school.wsgi:application --bind 0.0.0.0:8000
