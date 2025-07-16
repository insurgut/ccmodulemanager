from PIL import Image

def pixelize(image: Image.Image, pixel_size: int = 10) -> Image.Image:
    """
    Применяет эффект "большие пиксели" к изображению.

    Аргументы:
        image (Image.Image): Исходное изображение PIL.
        pixel_size (int): Размер "пикселя" для эффекта. Большее значение приводит к большей пикселизации.
                          По умолчанию 10.

    Возвращает:
        Image.Image: Изображение с примененным эффектом пикселизации.
    """
    if not isinstance(pixel_size, int) or pixel_size <= 0:
        # В случае некорректного значения, устанавливаем безопасное значение по умолчанию.
        # Это поможет избежать ошибок, если параметр будет передан неверно.
        pixel_size = 10 

    width, height = image.size
    
    # Вычисляем целевые размеры для уменьшенного изображения.
    # Убеждаемся, что размеры не меньше 1, чтобы избежать ошибок при очень больших pixel_size.
    target_width = max(1, width // pixel_size)
    target_height = max(1, height // pixel_size)

    # Уменьшаем изображение с использованием интерполяции NEAREST.
    # Это ключевой шаг для создания "блочного" или "пиксельного" эффекта.
    small_image = image.resize((target_width, target_height), Image.NEAREST)

    # Увеличиваем изображение обратно до исходных размеров,
    # что завершает эффект пикселизации.
    return small_image.resize((width, height), Image.NEAREST)
