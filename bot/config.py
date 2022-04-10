""" Creating bot instance """

import telebot
from django.conf import settings

from bot.user.main_page import CatStore
from skillboxcatapi.settings import config
from loguru import logger
from telebot import apihelper


client = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
store = CatStore(client=client, web_url=settings.WEB_URL)


def run_bot(none_stop=True, interval=0):
    """ Runs bot, called in run_pooling.py """

    from bot.listener import commands_listener
    from bot.listener.text_listener import  main_page_listener
    from bot.listener.inline_listener import main_inline_listener
    logger.info(f"Starting bot, {client}")
    client.infinity_polling(timeout=30)
