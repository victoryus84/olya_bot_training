from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, user
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from tgbot.data.OT_messages import (
    HELP_MESSAGE, BEGIN_MESSAGE, LANGUAGE_MESSAGE,
    UNIVERSITY_MESSAGES, COURSES_MESSAGES, COURSES_MESSAGES_BEGIN,
    COURSES_MESSAGES_WHY, COURSES_CANCEL
    )
from tgbot.data.OT_constants import (
    LANGUAGES_DICT,
    )
from tgbot.keyboards import OT_builders, OT_inline, OT_reply
from tgbot.callbacks.OT_procedures import *

from tgbot.utils.states import Questions
from tgbot.utils import postgres

router = Router()

@router.message(F.text.lower().in_(["hi", "hello", "привет"]))
async def greetings(message: Message):
    await message.reply("Hello mate! (MENU->START OR type <</start>>)")

@router.message(Command(commands=["help"]))
async def help(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, HELP_MESSAGE[0])
    # print(message.from_user.url, message.from_user.full_name)
        
# @router.message(CommandStart(), IsAdmin(1490170564))
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Questions.BEGIN)
    await message.answer(BEGIN_MESSAGE.get("all"), 
                         reply_markup=OT_inline.begin_markup)
    
@router.callback_query(F.data == "begin", Questions.BEGIN)
async def language_choise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Questions.LANGUAGE)
    await callback.message.answer(LANGUAGE_MESSAGE.get("all"), 
                                  reply_markup=OT_builders.language_reply(),
                                  disable_notification=True)  
    
@router.message(Questions.LANGUAGE)
async def univerersity_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(LANGUAGE=get_dict_key_from_value(message.text, LANGUAGES_DICT))
    await state.set_state(Questions.UNIVERSITY)
    data = await state.get_data()
    await message.answer(UNIVERSITY_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.universities_reply(),
                         disable_notification=True)
    
@router.message(Questions.UNIVERSITY)
async def course_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(UNIVERSITY=message.text)
    await state.set_state(Questions.COURSE)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES.get(data["LANGUAGE"]), 
                         reply_markup=OT_builders.courses_reply(message.text),
                         disable_notification=True)
    
@router.message(Questions.COURSE)
async def course_handler_begin(message: Message, state: FSMContext) -> None:
    await state.update_data(COURSE=message.text)
    data = await state.get_data()
    await message.answer(COURSES_MESSAGES_BEGIN.get(data["LANGUAGE"]), 
                         reply_markup=OT_inline.begin_course_markup)
    
