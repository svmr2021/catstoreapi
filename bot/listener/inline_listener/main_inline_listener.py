from bot.config import client, store
from bot.keys import KEYS


@client.callback_query_handler(func=lambda call: True)
def animal_list_listener(call):
    if '#>' in call.data:
        store.switch_between_pages(message=call.message, next=True)
    elif "#<" in call.data:
        store.switch_between_pages(message=call.message, next=False)
    elif '#animal_detail' in call.data:
        store.animal_detail(call=call)
    elif call.data == '#back_animal_list':
        state = store.get_state(user_id=call.message.chat.id)
        store.animal_list(message=call.message, delete_prev=True, filter_field=state['filter_field'],
                          filtration_menu=bool(state['filtration_menu']))
    elif call.data == '#filter_open':
        store.animal_list(message=call.message, filtration_menu=False)
    elif call.data == '#filter_close':
        store.animal_list(message=call.message, filtration_menu=True)
    elif call.data == '#sort_species':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='species')
    elif call.data == '#sort_species_down':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='-species')
    elif call.data == '#sort_species_off':
        store.animal_list(message=call.message, filtration_menu=True, filter_field=None)
    elif call.data == '#sort_age':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='age')
    elif call.data == '#sort_age_down':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='-age')
    elif call.data == '#sort_age_off':
        store.animal_list(message=call.message, filtration_menu=True, filter_field=None)