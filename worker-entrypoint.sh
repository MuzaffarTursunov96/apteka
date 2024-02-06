#!/bin/sh

# run a worker 🙂
celery -A core worker --loglevel=info -P prefork -c 50 -E
