#!/bin/sh
python manage.py makemigrations tickets
python manage.py migrate

python manage.py collectstatic --noinput
/usr/local/bin/gunicorn project.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/usr/src/app
