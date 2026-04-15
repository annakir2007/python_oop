import sys
import os
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_path)
sys.path.append(os.path.join(src_path, 'lab01'))
from lab01.model import Apartment
from models import NewBuilding, SecondaryProperty, Apartment_collection

def main():

    print('СЦЕНАРИЙ 1:')

    apartment = Apartment(
        address="ул. Ленина, д. 10, кв. 45",
        area=65.5,
        rooms=3,
        price=8500000,
        floor=5,
        construction_year=2015
    )
    
    new_building = NewBuilding(
        address="ЖК 'Солнечный', ул. Новая, д. 15, кв. 78",
        area=55.0,
        rooms=2,
        price=7200000,
        floor=12,
        construction_year=2024,
        developer="ПИК",
        completion_date="2025-06-30",
        finishing_type=NewBuilding.FINISHING_FINE,
        has_underground_parking=True
    )
    
    secondary = SecondaryProperty(
        address="ул. Старая, д. 5, кв. 12",
        area=48.0,
        rooms=2,
        price=5800000,
        floor=3,
        construction_year=1995,
        previous_owners=2,
        condition=SecondaryProperty.CONDITION_GOOD,
        has_debts=False
    )
    
    print("\nИнформация о квартире:")
    print(apartment)
    
    print("\nИнформация о новостройке:")
    print(new_building)
    
    print("\nИнформация о вторичном жилье:")
    print(secondary)
    
    print("\nНовые методы дочерних классов:")
    print(f"Новостройка: {new_building.add_mortgage_program('Сбербанк', 8.5, 20)}")
    print(f"Новостройка: {new_building.add_mortgage_program('ВТБ', 7.2, 15)}")
    
    best = new_building.get_best_mortgage()
    if best:
        print(f"Лучшая ипотека: {best['bank']} - {best['rate']}%")
    
    print(f"\nВторичка: {secondary.add_renovation(2020, 'Косметический ремонт', 200000)}")
    print(f"Вторичка: возраст дома = {secondary.get_age()} лет")
    print(f"Вторичка: скидка за состояние = {secondary.calculate_discount():,.0f} руб.")
    

    print('СЦЕНАРИЙ 2:')

    objects = [
        Apartment("ул. Пушкина, д. 5, кв. 12", 45.0, 2, 5500000, 3, 2005),
        NewBuilding("ЖК 'Зелёный', ул. Парковая, д. 8", 62.0, 3, 8900000, 7, 2024,
                   "Самолёт", "2025-03-31", NewBuilding.FINISHING_ROUGH, True),
        SecondaryProperty("ул. Советская, д. 20, кв. 5", 52.0, 2, 6200000, 4, 1985,
                         3, SecondaryProperty.CONDITION_SATISFACTORY, True),
        NewBuilding("ЖК 'Морской', ул. Приморская, д. 3", 75.0, 4, 12500000, 15, 2024,
                   "ЛСР", "2025-09-30", NewBuilding.FINISHING_DESIGNER, True),
        SecondaryProperty("ул. Цветочная, д. 7, кв. 33", 38.0, 1, 4200000, 2, 1975,
                         5, SecondaryProperty.CONDITION_BAD, False)
    ]
    
    print("\nПолиморфизм:")
    for obj in objects:
        print(f"\n{obj.__class__.__name__}:")
        print(obj)
    
    print("\n\nПроверка типов объектов:")
    for obj in objects:
        if isinstance(obj, NewBuilding):
            print(f"Новостройка: {obj.address} (застройщик: {obj.developer})")
        elif isinstance(obj, SecondaryProperty):
            print(f"Вторичка: {obj.address} (состояние: {obj.condition}, возраст: {obj.get_age()} лет)")
        elif isinstance(obj, Apartment):
            print(f"Квартира: {obj.address} (этаж: {obj.floor})")

    print('СЦЕНАРИЙ 3:')

    collection = Apartment_collection()
    
    collection.add(Apartment("ул. Мира, д. 15, кв. 7", 55.0, 2, 6200000, 4, 2010))
    collection.add(NewBuilding("ЖК 'Зелёный', ул. Парковая, д. 8", 62.0, 3, 8900000, 7, 2024,
                              "Самолёт", "2025-03-31", NewBuilding.FINISHING_ROUGH, True))
    collection.add(SecondaryProperty("ул. Советская, д. 20, кв. 5", 52.0, 2, 6200000, 4, 1985,
                                    3, SecondaryProperty.CONDITION_SATISFACTORY, True))
    collection.add(NewBuilding("ЖК 'Солнечный', ул. Новая, д. 15", 55.0, 2, 7200000, 12, 2024,
                              "ПИК", "2025-06-30", NewBuilding.FINISHING_FINE, True))
    collection.add(SecondaryProperty("ул. Цветочная, д. 7, кв. 33", 38.0, 1, 4200000, 2, 1975,
                                    5, SecondaryProperty.CONDITION_BAD, False))
    collection.add(NewBuilding("ЖК 'Морской', ул. Приморская, д. 3", 75.0, 4, 12500000, 15, 2024,
                              "ПИК", "2025-09-30", NewBuilding.FINISHING_DESIGNER, True))
    
    print(f"\nВсего объектов в коллекции: {len(collection)}")
    
    print("\nСодержимое коллекции:")
    for i, item in enumerate(collection, 1):
        print(f"{i}. {item.__class__.__name__}: {item.address}")
    
    print("\nФильтрация по типам объектов:")
    
    new_buildings = collection.get_only_new_buildings()
    print(f"Новостройки ({len(new_buildings)}):")
    for nb in new_buildings:
        print(f"  - {nb.address} (застройщик: {nb.developer})")
    
    secondary_list = collection.get_only_secondary()
    print(f"\nВторичное жильё ({len(secondary_list)}):")
    for sec in secondary_list:
        print(f"  - {sec.address} (состояние: {sec.condition})")
    
    print("\nФильтрация по застройщику 'ПИК':")
    pik_objects = collection.filter_by_developer("ПИК")
    for obj in pik_objects:
        print(f"  - {obj.address}")
    
    total_price = collection.calculate_total_price()
    print(f"\nОбщая стоимость всех объектов: {total_price:,.0f} руб.")
    
    print('СЦЕНАРИЙ 4:')

    apt = Apartment("ул. Новая, д. 3, кв. 88", 42.0, 1, 4800000, 7, 2022)
    nb = NewBuilding("ЖК 'Престиж', ул. Центральная, д. 10", 65.0, 3, 9500000, 8, 2024,
                    "ПИК", "2025-12-31", NewBuilding.FINISHING_FINE, True)
    sec = SecondaryProperty("ул. Лесная, д. 8, кв. 15", 50.0, 2, 5300000, 3, 1990,
                           2, SecondaryProperty.CONDITION_GOOD, False)
    
    biz_objects = [apt, nb, sec]
    
    print("\nРасчёт ипотеки:")
    for obj in biz_objects:
        obj_type = obj.__class__.__name__
        payment = obj.calculate_monthly_payment(20, 8.5)
        print(f"{obj_type}: {payment:,.0f} руб./мес.")
    
    print("\nБронирование объектов:")
    print(f"Квартира: {apt.reserve(3)}")
    print(f"Новостройка: {nb.reserve(7)}")
    print(f"Вторичка: {sec.reserve(5)}")
    
    print("\nСпецифичные операции:")
    print(f"Новостройка: {nb.add_mortgage_program('Сбер', 7.5, 15)}")
    print(f"Новостройка: стоимость отделки = {nb.calculate_finishing_cost():,.0f} руб.")
    print(f"Вторичка: {sec.add_renovation(2023, 'Замена труб', 150000)}")
    print(f"Вторичка: скидка = {sec.calculate_discount():,.0f} руб.")
    
    print(f"\nПродажа: {apt.sell()}")
    
    print('СЦЕНАРИЙ 5:')

    mixed_objects = [
        Apartment("ул. Садовая, д. 7, кв. 23", 58.0, 2, 7100000, 5, 2012),
        NewBuilding("ЖК 'Дубки', ул. Лесная, д. 9", 70.0, 3, 10500000, 10, 2024,
                   "Самолёт", "2025-08-31", NewBuilding.FINISHING_FINE, False),
        SecondaryProperty("ул. Центральная, д. 15, кв. 7", 45.0, 2, 4900000, 2, 1980,
                         1, SecondaryProperty.CONDITION_EXCELLENT, False),
        NewBuilding("ЖК 'Речной', ул. Набережная, д. 4", 80.0, 4, 14200000, 20, 2024,
                   "ПИК", "2025-04-30", NewBuilding.FINISHING_DESIGNER, True),
        SecondaryProperty("пр. Победы, д. 77, кв. 12", 60.0, 3, 6800000, 5, 2000,
                         2, SecondaryProperty.CONDITION_GOOD, True)
    ]
    
    print("\nЕдиный интерфейс:")
    
    for obj in mixed_objects:
        print(f"\n{obj.__class__.__name__}:")
        print(obj)
    
    print("\nЕдиный интерфейс calculate_monthly_payment() для всех типов:")
    print(f"{'Тип объекта':<20} {'Адрес':<35} {'Платёж':>12}")
    
    for obj in mixed_objects:
        obj_type = obj.__class__.__name__
        address_short = obj.address[:32] + "..." if len(obj.address) > 35 else obj.address
        payment = obj.calculate_monthly_payment(20, 8.5)
        print(f"{obj_type:<20} {address_short:<35} {payment:>12,.0f} руб.")

if __name__ == "__main__":
    main()