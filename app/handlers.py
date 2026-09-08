from datetime import datetime, timedelta
import app.keyboards as kb
import app.api as api
import app.format

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest


rt = Router()

@rt.callback_query(F.data.startswith("schedule_keyboard:"))
async def show_schedule(callback: CallbackQuery, session):
    await callback.answer(text="🚀 Загружаю расписание")
    split_callback_data = callback.data.split(":")

    select = split_callback_data[1]
    date = split_callback_data[2]
    group = split_callback_data[3]
    course = split_callback_data[4]

    if select in {"next", "prev", "today", "prevweek", "nextweek"}:
        shifts = {"next": 1, "prev": -1, "prevweek": -7, "nextweek": 7}
        if select != "today":
            calculated_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=shifts[select])
            current_date = calculated_date.strftime("%Y-%m-%d")
        else:
            current_date = datetime.today().strftime("%Y-%m-%d")

    raw_data = await api.fetch_api(session, id_=group, date=current_date)

    schedule = app.format.create_schedule(raw_data, date=current_date)
    schedule_keyboard = kb.build_schedule_keyboard(group_id=group, date=current_date, course=course)
    
    try:
        await callback.message.edit_text(
            schedule,
            reply_markup=schedule_keyboard,
            parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        if "message is not modified" in e.message:
            pass
        else:
            print(e)

@rt.callback_query(F.data.startswith("additional_features:"))
async def show_additional_features(callback: CallbackQuery):
    await callback.answer("⚙️")

    keyboard = kb.build_additional_features("")
    await callback.message.edit_text(
        text="допвозможности",
        reply_markup=keyboard
    )

@rt.callback_query(F.data.startswith("select_group:"))
async def group_selection(callback: CallbackQuery, session):
    await callback.answer(text="🚀 Загружаю расписание")
    today = datetime.now().date()

    group_id = callback.data.split(":")[1]
    course = callback.data.split(":")[2]

    data = await api.fetch_api(session, group_id)

    schedule = app.format.create_schedule(data, date=today.strftime("%Y-%m-%d"))

    schedule_keyboard = kb.build_schedule_keyboard(group_id=group_id, course=course)

    await callback.message.edit_text(
        schedule,
        reply_markup=schedule_keyboard,
        parse_mode="HTML"
    )

@rt.callback_query(F.data.startswith("select_course:"))
async def course_selection(callback: CallbackQuery, session):
    await callback.answer(text="🚀 Загружаю группы")
    course = callback.data.split(":")[1][0]
    data = await api.fetch_api(session)
    
    group_keyboard = kb.build_groups_keyboard(data, course)

    await callback.message.edit_text(
        text="📌 **Выберите вашу группу из списка ниже:**",
        reply_markup=group_keyboard,
        parse_mode="Markdown"
    )

@rt.message(Command("malstroy"))
async def get_photo(message: Message):
    photo = "AgACAgIAAxkBAAOHalzIKQjE2aL-bn_FE_cy29ktGMUAArAZaxsje-lKCOhmZ4X4SAEBAAMCAANtAAM9BA"
    for _ in range(10):    
        await message.answer_photo(photo, caption="МАЛСТРОЙ")

@rt.callback_query(F.data.startswith("course_page:"))
async def course_page(callback: CallbackQuery):
    await _show_course_page(callback.message, edit=True)

@rt.message(CommandStart())
async def cmd_start(message: Message):
    # data = str(message.from_user).split(" ")
    # for d in data[:]:
    #     if "None" in d:
    #         data.remove(d)
    
    # await message.answer("\n".join(data))
    await _show_course_page(message)

@rt.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "🎓 <b>Как пользоваться ботом?</b>\n\n"
        "Этот бот помогает быстро узнавать актуальное расписание пар. "
        "Все данные берутся напрямую с сайта.\n\n"
        "🕹 <b>Навигация:</b>\n"
        "<b>1.</b> Нажмите /start, чтобы выбрать свой курс и группу.\n"
        "<b>2.</b> Бот пришлет расписание на текущий день.\n"
        "<b>3.</b> Используйте кнопки под сообщением, чтобы переключать дни (◀️ ... / ... ▶️).\n\n"
        "🔄 <b>Если нужно сменить группу:</b>\n"
        "Нажмите кнопку <i>«👥 Сменить группу»</i> под расписанием или введи команду /start.\n\n"
        "🛠 <b>Доступные команды:</b>\n"
        "/start — Запустить бота\n"
        "/help — Показать эту справку"
    )

    await message.answer(
        text=help_text,
        parse_mode="HTML"
    )

async def _show_course_page(message: Message, edit=False):
    metod_name = "edit_text" if edit else "answer"
    metod = getattr(message, metod_name)
    
    await metod(
        "🎓 <b>Выберите курс:</b>",
        reply_markup=kb.bluid_course_keyboard(),
        parse_mode="HTML"
        )