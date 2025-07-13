import datetime
import time

# Важно: sleep_func, send_message_wrapper и plugin_instance
# будут доступны в глобальной области видимости этого динамически загружаемого модуля.

def cmd_loading_animation(account, params):
    """
    Динамическая команда, которая имитирует анимацию загрузки,
    отправляя последовательные сообщения.
    Использование: .load
    """
    chat_id = params.peer # Получаем peer из params

    try:
        # Отправляем начальное сообщение через обертку, передавая account, chat_id и текст
        send_message_wrapper(account, chat_id, "Загрузка.")
        sleep_func(0.5) # Небольшая задержка перед началом анимации

        # Анимация загрузки (отправка новых сообщений через обертку)
        for i in range(1, 4): # 3 шага анимации
            send_message_wrapper(account, chat_id, "Загрузка" + "." * (i % 3 + 1))
            sleep_func(0.7) # Задержка между кадрами анимации

        # Финальное сообщение
        send_message_wrapper(account, chat_id, "Загрузка завершена!")
        
    except Exception as e:
        # Отправляем сообщение об ошибке через обертку
        error_text = f"Ошибка анимации загрузки: {e}"
        send_message_wrapper(account, chat_id, error_text)
        # log(f"Ошибка в cmd_loading_animation: {e}") # log также доступен, если нужно

    return None # Возвращаем None, так как сообщения отправляются напрямую

def cmd_time(account, params):
    """
    Динамическая команда, которая возвращает текущее время.
    Использование: .time
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"Текущее время: {current_time}"
    #55511521
