from datetime import datetime


WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
MONDAY_TIME = {
    "08:30 — 09:55": "09:15 — 10:40",
    "10:05 — 11:30": "10:50 — 12:15",
    "12:25 — 13:50": "13:10 — 14:35",
    "14:00 — 15:25": "14:45 — 16:10",
    "15:35 — 16:55": "16:20 — 17:45",
    "17:05 — 18:30": "17:50 — 19:10",
    "18:40 — 20:05": "19:20 — 20:45",
    "20:15 — 21:40": "20:55 — 22:20",
}

SATURDAY_TIME = {
    "08:30 — 09:55": "08:30 — 09:45",
    "10:05 — 11:30": "09:55 — 11:10",
    "12:25 — 13:50": "11:30 — 12:45",
    "14:00 — 15:25": "12:55 — 14:10",
    "15:35 — 16:55": "14:20 — 15:30",
    "17:05 — 18:30": "15:40 — 16:50", 
}

def format_lesson_time(time_slot: str, date: datetime) -> str:
    if datetime.weekday(date) == 0:
        return MONDAY_TIME.get(time_slot, "Error")

    if datetime.weekday(date) == 5:
        return SATURDAY_TIME.get(time_slot, "Error")

    return time_slot

def format_time_block(time_slot: str, lessons: list[dict], date: str) -> str:
    """Форматирует один временной блок (одна общая пара или 1-2 подгруппы)."""
    time_slot = format_lesson_time(time_slot, date)
    
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
        formatted_blocks.append(format_time_block(time_slot, lessons, date))

    # 3. Собираем итоговое сообщение
    header = f"📅 <b>РАСПИСАНИЕ {string_date} {week_day}</b>\n\n"
    return header + "\n\n".join(formatted_blocks)
