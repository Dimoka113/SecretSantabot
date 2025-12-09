from datetime import datetime

def date_text(dt_str: str|datetime, months_dir: dict) -> str:
    if dt_str is datetime:
        dt = dt_str
    else:
        dt = datetime.strptime(dt_str, r"%d.%m.%Y %H:%M")

    return f"{dt.day} {months_dir[str(dt.month)]} {dt.year} года, в {dt:%H:%M}"


print(date_text("31.12.2025 00:30", {"1": "января", "2": "февраля", "3": "марта", "4": "апреля", "5": "мая", "6": "июня", "7": "июля", "8": "августа", "9": "сентября", "10": "октября", "11": "ноября", "12": "декабря"}))