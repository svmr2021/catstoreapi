import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillboxcatapi.settings')
django.setup()

from bot.config import run_bot

if __name__ == "__main__":
    run_bot()