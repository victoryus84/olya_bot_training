from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)
import tgbot.data.OT_constants as constants   
import tgbot.data.OT_messages as texts

language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=constants.LANGUAGES_DICT.get("en")),
            KeyboardButton(text=constants.LANGUAGES_DICT.get("ro"))
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose a language",
)
    
ok_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="OK")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)

next_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Next")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)

show_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="""Show the interview questions.
                \nAfiseaza intrebarile pentru interviu.""")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click button please",
)        

feed_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Excellent/Excelent"),
            KeyboardButton(text="Acceptable/Acceptabil"),               
            KeyboardButton(text="Poor/Slab")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Click one button please",
)        
    
    