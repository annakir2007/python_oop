"""
Демонстрация работы Generic-коллекции TypedCollection и протоколов.
"""

import sys
import os
from pathlib import Path

# Добавляем пути
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(src_dir / 'lab01'))
sys.path.insert(0, str(src_dir / 'lab02'))
sys.path.insert(0, str(src_dir / 'lab03'))

lab01_model_path = src_dir / 'lab01' / 'model.py'

with open(lab01_model_path, 'r', encoding='utf-8') as f:
    model_code = f.read()

from container import TypedCollection, Displayable, Scorable, D, S

from lab01.model import Apartment
from lab03.models import NewBuilding, SecondaryProperty


#Добавляем методы display() и score() в классы

def apartment_display(self) -> str:
    """Метод display для Apartment."""
    return (f"Квартира: {self.address}, "
            f"площадь: {self.area:.1f} м2, "
            f"цена: {self.price:.0f} руб.")


def apartment_score(self) -> float:
    """Метод score для Apartment - оценка качества (цена за м2)."""
    return self.price / self.area if self.area > 0 else float('inf')


Apartment.display = apartment_display
Apartment.score = apartment_score


def newbuilding_display(self) -> str:
    """Улучшенный display для новостроек."""
    parking = "есть" if self.has_underground_parking else "нет"
    return (f"НОВОСТРОЙКА: {self.address}\n"
            f"  Застройщик: {self.developer}\n"
            f"  Отделка: {self.finishing_type}\n"
            f"  Подземный паркинг: {parking}\n"
            f"  Площадь: {self.area:.1f} м2, цена: {self.price:,.0f} руб.")


def newbuilding_score(self) -> float:
    """Оценка новостройки: цена за м2 с учётом отделки."""
    base_price = self.price + self.calculate_finishing_cost()
    if self.has_underground_parking:
        base_price += 800000
    return base_price / self.area if self.area > 0 else float('inf')


NewBuilding.display = newbuilding_display
NewBuilding.score = newbuilding_score


def secondary_display(self) -> str:
    """Улучшенный display для вторичного жилья."""
    age = self.get_age()
    discount = self.calculate_discount()
    return (f"ВТОРИЧНОЕ ЖИЛЬЁ: {self.address}\n"
            f"  Возраст: {age} лет\n"
            f"  Состояние: {self.condition}\n"
            f"  Площадь: {self.area:.1f} м2\n"
            f"  Цена: {self.price:,.0f} руб.\n"
            f"  Скидка за состояние: {discount:,.0f} руб.")


def secondary_score(self) -> float:
    """Оценка вторички: цена с учётом скидки за м2."""
    effective_price = self.price - self.calculate_discount()
    return effective_price / self.area if self.area > 0 else float('inf')


SecondaryProperty.display = secondary_display
SecondaryProperty.score = secondary_score


def demo_task3() -> None:
    """Типизированная коллекция."""
    
    apartments: TypedCollection[Apartment] = TypedCollection()
    
    apt1 = Apartment("ул. Ленина, 10", 55.5, 2, 4500000, floor=3)
    apt2 = Apartment("ул. Пушкина, 25", 78.0, 3, 7500000, floor=5)
    apt3 = Apartment("пр. Мира, 100", 42.0, 1, 3200000, floor=2)
    
    print("Добавление объектов в коллекцию:")
    apartments.add(apt1)
    print(f" Добавлена: {apt1.address}")
    apartments.add(apt2)
    print(f" Добавлена: {apt2.address}")
    apartments.add(apt3)
    print(f" Добавлена: {apt3.address}")
    
    print(f"\nВсего объектов в коллекции: {len(apartments)}")
    
    print("\nСодержимое коллекции:")
    for i, apt in enumerate(apartments.get_all(), 1):
        print(f"\n  Объект №{i}:")
        print(f"    Адрес: {apt.address}")
        print(f"    Площадь: {apt.area:.1f} м2")
        print(f"    Комнат: {apt.rooms}")
        print(f"    Цена: {apt.price:.0f} руб.")
        print(f"    Год постройки: {apt.construction_year}")

