import datetime
import time
import random
# requests больше не нужен, так как мы не используем внешний API погоды

# Важно: sleep_func, send_message_wrapper, edit_message_func и plugin_instance
# будут доступны в глобальной области видимости этого динамически загружаемого модуля.
# log также доступен для отладки.

def _get_peer_id(peer_obj):
    """Вспомогательная функция для извлечения числового ID из объекта TLRPC.Peer."""
    try:
        if hasattr(peer_obj, 'user_id') and peer_obj.user_id != 0:
            return peer_obj.user_id
        elif hasattr(peer_obj, 'channel_id') and peer_obj.channel_id != 0:
            return -peer_obj.channel_id # Каналы и группы имеют отрицательные ID
        elif hasattr(peer_obj, 'chat_id') and peer_obj.chat_id != 0:
            return -peer_obj.chat_id # Группы также могут иметь chat_id
        # Дополнительная проверка на случай, если peer_obj сам является числовым ID или имеет атрибут 'id'
        elif isinstance(peer_obj, (int, float)):
            return int(peer_obj)
        elif hasattr(peer_obj, 'id') and peer_obj.id != 0:
            # Попытка получить id напрямую, если он существует
            # Важно: для каналов/чатов может потребоваться отрицательное значение
            if hasattr(peer_obj, 'access_hash') and peer_obj.access_hash != 0: # Проверка на тип объекта
                return -peer_obj.id # Предполагаем, что это канал/чат
            else:
                return peer_obj.id # Предполагаем, что это пользователь
        
        log(f"Не удалось определить peer_id из объекта: Тип={type(peer_obj)}, Объект={peer_obj}, Атрибуты={dir(peer_obj)}")
        return None # Вернуть None, если ID не найден
    except Exception as e:
        log(f"Ошибка в _get_peer_id: {e}. Объект: {peer_obj}")
        return None


def cmd_time(account, params):
    """
    Динамическая команда, которая возвращает текущее время.
    Использование: .time
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Текущее время: {current_time}"

def cmd_dice(account, params):
    """
    Динамическая команда, которая имитирует бросок кубика.
    Использование: .dice
    """
    peer_id = _get_peer_id(params.peer)
    if peer_id is None:
        send_message_wrapper(account, params.peer, "Ошибка: Не удалось определить ID чата для броска кубика.")
        return None

    try:
        roll = random.randint(1, 6)
        send_message_wrapper(account, peer_id, f"Вы бросили кубик и выпало число: {roll}!")
    except Exception as e:
        error_text = f"Ошибка при броске кубика: {e}"
        send_message_wrapper(account, peer_id, error_text)
        log(f"Ошибка в cmd_dice: {e}")
    return None

def cmd_weather(account, params):
    """
    Динамическая команда, которая показывает симулированную погоду для указанного города.
    Не использует внешний API.
    Использование: .w <город>
    Например: .w Москва
    """
    peer_id = _get_peer_id(params.peer)
    if peer_id is None:
        send_message_wrapper(account, params.peer, "Ошибка: Не удалось определить ID чата для запроса погоды.")
        return None

    args = params.message.split(maxsplit=1)
    if len(args) < 2:
        send_message_wrapper(account, peer_id, "Пожалуйста, укажите город. Пример: .w Москва")
        return None
    
    city_name = args[1].strip().capitalize()

    try:
        # Генерируем случайную температуру
        temperature = random.randint(-10, 30) # От -10 до +30 градусов Цельсия
        
        # Выбираем случайное описание погоды
        weather_descriptions = [
            "ясно",
            "облачно",
            "небольшой дождь",
            "пасмурно",
            "снег",
            "солнечно",
            "туман",
            "гроза",
            "переменная облачность"
        ]
        weather_description = random.choice(weather_descriptions)

        # Генерируем случайную влажность и скорость ветра
        humidity = random.randint(40, 95)
        wind_speed = round(random.uniform(1.0, 10.0), 1) # От 1.0 до 10.0 м/с

        # Формируем сообщение о погоде
        weather_message = (
            f"Симулированная погода в {city_name}:\n"
            f"Температура: {temperature}°C\n"
            f"Описание: {weather_description.capitalize()}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        send_message_wrapper(account, peer_id, weather_message)

    except Exception as e:
        error_text = f"Произошла ошибка при симуляции погоды: {e}"
        send_message_wrapper(account, peer_id, error_text)
        log(f"Ошибка в cmd_weather (симуляция): {e}")
    
    return None

