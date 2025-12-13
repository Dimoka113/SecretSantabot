from datetime import datetime

def date_text(dt_str: str|datetime, months_dir: dict) -> str:
    if dt_str is datetime:
        dt = dt_str
    else:
        dt = datetime.strptime(dt_str, r"%d.%m.%Y %H:%M")

    return f"{dt.day} {months_dir[str(dt.month)]} {dt.year} года, в {dt:%H:%M}"