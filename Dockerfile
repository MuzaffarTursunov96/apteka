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

RUN pip install --no-cache-dir -r /app/requrement3.txt 
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

# COPY ./server-entrypoint.sh /app/
# RUN chmod +x /app/server-entrypoint.sh
CMD python manage.py runserver 0.0.0.0:8000
