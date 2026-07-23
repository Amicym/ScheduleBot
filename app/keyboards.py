from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime


def build_groups_keyboard(groups: dict[str: str], course: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for group in groups:
        if group["name"].split("-")[1][0] == course:
            builder.row(
                InlineKeyboardButton(
                    text=group["name"],
                    callback_data=f"select_group:{group["id"]}:{course}" 
                )
            )
    
    builder.adjust(2) 
    
    builder.row(InlineKeyboardButton(
        text="Выбрать другой курс",
        callback_data="course_page:"
    ))
    
    return builder.as_markup()

def bluid_course_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for course in range(1, 5):
        builder.add(
            InlineKeyboardButton(
                text=f"{course}",
                callback_data=f"select_course:{course}"
            )
        )
    
    builder.adjust(1)
    
    return builder.as_markup()

def build_schedule_keyboard(group_id, course=None, date=None):
    if date is None:
        date = datetime.today().date().strftime("%Y-%m-%d")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        # [
        # InlineKeyboardButton(text="⚙️ Дополнительные возможности", callback_data=f"additional_features:{date}:{group_id}:{course}"),
        # ],
        
        [
        InlineKeyboardButton(text="👥 Сменить группу", callback_data=f"select_course:{course}"),
        ],

        [
        InlineKeyboardButton(text="◀️ Вчера", callback_data=f"schedule_keyboard:prev:{date}:{group_id}:{course}"),
        InlineKeyboardButton(text="📅 Сегодня", callback_data=f"schedule_keyboard:today:{date}:{group_id}:{course}"),
        InlineKeyboardButton(text="Завтра ▶️", callback_data=f"schedule_keyboard:next:{date}:{group_id}:{course}"),
        ]
    ])

    return kb

def build_additional_features(group_id, course=None, date=None):
    if date is None:
        date = datetime.today().date().strftime("%Y-%m-%d")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text="Выбрать другой курс", callback_data="course_page:")
        ]
    ])

    return kb
