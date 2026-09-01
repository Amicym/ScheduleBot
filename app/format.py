from datetime import datetime


WEEK_DAY = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

def format_time_block(time_slot: str, lessons: list[dict]) -> str:
    """Форматирует один временной блок (одна общая пара или 1-2 подгруппы)."""
    text = [f"⏱️ <code>{time_slot}</code>"]

    for data in lessons:
        room = f"каб. {data['room']}" if data['room'] != "дист" else "<i>дистант</i>"
        
        if data.get("subgroup"):
            text.append(f"👥 <b>{data['subgroup']}-я подгруппа:</b>")


        text.append(f"📘 <b>{data['subject']}</b> — {data['teacher']}")
        text.append(f"📍 {room}")

    return "\n".join(text)


def create_schedule(data: list, date: str | datetime) -> str:
    date = datetime.strptime(date, "%Y-%m-%d")
    string_date = date.strftime("%Y-%m-%d")
    week_day = WEEK_DAYS[date.weekday()]
    
    if not data:
        return f"ℹ️ На <b>{string_date} {week_day}</b> расписание отсутствует."
    
    # 1. Группируем предметы по их времени (сохраняя порядок появления)
    grouped_by_time: dict[str, list[dict]] = {}
    for item in data:
        time_slot = item["time"]
        if time_slot not in grouped_by_time:
            grouped_by_time[time_slot] = []
        grouped_by_time[time_slot].append(item)

    # 2. Форматируем каждый временной блок
    formatted_blocks = []
    for time_slot, lessons in grouped_by_time.items():
        formatted_blocks.append(format_time_block(time_slot, lessons))

    # 3. Собираем итоговое сообщение
    header = f"📅 <b>РАСПИСАНИЕ {string_date} {week_day}</b>\n\n"
    return header + "\n\n".join(formatted_blocks)