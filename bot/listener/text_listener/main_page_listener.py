from bot.config import client, store
from bot.keys import KEYS


@client.message_handler(content_types=['text'])
def main_page_listener(message):
    if message.text == KEYS.get('LOOK_CATS'):
        store.animal_list(message=message, set_state=True)