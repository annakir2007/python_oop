"""
Функции валидации для класса Apartment.
"""

from datetime import datetime

def validate_address(value, field_name, min_length=5):
    """
    Проверка корректности адреса.
    
    Args:
        value: проверяемое значение
        field_name: название поля (для сообщений об ошибках)
        min_length: минимальная длина адреса
        
    Returns:
        str: очищенный адрес(с удалёнными пробелами по краям)
        
    Raises:
        TypeError: если значение не строка
        ValueError: если адрес пустой или слишком короткий
    """
    if not isinstance(value, str):
        raise TypeError(f"{field_name} должен быть строкой")
    
    value = value.strip()
    
    if len(value) == 0:
        raise ValueError(f"{field_name} не может быть пустым")
    
    if len(value) < min_length:
        raise ValueError(f"{field_name} слишком короткий (минимум {min_length} символов)")
    
    return value


def validate_area(area, min_val, max_val):
    """
    Проверка корректности площади.
    
    Args:
        area: проверяемое значение
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
        
    Returns:
        float: площадь
        
    Raises:
        TypeError: если значение не число
        ValueError: если значение вне допустимого диапазона
    """
    if not isinstance(area, (int, float)):
        raise TypeError("Площадь должна быть числом")
    
    if min_val <= area <= max_val:
        return float(area)
    
    raise ValueError(f"Площадь должна быть от {min_val} до {max_val} кв.м")


def validate_rooms(rooms, min_val, max_val):
    """
    Проверка корректности количества комнат.
    
    Args:
        rooms: проверяемое значение
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
        
    Returns:
        int: количество комнат
        
    Raises:
        TypeError: если значение не целое число
        ValueError: если значение вне допустимого диапазона
    """
    if not isinstance(rooms, int):
        raise TypeError("Количество комнат должно быть целым числом")
    
    if min_val <= rooms <= max_val:
        return rooms
    
    raise ValueError(f"Количество комнат должно быть от {min_val} до {max_val}")


def validate_price(price, min_val, max_val):
    """
    Проверка корректности цены.
    
    Args:
        price: проверяемое значение
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
        
    Returns:
        float: цена
        
    Raises:
        TypeError: если значение не число
        ValueError: если значение вне допустимого диапазона
    """
    if not isinstance(price, (int, float)):
        raise TypeError("Цена должна быть числом")
    
    if min_val <= price <= max_val:
        return float(price)
    
    raise ValueError(f"Цена должна быть от {min_val:.0f} до {max_val:.0f} руб.")


def validate_floor(floor, min_val, max_val):
    """
    Проверка корректности этажа.
    
    Args:
        floor: проверяемое значение
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
        
    Returns:
        int: этаж
        
    Raises:
        TypeError: если значение не целое число
        ValueError: если значение вне допустимого диапазона
    """
    if not isinstance(floor, int):
        raise TypeError("Этаж должен быть целым числом")
    
    if min_val <= floor <= max_val:
        return floor
    
    raise ValueError(f"Этаж должен быть от {min_val} до {max_val}")


def validate_construction_year(year):
    """
    Проверка корректности года постройки.
    
    Args:
        year: проверяемое значение
        
    Returns:
        int: год постройки
        
    Raises:
        TypeError: если значение не целое число
        ValueError: если значение вне допустимого диапазона
    """
    if not isinstance(year, int):
        raise TypeError("Год постройки должен быть целым числом")
    
    current_year = datetime.now().year
    
    if 1800 <= year <= current_year:
        return year
    
    raise ValueError(f"Год постройки должен быть от 1800 до {current_year}")