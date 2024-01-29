#!/bin/bash

# Run Daphne
daphne config.asgi:application -b 0.0.0.0 -p 8000 &

# Run your Telegram bot script (replace with the actual script name)
python your_telegram_bot_script.py

# Keep the script running to prevent the container from exiting
tail -f /dev/null