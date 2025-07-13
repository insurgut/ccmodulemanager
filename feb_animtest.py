import datetime # Оставляем для совместимости, если другие команды его используют
import time # Необходим для sleep_func, хотя sleep_func уже передается

# Важно: sleep_func, edit_message_func и plugin_instance
# будут доступны в глобальной области видимости этого динамически загружаемого модуля
# благодаря тому, как они передаются в _extract_and_register_commands.

def cmd_loading_animation(account, params):
    """
    Динамическая команда, которая имитирует анимацию загрузки,
    отправляя последовательные сообщения.
    Использование: .load
    """
    chat_id = params.peer # Объект чата/диалога

    try:
        # Отправляем начальное сообщение
        send_message(account, chat_id, "Загрузка.")
        sleep_func(0.5) # Небольшая задержка перед началом анимации

        # Анимация загрузки (отправка новых сообщений)
        for i in range(1, 4): # 3 шага анимации
            send_message(account, chat_id, "Загрузка" + "." * (i % 3 + 1))
            sleep_func(0.7) # Задержка между кадрами анимации

        # Финальное сообщение
        send_message(account, chat_id, "Загрузка завершена!")
        
    except Exception as e:
        # Отправляем сообщение об ошибке, если что-то пошло не так
        error_text = f"Ошибка анимации загрузки: {e}"
        send_message(account, chat_id, error_text) # Отправляем новое сообщение с ошибкой
        log(f"Ошибка в cmd_loading_animation: {e}")

    return None # Возвращаем None, так как сообщения отправляются напрямую

