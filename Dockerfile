FROM python:3.11.7-alpine3.19
WORKDIR /app
COPY ./backend ./

# RUN pip install --upgrade pip --no-cache-dir
RUN pip install twisted

RUN pip install -r /app/requirements.txt 

# ENV DJANGO_SETTINGS_MODULE backend.config.settings

CMD [ "python", "manage.py","runserver","0.0.0.0:8000" ]
# CMD ["gunicorn", "-b", "0.0.0.0:8010", "--workers", "7", "-k", "uvicorn.workers.UvicornWorker", "config.asgi:application"] 
# CMD [ "gunicorn", "config.asgi:application","--bind","0.0.0.0:8000" ]
# CMD [ "daphne", "config.asgi:application"]
# CMD [ "daphne", "-u 0.0.0.0","-p 8000","config.asgi:application"]

EXPOSE 8000