def demo_task4() -> None:
    """Методы find, filter, map."""
    
    collection: TypedCollection[Apartment] = TypedCollection()
    
    collection.add(Apartment("ул. Ленина, 10", 55.5, 2, 4500000, floor=3))
    collection.add(Apartment("ул. Пушкина, 25", 78.0, 3, 7500000, floor=5))
    collection.add(Apartment("пр. Мира, 100", 42.0, 1, 3200000, floor=2))
    collection.add(Apartment("ул. Садовая, 50", 65.0, 2, 12000000, floor=8))
    collection.add(Apartment("ул. Цветочная, 15", 90.0, 4, 15000000, floor=12))
    
    print("Коллекция содержит 5 объектов:\n")
    for i, apt in enumerate(collection, 1):
        print(f"  {i}. {apt.address} - {apt.area:.1f} м2, {apt.rooms} комн., "
              f"{apt.price:.0f} руб.")
    
    # find()
    print("Поиск дорогой квартиры (цена > 10 млн):")
    found = collection.find(lambda apt: apt.price > 10_000_000)
    if found:
        print(f" Найдена: {found.address}, цена: {found.price:.0f} руб.")
    else:
        print("  Ничего не найдено")
    
    print("\nПоиск квартиры с площадью > 100 м2:")
    not_found = collection.find(lambda apt: apt.area > 100)
    if not_found:
        print(f"  Найдена: {not_found.address}")
    else:
        print("  Ничего не найдено")
    
    # filter()
    print("Фильтрация: квартиры с ценой от 5 до 10 млн:")
    filtered = collection.filter(lambda apt: 5_000_000 <= apt.price <= 10_000_000)
    if filtered:
        for apt in filtered:
            print(f"  - {apt.address} - {apt.price:.0f} руб.")
    else:
        print("  Нет подходящих объектов")
    
    print("\nФильтрация: 2-комнатные квартиры:")
    two_rooms = collection.filter(lambda apt: apt.rooms == 2)
    for apt in two_rooms:
        print(f"  * {apt.address} - {apt.rooms} комн., {apt.price:.0f} руб.")
    
    # map()
    addresses: list[str] = collection.map(lambda apt: apt.address)
    for i, addr in enumerate(addresses, 1):
        print(f"  {i}. {addr}")
    print(f"  Тип результата: {type(addresses).__name__}[{type(addresses[0]).__name__}]")
    
    print("\nmap() -> цены (list[float]):")
    prices: list[float] = collection.map(lambda apt: apt.price)
    for i, price in enumerate(prices, 1):
        print(f"  {i}. {price:.0f} руб.")
    print(f"  Тип результата: {type(prices).__name__}[{type(prices[0]).__name__}]")
    
    print("\nmap() -> площади (list[float]):")
    areas: list[float] = collection.map(lambda apt: apt.area)
    for i, area in enumerate(areas, 1):
        print(f"  {i}. {area} м2")
    print(f"  Тип результата: {type(areas).__name__}[{type(areas[0]).__name__}]")


def demo_task5() -> None:
    """Протоколы Displayable и Scorable."""
    
    apt = Apartment("проверочная", 50.0, 2, 5000000)
    print(f"Apartment имеет display(): {hasattr(apt, 'display')}")
    print(f"Apartment имеет score(): {hasattr(apt, 'score')}")
    print()
    
    # Сценарий 1: Displayable
    print('Сценарий 1:')
    displayable_collection: TypedCollection[D] = TypedCollection()
    
    new_building = NewBuilding(
        address="ЖК 'Солнечный', ул. Новая, 1",
        area=65.0, rooms=3, price=8500000, floor=7,
        construction_year=2024, developer="СтройИнвест",
        completion_date="2025-06", finishing_type="чистовая",
        has_underground_parking=True
    )
    
    secondary = SecondaryProperty(
        address="ул. Старая, 30",
        area=55.0, rooms=2, price=4200000, floor=2,
        construction_year=1995, previous_owners=2,
        condition="хорошее", has_debts=False
    )
    
    simple_apartment = Apartment(
        address="ул. Центральная, 15",
        area=48.0, rooms=2, price=3800000, floor=4
    )
    
    print("Добавление объектов разных типов:")
    displayable_collection.add(new_building)
    print(f"  Добавлена новостройка: {new_building.address}")
    displayable_collection.add(secondary)
    print(f"  Добавлено вторичное жильё: {secondary.address}")
    displayable_collection.add(simple_apartment)
    print(f"  Добавлена квартира: {simple_apartment.address}")
    
    print(f"\nВсего объектов: {len(displayable_collection)}")
    print("\nВызов display() для каждого объекта:\n")
    for i, item in enumerate(displayable_collection, 1):
        print(f"  Объект №{i}:")
        print(f"  {item.display()}")
        print()
    
    # Сценарий 2: Scorable
    print("Сценарий 2: TypedCollection[Scorable]")
    
    scorable_collection: TypedCollection[S] = TypedCollection()
    
    n1 = NewBuilding(
        address="ЖК 'Элитный', ул. Престижная, 5",
        area=120.0, rooms=5, price=25000000, floor=15,
        construction_year=2025, developer="ПрестижСтрой",
        completion_date="2026-01", finishing_type="дизайнерская",
        has_underground_parking=True
    )
    
    s1 = SecondaryProperty(
        address="ул. Ветхая, 1",
        area=40.0, rooms=1, price=1500000, floor=1,
        construction_year=1960, previous_owners=5,
        condition="плохое", has_debts=True
    )
    
    a1 = Apartment(
        address="ул. Средняя, 20",
        area=70.0, rooms=3, price=5500000, floor=6
    )
    
    print("Добавление объектов в Scorable-коллекцию:")
    scorable_collection.add(n1)
    print(f"  Элитная новостройка: {n1.address}")
    scorable_collection.add(s1)
    print(f"  Ветхое вторичное жильё: {s1.address}")
    scorable_collection.add(a1)
    print(f"  Обычная квартира: {a1.address}")
    
    print("\nРейтинг объектов по цене за м2):")
    for i, item in enumerate(scorable_collection, 1):
        s = item.score()
        print(f"  {i}. {item.address}")
        print(f"     Цена: {s:.0f} руб./м2")
        if s < 100_000:
            category = "Эконом"
        elif s < 200_000:
            category = "Комфорт"
        else:
            category = "Премиум"
        print(f"     Категория: {category}")
    
    print("\nmap() -> список score (list[float]):")
    scores: list[float] = scorable_collection.map(lambda item: item.score())
    for i, s in enumerate(scores, 1):
        print(f"  {i}. {s:.0f} руб./м2")

def main() -> None:

    
    try:
        demo_task3()
        demo_task4()
        demo_task5()
    except Exception as e:
        print(f"\nОшибка {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()