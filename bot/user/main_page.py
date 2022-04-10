import io
import json
import math

from loguru import logger
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from telebot import TeleBot

from bot.keys import KEYS
import urllib.request
from PIL import Image


class CatStore(object):
    def __init__(self, client: TeleBot, web_url: str):
        self.client = client  # Telegram bot instance
        self.web_url = web_url

    def set_or_update_state(self, user_id, kwargs=None):
        """
        Set bot user state
        :param user_id:
        :param kwargs:
        :return:
        """
        try:
            if kwargs is None:
                kwargs = dict(limit=5, offset=0, page_number=1)
            state = self.client.get_state(user_id=user_id)
            if state:
                for k, v in kwargs.items():
                    state[k] = v
            else:
                state = kwargs
            self.client.set_state(user_id=user_id, state=state)
            return state
        except Exception as e:
            logger.error(e)

    def get_state(self, user_id):
        """
        Get bot user state
        :param user_id:
        :return:
        """
        try:
            state = self.client.get_state(user_id=user_id)
            if state:
                return state
            else:
                return self.set_or_update_state(user_id=user_id)

        except Exception as e:
            logger.error(e)

    def main_page(self, message, text=None):
        """
        Main page in bot
        :param message:
        :return:
        """
        try:
            if not text:
                text = KEYS.get('WELCOME').format(message.from_user.first_name)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KEYS.get('LOOK_CATS'), KEYS.get('SEARCH'), row_width=1)
            self.client.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
        except Exception as e:
            logger.error(e)

    def animal_list(self, message, set_state=False, limit=5, offset=0,
                    page_number=1, delete_prev=False, filtration_menu=False, filter_field=None, search=False, search_field=None):
        """
        List of animals
        :param search:
        :param filter_field:
        :param filtration_menu:
        :param delete_prev:
        :param page_number:
        :param set_state:
        :param offset:
        :param limit:
        :param message:
        :return:
        """

        try:
            if set_state:
                self.set_or_update_state(user_id=message.chat.id,
                                         kwargs=dict(limit=limit, offset=offset, page_number=page_number,
                                                     filtration_menu=filtration_menu, filter_field=filter_field,
                                                     search=search, search_field=search_field))
            state = self.get_state(user_id=message.chat.id)
            limit = state['limit']
            offset = state['offset']
            if search:
                self.set_or_update_state(user_id=message.chat.id, kwargs=dict(search=True, search_field=search_field))
                url = self.web_url + '/api/v1/search/'
                payload = dict(limit=limit, offset=offset, q=search_field)
            else:
                url = self.web_url + '/api/v1/list/'
                payload = dict(limit=limit, offset=offset)
            if filter_field:
                payload['ordering'] = filter_field
                self.set_or_update_state(user_id=message.chat.id, kwargs=dict(filter_field=filter_field))
            request = requests.get(url=url, params=payload)
            if request.status_code == 200:
                data = request.json()
                if data['results']:
                    count = data['count']
                    number_of_pages = math.ceil(count / limit)
                    self.set_or_update_state(user_id=message.chat.id, kwargs=dict(max_page_num=number_of_pages))
                    animals = data['results']
                    text = KEYS.get("ANIMAL_LIST")
                    text += '```\n'
                    markup = InlineKeyboardMarkup()
                    buttons = []
                    for index, animal in enumerate(animals):
                        text += f"{index + 1:<1}.{animal['title'] : <19}{animal['species'] : ^0}\n"
                        buttons.append(
                            InlineKeyboardButton(text=animal['title'], callback_data=f'#animal_detail||{animal["id"]}'))
                    text += '```\n'
                    markup.add(*buttons, row_width=1)
                    if data['previous']:
                        previous_text = '<'
                        previous_callback = f'#<||{page_number - 1}'
                    else:
                        previous_text = ' '
                        previous_callback = f' '
                    previous_page = InlineKeyboardButton(text=previous_text, callback_data=previous_callback)
                    if data['next']:
                        next_text = '>'
                        next_callback = f'#>||{page_number + 1}'
                    else:
                        next_text = ' '
                        next_callback = f' '
                    next_page = InlineKeyboardButton(text=next_text, callback_data=next_callback)
                    page_number = state['page_number']
                    page = InlineKeyboardButton(text=f'{page_number}/{number_of_pages}', callback_data=' ')
                    markup.add(previous_page, page, next_page)
                    if filtration_menu:
                        self.set_or_update_state(user_id=message.chat.id, kwargs=dict(filtration_menu=True))
                        filter_text = KEYS.get('FILTER') + '  ⬆️'
                        filter_callback = '#filter_open'
                        markup.add(InlineKeyboardButton(text=filter_text, callback_data=filter_callback))
                        species_text = KEYS.get('SPECIES_SORTING')
                        age_text = KEYS.get('AGE_SORTING')
                        species_callback = '#sort_species'
                        age_callback = '#sort_age'
                        if filter_field == 'species':
                            species_text += ' 🔼'
                            species_callback = '#sort_species_down'
                        elif filter_field == '-species':
                            species_text += ' 🔽'
                            species_callback = '#sort_species_off'
                        elif filter_field == 'age':
                            age_text += ' 🔼'
                            age_callback = '#sort_age_down'
                        elif filter_field == '-age':
                            age_text += ' 🔽'
                            age_callback = '#sort_age_off'
                        species_sort = InlineKeyboardButton(text=species_text, callback_data=species_callback)
                        age_sort = InlineKeyboardButton(text=age_text, callback_data=age_callback)
                        markup.add(species_sort, age_sort)
                    else:
                        self.set_or_update_state(user_id=message.chat.id, kwargs=dict(filtration_menu=False))
                        filter_text = KEYS.get("FILTER") + '  🔽'
                        filter_callback = '#filter_close'
                        markup.add(InlineKeyboardButton(text=filter_text, callback_data=filter_callback))
                    if delete_prev:
                        self.client.delete_message(chat_id=message.chat.id, message_id=message.id)
                    try:
                        self.client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=text,
                                                      parse_mode='MarkdownV2', reply_markup=markup)
                    except:
                        if search:
                            self.main_page(message=message, text=KEYS.get("SEARCH_RESULT"))
                        self.client.send_message(chat_id=message.chat.id, text=text, parse_mode='MarkdownV2',
                                                 reply_markup=markup)
                else:
                    self.client.send_message(chat_id=message.chat.id, text=KEYS.get("NOT_FOUND"))
                    if search:
                        self.search(message=message)
            else:
                self.client.send_message(chat_id=message.chat.id, text=KEYS.get('ERROR'))
        except Exception as e:
            logger.error(e)

    def switch_between_pages(self, message, next=True):
        """
        Switch page in animal list
        :return:
        """
        try:
            state = self.get_state(user_id=message.chat.id)
            offset = state['offset']
            limit = state['limit']
            page_number = state['page_number']
            max_page_num = state['max_page_num']
            filtration_menu = state['filtration_menu']
            filer_field = state['filter_field']
            search = state['search']
            search_field = state['search_field']
            if next:
                if (int(page_number) + 1) <= int(max_page_num):
                    page_number += 1
                    offset += limit
            else:
                if (int(page_number) - 1) > 0:
                    page_number -= 1
                    offset -= limit
            self.set_or_update_state(user_id=message.chat.id,
                                     kwargs=dict(limit=limit, offset=offset, page_number=page_number))
            self.animal_list(message=message, filtration_menu=bool(filtration_menu), filter_field=filer_field,
                             search=bool(search), search_field=bool(search_field))
        except Exception as e:
            logger.error(e)

    def animal_detail(self, call):
        """
        Animal detail inline page
        :param call:
        :return:
        """

        try:
            id = call.data.split('||')[1]
            url = self.web_url + f'/api/v1/detail/{id}'
            request = requests.get(url=url)
            if request.status_code == 200:
                data = request.json()
                r = requests.get(data['image'], stream=True)
                if r.status_code == 200:
                    image = io.BytesIO() # To keep шфьпу in memory
                    image.write(r.content)
                    image.seek(0)
                else:
                    image = open('bot/animal_default.png', 'rb')
                caption = KEYS.get("ANIMAL_DETAIL").format(data['title'], data['species'], data['description'], data['age'] )
                inline = InlineKeyboardMarkup()
                inline.add(InlineKeyboardButton(text=KEYS.get('BACK'), callback_data='#back_animal_list'))
                self.client.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                self.client.send_photo(chat_id=call.message.chat.id, caption=caption, photo=image, reply_markup=inline)
            elif request.status_code == 404:
                self.client.send_message(chat_id=call.message.chat.id, text=KEYS.get('ERROR'))
        except Exception as e:
            logger.error(e)

    def search(self, message):
        """
        Search animals
        :param message:
        :return:
        """
        try:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(KEYS.get('BACK'))
            msg = self.client.send_message(chat_id=message.chat.id, text=KEYS.get('ASK_SEARCH'), reply_markup=markup)
            self.client.register_next_step_handler(msg, self.take_search)
        except Exception as e:
            logger.error(e)

    def take_search(self, message):
        """
        Search animals
        :param message:
        :return:
        """
        try:
            if message.text == KEYS.get('BACK'):
                self.main_page(message=message)
            else:
                self.animal_list(message=message, set_state=True, search=True, search_field=message.text)
        except Exception as e:
            logger.error(e)

