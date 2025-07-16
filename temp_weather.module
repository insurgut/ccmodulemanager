import requests # Необходим для выполнения HTTP-запросов
import random # Если вам понадобится случайный выбор в ваших командах
import re # Для работы с регулярными выражениями, например, для форматирования текста

# Важно: эти функции и переменные доступны для использования в ваших командах
# log(message) - для записи логов плагина
# get_user_config(account) - для получения информации о текущем пользователе
# get_last_fragment() - для получения текущего фрагмента UI (для BulletinHelper)
# BulletinHelper.show_success/show_error/show_info - для отображения уведомлений
# send_message_wrapper(account, peer, text) - для отправки сообщений
# sleep_func(seconds) - для задержки выполнения
# edit_message_func(account, peer, message_id, new_text) - для изменения сообщения
# delete_message_func(account, peer, message_id) - для удаления сообщения
# plugin_instance.get_setting('key') - для доступа к настройкам вашего плагина

def cmd_hello(account, params):
    """
    Пример простой команды, которая приветствует пользователя.
    Пример использования: .hello
    """
    user_config = get_user_config(account)
    user_name = user_config.getCurrentUser().first_name if user_config and user_config.getCurrentUser() else "Пользователь"
    return f"Привет, {user_name}! Я бот с динамическими командами."

def cmd_weather(account, params):
    """
    Показывает текущую погоду для указанного города, используя wttr.in.
    Пример использования: .weather Москва
    """
    command_args = params.message.split(maxsplit=1)
    if len(command_args) < 2:
        return "Пожалуйста, укажите город. Пример: `.weather Москва`"

    location = command_args[1].strip()
    # Удаляем потенциальные Markdown-теги из локации, чтобы избежать проблем с URL
    location = location.replace("*", "").replace("_", "").replace("`", "").replace("~", "").replace("|", "")

    # Формат запроса к wttr.in:
    # %l - Location
    # %t - Temperature
    # %c - Condition code (e.g., Sunny)
    # %C - Condition text (e.g., Clear)
    # %f - Feels like temperature
    # %w - Wind
    # %h - Humidity
    # \\n - перевод строки
    weather_url = f"https://wttr.in/{location}?format=%l:+%t,+%c+%C+\\nОщущается:%f\\nВетер:%w\\nВлажность:%h"
    
    try:
        log(f"[cmd_weather] Запрос погоды для {location} через {weather_url}")
        # Увеличим таймаут на всякий случай
        response = requests.get(weather_url, timeout=15) 
        response.raise_for_status() # Вызывает исключение для HTTP ошибок (4xx, 5xx)

        weather_data = response.text.strip()

        # wttr.in возвращает "Unknown location" или похожие сообщения, если город не найден
        if "Unknown location" in weather_data or "Sorry, no weather information found" in weather_data or "Follow " in weather_data:
            return f"Не удалось найти погоду для города: *{location}*. Пожалуйста, проверьте название или используйте английский."

        # Форматируем температуру жирным шрифтом
        weather_data = re.sub(r'([+\-]?\d+°C)', r'*\1*', weather_data)
        
        # Заменяем стрелки направления ветра на эмодзи для лучшей читаемости
        weather_data = weather_data.replace("←", "⬅️").replace("→", "➡️").replace("↑", "⬆️").replace("↓", "⬇️")
        weather_data = weather_data.replace("↖", "↖️").replace("↗", "↗️").replace("↘", "↘️").replace("↙", "↙️")
        weather_data = weather_data.replace("↔", "↔️").replace("↕", "↕️")

        log(f"[cmd_weather] Получены данные погоды: {weather_data}")
        return weather_data
    except requests.exceptions.RequestException as e:
        log(f"[cmd_weather] Ошибка сети при запросе погоды для {location}: {e}")
        return f"Не удалось получить погоду для *{location}* из-за сетевой ошибки. Попробуйте позже."
    except Exception as e:
        log(f"[cmd_weather] Неожиданная ошибка в cmd_weather для {location}: {e}")
        return f"Произошла непредвиденная ошибка при получении погоды для *{location}*."

