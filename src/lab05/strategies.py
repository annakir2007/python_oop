"""
Модуль стратегий для работы с объектами недвижимости.
"""

def by_price(item) -> float:
    """Сортировка по цене недвижимости."""
    return item.price


def by_area(item) -> float:
    """Сортировка по площади недвижимости."""
    return item.area


def by_price_per_square_meter(item) -> float:
    """Сортировка по цене за квадратный метр."""
    return item.price / item.area if item.area > 0 else float('inf')


# ========== 2 функции-фильтра ==========

def is_expensive(item) -> bool:
    """Проверяет, дорогой ли объект (цена > 10 млн)."""
    return item.price > 10_000_000


def is_apartment(item) -> bool:
    """Проверяет, является ли объект квартирой."""
    return item.__class__.__name__ == 'Apartment'


# ========== 1 фабрика функций ==========

def make_price_filter(max_price: float):
    """Создаёт функцию-фильтр по максимальной цене.
    
    Args:
        max_price: максимальная цена
        
    Returns:
        Функция-фильтр
    """
    def filter_fn(item) -> bool:
        return item.price <= max_price
    return filter_fn


# ========== 2 callable-объекта (паттерн Стратегия) ==========

class DiscountStrategy:
    """Стратегия применения скидки к объекту недвижимости."""
    
    def __init__(self, discount_percent: float = 0.1):
        """Инициализация стратегии скидки.
        
        Args:
            discount_percent: процент скидки (0.0 до 1.0)
        """
        self.discount_percent = discount_percent
    
    def __call__(self, item):
        """Применяет скидку к объекту."""
        item.price *= (1 - self.discount_percent)
        return item


class StatusUpdateStrategy:
    """Стратегия обновления статуса объекта."""
    
    def __init__(self, new_status: str = "Доступен"):
        """Инициализация стратегии обновления статуса.
        
        Args:
            new_status: новый статус объекта
        """
        self.new_status = new_status
    
    def __call__(self, item):
        """Обновляет статус объекта."""
        if hasattr(item, 'status'):
            item.status = self.new_status
        return item