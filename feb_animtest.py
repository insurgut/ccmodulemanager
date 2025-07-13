import datetime # Оставляем для совместимости, если другие команды его используют
import time # Необходим для sleep_func, хотя sleep_func уже передается

# Важно: sleep_func, edit_message_func и plugin_instance
# будут доступны в глобальной области видимости этого динамически загружаемого модуля
# благодаря тому, как они передаются в _extract_and_register_commands.

def cmd_loading_animation(account, params):
    """
    Динамическая команда, которая имитирует анимацию загрузки.
    Использование: .load
    """
    chat_id = params.peer # Объект чата/диалога
    message_id = params.id # ID исходного сообщения пользователя (команды)

    try:
        # Начальное сообщение
        edit_message_func(account, chat_id, message_id, "Загрузка.")
        sleep_func(0.5) # Небольшая задержка перед началом анимации

        # Анимация загрузки
        for i in range(1, 4): # 3 шага анимации
            # Проверяем, не превышен ли лимит изменений
            # dynamic_edits_count отслеживается плагином,
            # edit_message_func уже имеет встроенную проверку лимита.
            
            # Если лимит изменений равен 1, то только первое изменение пройдет,
            # и дальнейшие вызовы edit_message_func будут игнорироваться.
            # Для полноценной анимации, лимит должен быть выше (например, 4 или 5).
            edit_message_func(account, chat_id, message_id, "Загрузка" + "." * (i % 3 + 1))
            sleep_func(0.7) # Задержка между кадрами анимации

        # Финальное сообщение
        edit_message_func(account, chat_id, message_id, "Загрузка завершена!")
        
    except Exception as e:
        # Отправляем сообщение об ошибке, если что-то пошло не так
        error_text = f"Ошибка анимации загрузки: {e}"
        # Попытаемся отредактировать сообщение с ошибкой, если это возможно
        edit_message_func(account, chat_id, message_id, error_text)
        log(f"Ошибка в cmd_loading_animation: {e}")

    return None # Возвращаем None, так как сообщение редактируется напрямую

