import datetime
import time
import random

# Важно: sleep_func, send_message_wrapper, edit_message_func и plugin_instance
# будут доступны в глобальной области видимости этого динамически загружаемого модуля.
# log также доступен для отладки.

def _get_peer_id(peer_obj):
    """Вспомогательная функция для извлечения числового ID из объекта TLRPC.Peer."""
    if hasattr(peer_obj, 'user_id'):
        return peer_obj.user_id
    elif hasattr(peer_obj, 'channel_id'):
        return -peer_obj.channel_id # Каналы и группы имеют отрицательные ID
    elif hasattr(peer_obj, 'chat_id'):
        return -peer_obj.chat_id # Группы также могут иметь chat_id
    log(f"Не удалось определить peer_id из объекта: {peer_obj}")
    return None # Вернуть None, если ID не найден

def cmd_progress_bar(account, params):
    """
    Динамическая команда, которая имитирует прогресс-бар в чате.
    Использование: .progress
    """
    peer_id = _get_peer_id(params.peer) # Получаем числовой peer_id
    if peer_id is None:
        send_message_wrapper(account, peer_id, "Ошибка: Не удалось определить ID чата для прогресс-бара.")
        return None
    
    message_id = params.id # Получаем ID текущего сообщения для редактирования

    total_steps = 10
    delay_per_step = 0.3 # Секунды

    try:
        # Отправляем первое сообщение, которое будем редактировать
        # Теперь передаем числовой peer_id
        send_message_wrapper(account, peer_id, "Прогресс: [          ] 0%")
        sleep_func(delay_per_step)

        for i in range(1, total_steps + 1):
            filled_blocks = "█" * i
            empty_blocks = " " * (total_steps - i)
            percentage = int((i / total_steps) * 100)
            
            progress_text = f"Прогресс: [{filled_blocks}{empty_blocks}] {percentage}%"
            
            # Редактируем предыдущее сообщение, передавая числовой peer_id
            edit_message_func(account, peer_id, message_id, progress_text)
            sleep_func(delay_per_step)

        edit_message_func(account, peer_id, message_id, "Прогресс: [██████████] 100% Завершено!")
        
    except Exception as e:
        error_text = f"Ошибка прогресс-бара: {e}"
        send_message_wrapper(account, peer_id, error_text)
        log(f"Ошибка в cmd_progress_bar: {e}")

    return None # Возвращаем None, так как сообщения отправляются напрямую

def cmd_loading_animation(account, params):
    """
    Динамическая команда, которая имитирует анимацию загрузки.
    Использование: .load
    """
    peer_id = _get_peer_id(params.peer) # Получаем числовой peer_id
    if peer_id is None:
        send_message_wrapper(account, peer_id, "Ошибка: Не удалось определить ID чата для анимации загрузки.")
        return None
    
    try:
        # Отправляем начальное сообщение через обертку, передавая account, peer_id и текст
        send_message_wrapper(account, peer_id, "Загрузка.")
        sleep_func(0.5) # Небольшая задержка перед началом анимации

        # Анимация загрузки (отправка новых сообщений через обертку)
        for i in range(1, 4): # 3 шага анимации
            send_message_wrapper(account, peer_id, "Загрузка" + "." * (i % 3 + 1))
            sleep_func(0.7) # Задержка между кадрами анимации

        # Финальное сообщение
        send_message_wrapper(account, peer_id, "Загрузка завершена!")
        
    except Exception as e:
        # Отправляем сообщение об ошибке через обертку
        error_text = f"Ошибка анимации загрузки: {e}"
        send_message_wrapper(account, peer_id, error_text)
        log(f"Ошибка в cmd_loading_animation: {e}")

    return None # Возвращаем None, так как сообщения отправляются напрямую

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
        send_message_wrapper(account, peer_id, "Ошибка: Не удалось определить ID чата для броска кубика.")
        return None

    try:
        roll = random.randint(1, 6)
        send_message_wrapper(account, peer_id, f"Вы бросили кубик и выпало число: {roll}!")
    except Exception as e:
        error_text = f"Ошибка при броске кубика: {e}"
        send_message_wrapper(account, peer_id, error_text)
        log(f"Ошибка в cmd_dice: {e}")
    return None

