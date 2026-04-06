"""
Демонстрация работы коллекции квартир
"""
from model import Apartment
from collection import Apartment_collection


def main():

    print('СЦЕНАРИЙ 1:')
    #Создание квартир
    print("Создание квартир")
    apt1 = Apartment("ул. Ленина, 10", 45.5, 2, 5000000, 3, 2015)
    apt2 = Apartment("ул. Пушкина, 5", 75.0, 3, 8500000, 5, 2018)
    apt3 = Apartment("пр. Мира, 20", 120.0, 4, 15000000, 7, 2020)
    apt4 = Apartment("ул. Гагарина, 8", 35.0, 1, 3200000, 2, 2010)
    apt5 = Apartment("ул. Советская, 15", 60.0, 2, 6200000, 4, 2016)
    apt6 = Apartment("ул. Лермонтова, 3", 90.0, 3, 9500000, 6, 2019)
    
    print("Созданы квартиры:")
    print(f"  1. {apt1.address}, {apt1.price:.0f}р, {apt1.rooms} комн.")
    print(f"  2. {apt2.address}, {apt2.price:.0f}р, {apt2.rooms} комн.")
    print(f"  3. {apt3.address}, {apt3.price:.0f}р, {apt3.rooms} комн.")
    print(f"  4. {apt4.address}, {apt4.price:.0f}р, {apt4.rooms} комн.")
    print(f"  5. {apt5.address}, {apt5.price:.0f}р, {apt5.rooms} комн.")
    print(f"  6. {apt6.address}, {apt6.price:.0f}р, {apt6.rooms} комн.")
    
    #Добавление в коллекцию
    print("Добавлены в коллекцию:")

    collection = Apartment_collection()
    collection.add(apt1)
    collection.add(apt2)
    collection.add(apt3)
    collection.add(apt4)
    collection.add(apt5)
    collection.add(apt6)
    
    #Вывод всех элементов(квартир)
    print("Все квартиры:")
    for i, apt in enumerate(collection.get_all(), 1):
        print(f"  {i}. {apt.address} | {apt.rooms} комн. | {apt.area}м2 | {apt.price:.0f}р | {apt.status}")
    
    #Длина коллекции
    print(f"Длина коллекции: {len(collection)}")
    
    #Итерация по коллекции:
    print("Итерация по коллекции:")
    for apt in collection:
        print(f"  - {apt.address}, {apt.price:.0f}р.")
    
    #Элементы по индексам
    print("Вывод элементов по индексам:")
    print(f"  Элемент с индексом 0: {collection[0].address}")
    print(f"  Элемент с индексом 2: {collection[2].address}")
    print(f"  Элемент с индексом -1: {collection[-1].address}")
    
    #Проверка защиты от дубликатов
    print("Проверка защиты от дубликатов:")
    try:
        apt_duplicate = Apartment("ул. Ленина, 10", 45.5, 2, 5000000, 3, 2015)
        collection.add(apt_duplicate)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    #Проверка типа объекта
    print("Проверка типа объекта:")
    try:
        collection.add("это строка")
    except TypeError as e:
        print(f"Ошибка: {e}")

    print('СЦЕНАРИЙ 2:')
    # Поиск по адресу
    found = collection.find_by_address("ул. Пушкина, 5")
    print(f"  Поиск по адресу 'ул. Пушкина, 5': {found.address if found else 'не найдено'}")
    
    # Поиск по диапазону цен
    price_range = collection.find_by_price_range(4000000, 7000000)
    print(f"  Квартиры в диапазоне 4-7 млн: {len(price_range)} шт.")
    for apt in price_range:
        print(f"    - {apt.address}: {apt.price:.0f}р.")
    
    # Поиск по количеству комнат
    rooms_2 = collection.find_by_rooms(2)
    print(f"  Квартиры с 2 комнатами: {len(rooms_2)} шт.")
    for apt in rooms_2:
        print(f"    - {apt.address}")
    
    # Поиск доступных
    available = collection.find_available()
    print(f"  Доступных квартир: {len(available)} шт.")

    #Удаление
    print("Удаление")
    
    # Удаление по объекту
    print("\n  Удаление по объекту (remove):")
    collection.remove(apt3)
    print(f"    После удаления квартиры '{apt3.address}' осталось: {len(collection)}")
    
    # Удаление по индексу
    print("\n  Удаление по индексу (remove_at):")
    collection.remove_at(2)
    print(f"    После удаления осталось: {len(collection)}")
    
    #Проверка get_all
    print("Вывод всех квартир:")
    all_apartments = collection.get_all()
    for i, apt in enumerate(all_apartments, 1):
        print(f"  {i}. {apt.address}")

    print('СЦЕНАРИЙ 3:')
    # Сортировка по цене (возрастание)
    print("\n  Сортировка по цене (возрастание):")
    sorted_by_price = collection.sort_by_price()
    for i, apt in enumerate(sorted_by_price, 1):
        print(f"    {i}. {apt.address}: {apt.price:.0f}р.")
    
    # Сортировка по цене (убывание)
    print("\n  Сортировка по цене (убывание):")
    sorted_by_price_desc = collection.sort_by_price(reverse=True)
    for i, apt in enumerate(sorted_by_price_desc, 1):
        print(f"    {i}. {apt.address}: {apt.price:.0f}р.")
    
    # Сортировка по площади
    print("\n  Сортировка по площади (возрастание):")
    sorted_by_area = collection.sort_by_area()
    for i, apt in enumerate(sorted_by_area, 1):
        print(f"    {i}. {apt.address}: {apt.area}м2")
    
    # Сортировка по комнатам
    print("\n  Сортировка по комнатам (от 1 до 4):")
    sorted_by_rooms = collection.sort_by_rooms()
    for i, apt in enumerate(sorted_by_rooms, 1):
        print(f"    {i}. {apt.address}: {apt.rooms} комн.")
    
    #Фильтрация
    print("Фильтрация:")
    # Доступные квартиры
    available_filtered = collection.get_available()
    print(f"\n  Доступные квартиры ({len(available_filtered)} шт.):")
    for apt in available_filtered:
        print(f"    - {apt.address}")
    
    # Дорогие квартиры (> 10 млн)
    expensive = collection.get_expensive(10000000)
    print(f"\n  Дорогие квартиры (> 10 млн) ({len(expensive)} шт.):")
    for apt in expensive:
        print(f"    - {apt.address}: {apt.price:.0f}р.")
    
    # Дорогие квартиры с другим порогом (7 млн)
    expensive2 = collection.get_expensive(7000000)
    print(f"\n  Дорогие квартиры (> 7 млн) ({len(expensive2)} шт.):")
    for apt in expensive2:
        print(f"    - {apt.address}: {apt.price:.0f}р.")
    
    # Дешёвые квартиры (порог 5 млн)
    cheap = collection.get_cheap(5000000)
    print(f"\n  Дешёвые квартиры (< 5 млн) ({len(cheap)} шт.):")
    for apt in cheap:
        print(f"    - {apt.address}: {apt.price:.0f}р.")

if __name__ == "__main__":
    main()