"""
Демонстрация работы с функциями-стратегиями.
3 сценария для оценки 5.
"""

from strategies import (
    by_price, by_area, by_price_per_square_meter,
    is_expensive, is_apartment,
    make_price_filter,
    DiscountStrategy, StatusUpdateStrategy
)
from collection import ApartmentCollection


# Заглушки классов недвижимости
class Apartment:
    """Квартира."""
    def __init__(self, address, price, area, rooms):
        self.address = address
        self.price = price
        self.area = area
        self.rooms = rooms
        self.status = "Доступен"
    
    def __repr__(self):
        return f"Квартира({self.address}, {self.price}р, {self.area}м2, {self.rooms}к.)"


class House:
    """Дом."""
    def __init__(self, address, price, area, rooms):
        self.address = address
        self.price = price
        self.area = area
        self.rooms = rooms
        self.status = "Доступен"
    
    def __repr__(self):
        return f"Дом({self.address}, {self.price}р, {self.area}м2, {self.rooms}к.)"


def print_items(collection, title=""):
    """Вывод коллекции."""
    if title:
        print(f"\n{title}")
        print("-" * 50)
    for item in collection:
        print(f"  {item.address}: {item.price:,}р, {item.area}м2, "
              f"{item.rooms}к., статус: {item.status}")


def scenario_1():
    """Сценарий 1: цепочка filter → sort → apply."""
    print("СЦЕНАРИЙ 1: Цепочка filter → sort → apply")
    
    # Создаём коллекцию
    collection = ApartmentCollection([
        Apartment("Москва, Тверская, 15", 15_000_000, 75, 3),
        Apartment("Москва, Арбат, 22", 8_500_000, 45, 1),
        House("Москва, Рублёвка, 10", 45_000_000, 250, 5),
        Apartment("Москва, Ленина, 100", 6_500_000, 55, 2),
        House("Москва, Жуковка, 5", 25_000_000, 180, 4),
    ])
    
    print_items(collection, "Исходная коллекция:")
    
    # Шаг 1: filter_by
    print("Шаг 1: filter_by (цена <= 20 млн)")
    cheap = collection.filter_by(make_price_filter(20_000_000))
    print_items(cheap, "После фильтрации:")
    
    # Шаг 2: sort_by
    print("Шаг 2: sort_by (по площади)")
    sorted_cheap = cheap.sort_by(by_area)
    print_items(sorted_cheap, "После сортировки:")
    
    # Шаг 3: apply
    print("Шаг 3: apply (скидка 10%)")
    discount = DiscountStrategy(0.10)
    result = sorted_cheap.apply(discount)
    print_items(result, "После скидки:")
    
    # Цепочка в одну строку
    print("Цепочка в одну строку:")
    chain = (collection
        .filter_by(is_expensive)
        .sort_by(by_price)
        .apply(DiscountStrategy(0.05)))
    print_items(chain, "Дорогие → сортировка по цене → скидка 5%:")


def scenario_2():
    """Сценарий 2: замена стратегии без изменения кода."""
    print("СЦЕНАРИЙ 2: Замена стратегий")
    
    collection = ApartmentCollection([
        Apartment("Москва, Тверская, 15", 15_000_000, 75, 3),
        Apartment("Москва, Арбат, 22", 8_500_000, 45, 1),
        House("Москва, Рублёвка, 10", 45_000_000, 250, 5),
    ])
    
    print_items(collection, "Исходная коллекция:")
    
    # Одна коллекция — разные стратегии сортировки
    strategies = [
        ("По цене", by_price),
        ("По площади", by_area),
        ("По цене за м2", by_price_per_square_meter),
    ]
    
    for name, strategy in strategies:
        sorted_col = collection.sort_by(strategy)
        print(f"\nСтратегия: {name}")
        for item in sorted_col:
            print(f"  {item.address}: {item.price:,}₽, {item.area}м²")
    
    # Одна коллекция — разные фильтры
    filters = [
        ("Дорогие (> 10 млн)", is_expensive),
        ("Только квартиры", is_apartment),
        ("Цена <= 15 млн", make_price_filter(15_000_000)),
    ]
    
    for name, filter_func in filters:
        filtered = collection.filter_by(filter_func)
        print(f"\nФильтр: {name} (найдено: {len(filtered)})")
        for item in filtered:
            print(f"  {item.address}: {item.price:,}₽")


def scenario_3():
    """Сценарий 3: callable-объекты как стратегии."""
    print("СЦЕНАРИЙ 3: Callable-объекты")
    
    collection = ApartmentCollection([
        Apartment("Москва, Тверская, 15", 15_000_000, 75, 3),
        Apartment("Москва, Арбат, 22", 8_500_000, 45, 1),
        House("Москва, Рублёвка, 10", 45_000_000, 250, 5),
    ])
    
    print_items(collection, "Исходная коллекция:")
    
    # Демонстрация DiscountStrategy (callable-объект)
    print("\n1. DiscountStrategy (скидка 15%):")
    discount = DiscountStrategy(0.15)
    discounted = collection.clone().apply(discount)
    for orig, new in zip(collection, discounted):
        print(f"  {orig.address}: {orig.price:,}р → {new.price:,}р")
    
    # Демонстрация StatusUpdateStrategy (callable-объект)
    print("\n2. StatusUpdateStrategy (статус 'VIP'):")
    vip_status = StatusUpdateStrategy("VIP")
    vip_collection = collection.clone().apply(vip_status)
    print_items(vip_collection, "Со статусом VIP:")
    
    # map + lambda vs именованная функция
    print("\n3. map + lambda vs функция:")
    # Через lambda
    prices_lambda = list(map(lambda x: x.price, collection))
    # Именованная функция
    def get_price(item):
        return item.price
    prices_func = list(map(get_price, collection))
    
    print(f"  Lambda: {prices_lambda}")
    print(f"  Функция: {prices_func}")
    print(f"  Результаты равны: {prices_lambda == prices_func}")


if __name__ == "__main__":
    scenario_1()
    scenario_2()
    scenario_3()