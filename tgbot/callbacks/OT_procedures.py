from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

router = Router()

# Funcția care returnează cursurile unei universități
def get_dict_key_from_value(val, my_dict):
   
    for key, value in my_dict.items():
        if val == value:
            return key
 
    return print(f"for value {val} key doesn't exist")

# @router.callback_query_handler(F.Text(equals="my_button_data"))
# async def my_button_callback(callback_query: CallbackQuery):
#     # Gestionează acțiunea butonului aici
#     print(f"my_button_callback")
#     await callback_query.answer("Ai apăsat pe 'My Button'")