@router.callback_query(F.data == "begin_course", Questions.COURSE)
async def course_handler_begin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await callback.message.answer(COURSES_MESSAGES_WHY.get(data["LANGUAGE"]), reply_markup=ReplyKeyboardRemove())      
    
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT 
                            courses.name,
                            courses.fullname, 
                            universities.fullname
                            FROM public.app_telegram_course courses
                            INNER JOIN public.app_telegram_university universities ON courses.university_id = universities.id
                            WHERE universities.name = %s AND courses.name = %s""", (data["UNIVERSITY"], data["COURSE"]))
    course_mess = cursor.fetchone()
    cursor.close()
    full_university = course_mess[2]
    full_course = course_mess[1]
    
    aprove_text = f"Ai aplicat la cursul <b><u>{full_course}</u></b>  universitatea <b><u>{full_university}</u></b> ?" 
    await callback.message.answer(aprove_text, reply_markup=OT_builders.bool_reply(data["LANGUAGE"]))      

    await state.set_state(Questions.CHOICE)
    await state.update_data(CHOICE=callback.message.text)
    data = await state.get_data()
    
@router.message(Questions.CHOICE)
async def course_handler_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if (message.text == "No/Nu") or (message.text == "No"):
        # await message.answer("...", reply_markup=ReplyKeyboardRemove())      
        await message.answer(COURSES_CANCEL.get(data["LANGUAGE"]))
        # await state.clear()
    else:
        conn = postgres.get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT message
                            FROM public.app_telegram_coursemessage c_mess
                            INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                            WHERE courses.name = %s
                            AND c_mess.language = %s
                            AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 1))
        course_mess = cursor.fetchone()
        cursor.close()
        await message.answer(course_mess[0], reply_markup=OT_reply.ok_markup)
        await state.set_state(Questions.CHOICE1)
        
@router.message(Questions.CHOICE1)
async def course_handler_choice2(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 2))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)
    await state.set_state(Questions.CHOICE2)

@router.message(Questions.CHOICE2)
async def course_handler_choice3(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 3))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.show_markup)
    await state.set_state(Questions.CHOICE3)
    
@router.message(Questions.CHOICE3)
async def course_handler_choice4(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 4))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)
    await state.set_state(Questions.CHOICE4)

@router.message(Questions.CHOICE4)
async def course_handler_choice5(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 5))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE5)
    
@router.message(Questions.CHOICE5)
async def course_handler_choice6(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 6))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE6)   
    
@router.message(Questions.CHOICE6)
async def course_handler_choice7(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 7))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE7)  
    
@router.message(Questions.CHOICE7)
async def course_handler_choice8(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 8))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE8)         
    
@router.message(Questions.CHOICE8)
async def course_handler_choice9(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 9))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE9)    
    
@router.message(Questions.CHOICE9)
async def course_handler_choice10(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 10))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE10)  
    
@router.message(Questions.CHOICE10)
async def course_handler_choice11(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 11))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE11) 
    
@router.message(Questions.CHOICE11)
async def course_handler_choice12(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 12))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE12)   
    
@router.message(Questions.CHOICE12)
async def course_handler_choice13(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 13))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE13)  
    
@router.message(Questions.CHOICE13)
async def course_handler_choice14(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 14))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE14) 
    
@router.message(Questions.CHOICE14)
async def course_handler_choice15(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 15))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE15) 
    
@router.message(Questions.CHOICE15)
async def course_handler_choice16(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 16))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE16)                      
    
@router.message(Questions.CHOICE16)
async def course_handler_choice17(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 17))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE17)   
    
@router.message(Questions.CHOICE17)
async def course_handler_choice18(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 18))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE18)              
    
@router.message(Questions.CHOICE18)
async def course_handler_choice19(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 19))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE19)                  
    
@router.message(Questions.CHOICE19)
async def course_handler_choice20(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 20))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE20)         
    
@router.message(Questions.CHOICE20)
async def course_handler_choice21(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 21))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE21)      
    
@router.message(Questions.CHOICE21)
async def course_handler_choice22(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 22))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE22)    
    
@router.message(Questions.CHOICE22)
async def course_handler_choice23(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 23))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE23)
    
@router.message(Questions.CHOICE23)
async def course_handler_choice24(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 24))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_builders.bool_reply(data["LANGUAGE"]))    
    await state.set_state(Questions.CHOICE24)          
    
@router.message(Questions.CHOICE24)
async def course_handler_choice25(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT c_mess.message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 25))
    course_mess = cursor.fetchall()
    cursor.close()
    
    if (message.text == "No/Nu") or (message.text == "No"):
        await message.answer(course_mess[1][0], reply_markup=OT_reply.next_markup)
    else:
        await message.answer(course_mess[0][0], reply_markup=OT_reply.next_markup)
        
    await state.set_state(Questions.CHOICE25)
    
@router.message(Questions.CHOICE25)
async def course_handler_choice26(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 26))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE26)   
    
@router.message(Questions.CHOICE26)
async def course_handler_choice27(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 27))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE27)            

@router.message(Questions.CHOICE27)
async def course_handler_choice28(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 28))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE28)       
    
@router.message(Questions.CHOICE28)
async def course_handler_choice29(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 29))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(course_mess[0], reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE29) 
    
@router.message(Questions.CHOICE29)
async def course_handler_choice30(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conn = postgres.get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT message
                        FROM public.app_telegram_coursemessage c_mess
                        INNER JOIN public.app_telegram_course courses ON courses.id = c_mess.course_id
                        WHERE courses.name = %s
                        AND c_mess.language = %s
                        AND c_mess.step = %s""", (data["COURSE"], data["LANGUAGE"], 30))
    course_mess = cursor.fetchone()
    cursor.close()
    await message.answer(f"<b>{course_mess[0]}</b>", reply_markup=OT_reply.next_markup)    
    await state.set_state(Questions.CHOICE30)                

    