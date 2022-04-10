from bot.config import client, store
# from bot.user.admin.send_messages import send_messages
# from bot.user.registered_user.main_page import main_page
from loguru import logger


@client.message_handler(commands=['start'])
def commands_listener(message):
    try:
        store.main_page(message=message)
    except Exception as e:
        logger.error(e)
