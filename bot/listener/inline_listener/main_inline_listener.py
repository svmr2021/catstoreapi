from bot.config import client, store
from bot.keys import KEYS


@client.callback_query_handler(func=lambda call: True)
def animal_list_listener(call):
    state = store.get_state(user_id=call.message.chat.id)
    search = bool(state['search'])
    search_field = state['search_field']
    if '#>' in call.data:
        store.switch_between_pages(message=call.message, next=True)
    elif "#<" in call.data:
        store.switch_between_pages(message=call.message, next=False)
    elif '#animal_detail' in call.data:
        store.animal_detail(call=call)
    elif call.data == '#back_animal_list':
        store.animal_list(message=call.message, delete_prev=True, filter_field=state['filter_field'],
                          filtration_menu=bool(state['filtration_menu']), search=search, search_field=search_field)
    elif call.data == '#filter_open':
        store.animal_list(message=call.message, filtration_menu=False, search=search, search_field=search_field)
    elif call.data == '#filter_close':
        store.animal_list(message=call.message, filtration_menu=True, search=search, search_field=search_field)
    elif call.data == '#sort_species':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='species', search=search,
                          search_field=search_field)
    elif call.data == '#sort_species_down':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='-species', search=search,
                          search_field=search_field)
    elif call.data == '#sort_species_off':
        store.animal_list(message=call.message, filtration_menu=True, filter_field=None, search=search,
                          search_field=search_field)
    elif call.data == '#sort_age':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='age', search=search,
                          search_field=search_field)
    elif call.data == '#sort_age_down':
        store.animal_list(message=call.message, filtration_menu=True, filter_field='-age', search=search,
                          search_field=search_field)
    elif call.data == '#sort_age_off':
        store.animal_list(message=call.message, filtration_menu=True, filter_field=None, search=search,
                          search_field=search_field)