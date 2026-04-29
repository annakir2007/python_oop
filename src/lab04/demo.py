"""
Модуль demo.py
Демонстрация работы интерфейсов и коллекции.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab04'))

from interfaces import Printable, Comparable
from models import Apartment, House, PropertyCollection


def print_all_items(items: list):
    for item in items:
        print(item.to_string())
        print("-" * 30)


def demo_collection():
    print("СЦЕНАРИЙ 1: Коллекция и фильтрация по интерфейсам")

    collection = PropertyCollection()

    collection.add(Apartment("ул. Ленина, д. 10, кв. 45", 65.0, 3, 8500000, floor=5, construction_year=2015))
    collection.add(Apartment("ул. Пушкина, д. 22, кв. 8", 42.0, 1, 5200000, floor=2, construction_year=2008))
    collection.add(Apartment("пр. Мира, д. 15, кв. 120", 85.0, 4, 12000000, floor=12, construction_year=2020))
    collection.add(House("ул. Садовая, д. 30", 120.0, 8.0, 2, 15000000, construction_year=2010, has_garage=True))
    collection.add(House("ул. Лесная, д. 5", 200.0, 12.0, 3, 25000000, construction_year=2018, has_garage=True))
    collection.add(House("ул. Полевая, д. 18", 90.0, 6.0, 1, 9500000, construction_year=2005, has_garage=False))

    print(f"\nВсего объектов в коллекции: {len(collection)}")
    print(f"Объектов с интерфейсом Printable: {len(collection.get_printable())}")
    print(f"Объектов с интерфейсом Comparable: {len(collection.get_comparable())}")

    print("\nВывод всех объектов через Printable:")
    print("-" * 50)
    collection.print_all()

    print("Сортировка через Comparable:")
    collection.sort_by_comparison()
    print("\nПосле сортировки:")
    print("-" * 50)
    for item in collection.get_all():
        if isinstance(item, Apartment):
            price_per_sqm = item.price / item.area
            print(f"[Квартира] {item.address}: {price_per_sqm:,.0f} руб./кв.м")
        elif isinstance(item, House):
            total = item.price + item.land_area * 50000
            print(f"[Дом]      {item.address}: {total:,.0f} руб. (общая стоимость)")


def demo_polymorphism():
    print("СЦЕНАРИЙ 2: Полиморфизм и проверка isinstance")

    apt1 = Apartment("ул. Ленина, д. 10, кв. 45", 65.0, 3, 8500000, floor=5)
    apt2 = Apartment("ул. Пушкина, д. 22, кв. 8", 42.0, 1, 5200000, floor=2)
    house = House("ул. Садовая, д. 30", 120.0, 8.0, 2, 15000000)

    objects = [apt1, apt2, house]

    print("Проверка реализации интерфейсов через isinstance:")
    print("-" * 40)
    for obj in objects:
        obj_type = "Квартира" if isinstance(obj, Apartment) else "Дом"
        print(f"{obj_type} ({obj.address}):")
        print(f"  Printable:  {isinstance(obj, Printable)}")
        print(f"  Comparable: {isinstance(obj, Comparable)}")
        print()

    print("Полиморфный вызов to_string() (разная реализация):")
    print("-" * 40)
    for obj in objects:
        print(obj.to_string())
        print("-" * 30)

    print("\nСравнение квартир через compare_to():")
    result = apt1.compare_to(apt2)
    if result < 0:
        print(f"  {apt1.address} дешевле за кв.м, чем {apt2.address}")
    elif result > 0:
        print(f"  {apt1.address} дороже за кв.м, чем {apt2.address}")
    else:
        print("  Одинаковая цена за кв.м")


def demo_architecture():
    print("СЦЕНАРИЙ 3: Архитектурное поведение (сортировка и вывод)")

    items = [
        House("ул. Лесная, д. 5", 200.0, 12.0, 3, 25000000, construction_year=2018),
        Apartment("ул. Пушкина, д. 22, кв. 8", 42.0, 1, 5200000, floor=2),
        Apartment("пр. Мира, д. 15, кв. 120", 85.0, 4, 12000000, floor=12),
        House("ул. Полевая, д. 18", 90.0, 6.0, 1, 9500000),
        Apartment("ул. Ленина, д. 10, кв. 45", 65.0, 3, 8500000, floor=5),
    ]

    collection = PropertyCollection()
    for item in items:
        collection.add(item)

    print("До сортировки:")
    print("-" * 40)
    for item in collection.get_printable():
        print(item.to_string())
        print("-" * 30)

    collection.sort_by_comparison()

    print("\nПосле сортировки через Comparable:")
    print("-" * 40)
    for item in collection.get_all():
        if isinstance(item, Apartment):
            print(f"[Квартира] {item.address}: {item.price/item.area:,.0f} руб./кв.м")
        elif isinstance(item, House):
            print(f"[Дом]      {item.address}: {item.price + item.land_area*50000:,.0f} руб. (общая)")

    print("\nУниверсальная функция print_all_items (через Printable):")
    print("-" * 40)
    print_all_items(collection.get_printable())


def main():

    demo_collection()
    demo_polymorphism()
    demo_architecture()


if __name__ == "__main__":
    main()