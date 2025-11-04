import os

# Get bot token from environment variable
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise RuntimeError("Please set the TOKEN environment variable with your Telegram bot token")

# Database file can be configured via environment variable
DB_NAME = os.environ.get('DB_NAME', 'users.json')
