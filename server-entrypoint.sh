#!/bin/sh


# until python manage.py migrate
# do
#     echo "Waiting for db to be ready..."
#     sleep 2
# done


# python manage.py collectstatic --noinput


# python manage.py createsuperuser --noinput

#gunicorn core.wsgi --bind 0.0.0.0:8000

# for debug
python manage.py runserver 0.0.0.0:8000
# gunicorn config.asgi:application -w 3 -b 0.0.0.0:8000  --worker-class uvicorn.workers.UvicornWorker
