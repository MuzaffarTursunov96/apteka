FROM python:3.11
WORKDIR /app
COPY ./backend ./



RUN pip install --upgrade pip --no-cache-dir
# RUN pip install twisted[http2,tls]
# RUN pip install websocket-client  aiohttp channels daphne django djangorestframework gunicorn
# RUN pip install Pillow python-decouple python-telegram-bot requests django-cors-headers
# RUN pip install --upgrade uvicorn
# RUN pip install hypercorn
# RUN pip install aiogram==2.23.1
COPY ./requrement3.txt /app/

RUN pip install -r /app/requrement3.txt 
# RUN pip install --upgrade Django channels gunicorn daphne
# COPY run.sh /app/

# Make the script executable
# RUN chmod +x /app/run.sh




EXPOSE 8000


# COPY ./server-entrypoint.sh /app/
# COPY ./worker-entrypoint.sh /app/
# #RUN python /app/backend/manage.py createsuperuser --noinput

# # Set executable permissions for entrypoint scripts~
# RUN chmod +x /app/server-entrypoint.sh
# RUN chmod +x /app/worker-entrypoint.sh
# Command to run the script
# CMD ["/app/run.sh"]

# Command to run supervisord
# CMD ["supervisord", "-c", "/app/supervisord.conf"]

#CMD ["daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
# CMD ["gunicorn", "config.asgi:application"]
# CMD gunicorn config.asgi:application -w 3 -b 0.0.0.0:8000  --worker-class uvicorn.workers.UvicornWorker
CMD python manage.py runserver 0.0.0.0:8000
# CMD ["python", "main_bot.py"]


# FROM python:3.9.18-bookworm

# # Install system dependencies
# # RUN apt-get update \ 
# #     && apt-get install -y python3-dev gcc libc-dev bash\
# #     && apt-get clean \
# #     && rm -rf /var/lib/apt/lists/*

# # Create and set the working directory
# WORKDIR /app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# # Copy only the requirements file to leverage Docker caching
# COPY ./requirements.txt /app/

# # Install dependencies
# RUN  pip install -r requirements.txt 



# ADD ./ /app/

# # Copy the rest of the application
# COPY ./server-entrypoint.sh /app/
# COPY ./worker-entrypoint.sh /app/
# #RUN python /app/backend/manage.py createsuperuser --noinput

# # Set executable permissions for entrypoint scripts~
# RUN chmod +x /app/server-entrypoint.sh
# RUN chmod +x /app/worker-entrypoint.sh
