import datetime

def cmd_time(account, params):
    """
    Динамическая команда, которая возвращает текущее время.
    Использование: .time
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Текущее время: {current_time}"
