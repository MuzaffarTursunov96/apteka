FROM python:3.11.7-alpine3.19
WORKDIR /app
COPY ./backend ./



RUN pip install --upgrade pip --no-cache-dir
RUN pip install twisted

RUN pip install -r requirements.txt 

# COPY run.sh /app/

# Make the script executable
# RUN chmod +x /app/run.sh




EXPOSE 8000



# Command to run the script
# CMD ["/app/run.sh"]

# Command to run supervisord
# CMD ["supervisord", "-c", "/app/supervisord.conf"]

# CMD ["daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
# CMD ["gunicorn", "config.asgi:application"]
CMD gunicorn config.asgi:application -w 3 -b 0.0.0.0:8000  --worker-class uvicorn.workers.UvicornWorker
# CMD ["python", "main_bot.py"]
