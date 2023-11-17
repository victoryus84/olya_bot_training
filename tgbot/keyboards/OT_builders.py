from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from tgbot.data.OT_constants import UNIVERSITIES_ARRAY, LANGUAGES_ARRAY, BOOL_DICT
from tgbot.callbacks.OT_procedures import *
from tgbot.utils import postgres

def language_reply():
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in LANGUAGES_ARRAY]
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def universities_reply():
    
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM public.app_telegram_university""")
    university_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in university_names]
    # builder.button(text="Cancel")
    builder.adjust(*[4] * 4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def courses_reply(university):
    print (university)
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT courses.name 
                      FROM public.app_telegram_course courses
                      INNER JOIN public.app_telegram_university universities ON courses.university_id = universities.id
                      WHERE universities.name = %s""", (university,))
    univ_courses = [row[0] for row in cursor.fetchall()]
    print(univ_courses)
    cursor.close()
    # univ_courses = get_courses_for_university(university)
    
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in univ_courses]
    # builder.button(text="Cancel")
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def bool_reply(language):
    bool_array = BOOL_DICT.get(language)
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in bool_array]
    # builder.button(text="Cancel")
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]
    
    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# ////////// inline kbd //////////
def languages_inline():
    
    builder = InlineKeyboardBuilder()
    
    for element in LANGUAGES_ARRAY:
        builder.add(InlineKeyboardButton(
        text=element,
        callback_data=element)
    )
        
    builder.adjust(*[2] * 4)

    return builder.as_markup(resize_keyboard=True)

def universities_inline():
    
    builder = InlineKeyboardBuilder()
    for element in UNIVERSITIES_ARRAY:
        builder.add(InlineKeyboardButton(
        text=element,
        callback_data=element)
    )
    
    builder.adjust(*[4] * 4)

    return builder.as_markup(resize_keyboard=True)





