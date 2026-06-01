"""CLI-интерфейс приложения."""
import sys
import os
from typing import List, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab07.app import App
from lab03.models import NewBuilding, SecondaryProperty
from lab04.models import House
from lab07.exceptions import ItemNotFoundError, DuplicateItemError


class CLI:
    """Консольный интерфейс."""
    
    def __init__(self, app: App) -> None:
        self.app = app
    
    def run(self) -> None:
        while True:
            self._show_menu()
            choice = self._input_int("Выберите пункт: ")
            
            try:
                if choice == 0:
                    print("До свидания!")
                    break
                elif choice == 1:
                    self._add_property()
                elif choice == 2:
                    self._show_all()
                elif choice == 3:
                    self._find_by_address()
                elif choice == 4:
                    self._filter_menu()
                elif choice == 5:
                    self._remove_property()
                elif choice == 6:
                    self._sort_menu()
                elif choice == 7:
                    self._show_stats()
                else:
                    print("Ошибка: неверный пункт меню")
            except DuplicateItemError as e:
                print(f"Ошибка: {e}")
            except ItemNotFoundError as e:
                print(f"Ошибка: {e}")
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
    
    def _show_menu(self) -> None:
        print("  УПРАВЛЕНИЕ НЕДВИЖИМОСТЬЮ")
        print("1. Добавить объект")
        print("2. Показать все объекты")
        print("3. Найти по адресу")
        print("4. Фильтровать")
        print("5. Удалить объект")
        print("6. Сортировать")
        print("7. Статистика")
        print("0. Выход")
    
    def _input_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Ошибка: введите целое число")
    
    def _input_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Ошибка: введите число")
    
    def _print_item(self, item: Any, index: int = -1) -> None:
        idx_str = f"[{index}] " if index >= 0 else ""
        
        if isinstance(item, NewBuilding):
            parking = "есть" if item.has_underground_parking else "нет"
            print(f"  {idx_str}Новостройка | {item.address}")
            print(f"     {item.area:.0f}м2 | {item.rooms} комн. | {item.floor} этаж")
            print(f"     {item.price:.0f}руб. | {item.developer} | Сдача: {item.completion_date}")
            print(f"     Отделка: {item.finishing_type} | Паркинг: {parking}")
        elif isinstance(item, SecondaryProperty):
            debts = "есть" if item.has_debts else "нет"
            print(f"  {idx_str}Вторичка | {item.address}")
            print(f"     {item.area:.0f}м2 | {item.rooms} комн. | {item.floor} этаж")
            print(f"     {item.price:.0f}руб. | Состояние: {item.condition} | Долги: {debts}")
        elif isinstance(item, House):
            garage = "есть" if item.has_garage else "нет"
            print(f"  {idx_str}Дом | {item.address}")
            print(f"     {item.area:.0f}м2 | Участок: {item.land_area:.1f}сот. | {item.floors} этаж.")
            print(f"     {item.price:.0f}руб. | Гараж: {garage}")
        else:
            print(f"  {idx_str}Квартира | {item.address}")
            print(f"     {item.area:.0f}м2 | {item.rooms} комн. | {item.floor} этаж")
            print(f"     {item.price:.0f}руб. | Год: {item.construction_year}")
    
    def _print_list(self, items: List[Any]) -> None:
        if not items:
            print("Список пуст.")
            return
        print(f"\nНайдено объектов: {len(items)}")
        for i, item in enumerate(items):
            self._print_item(item, i)
            print()
    
    def _add_property(self) -> None:
        print("\n--- ДОБАВЛЕНИЕ ОБЪЕКТА ---")
        print("1. Обычная квартира")
        print("2. Новостройка")
        print("3. Вторичное жильё")
        print("4. Дом")
        choice = self._input_int("Тип объекта: ")
        
        address = input("Адрес: ")
        area = self._input_float("Площадь (м2): ")

        rooms = self._input_int("Количество комнат: ")
        price = self._input_float("Цена (руб.): ")
        floor = self._input_int("Этаж: ")
        year = self._input_int("Год постройки: ")
        
        if choice == 1:
            item = self.app.add_apartment(address, area, rooms, price, floor, year)
        elif choice == 2:
            developer = input("Застройщик: ")
            completion = input("Дата сдачи (ГГГГ-ММ-ДД): ")
            print("Отделка: 1-без, 2-черновая, 3-чистовая, 4-дизайнерская")
            fin = self._input_int("Выбор: ")
            finishing = {1: "без отделки", 2: "черновая", 3: "чистовая", 4: "дизайнерская"}.get(fin, "черновая")
            parking = input("Подземный паркинг? (y/n): ").lower() == 'y'
            item = self.app.add_new_building(address, area, rooms, price, floor, year,
                                            developer, completion, finishing, parking)


        elif choice == 3:
            owners = self._input_int("Предыдущих владельцев: ")
            print("Состояние: 1-отличное, 2-хорошее, 3-удовл., 4-плохое")
            cond = self._input_int("Выбор: ")
            condition = {1: "отличное", 2: "хорошее", 3: "удовлетворительное", 4: "плохое"}.get(cond, "хорошее")
            debts = input("Есть долги? (y/n): ").lower() == 'y'
            item = self.app.add_secondary(address, area, rooms, price, floor, year,
                                         owners, condition, debts)
        elif choice == 4:
            land = self._input_float("Площадь участка (сот.): ")
            floors = self._input_int("Этажность: ")
            garage = input("Есть гараж? (y/n): ").lower() == 'y'
            item = self.app.add_house(address, area, land, floors, price, year, garage)
        else:
            print("Неверный тип")
            return
        
        print("\nОбъект добавлен:")
        self._print_item(item)
    
    def _show_all(self) -> None:
        self._print_list(self.app.items)
    
    def _find_by_address(self) -> None:
        query = input("\nПоиск по адресу: ")
        self._print_list(self.app.find_by_address(query))
    
    def _filter_menu(self) -> None:
        print("\n--- ФИЛЬТРАЦИЯ ---")
        print("1. По цене")
        print("2. По площади")
        print("3. По типу")
        choice = self._input_int("Критерий: ")
        
        if choice == 1:
            results = self.app.filter_by_price(
                self._input_float("Мин. цена: "),
                self._input_float("Макс. цена: ")
            )
        elif choice == 2:
            results = self.app.filter_by_area(
                self._input_float("Мин. площадь: "),
                self._input_float("Макс. площадь: ")
            )
        elif choice == 3:
            print("Типы: apartment, new_building, secondary, house")
            results = self.app.filter_by_type(input("Тип: ").lower())
        else:
            print("Неверный критерий")
            return
        
        self._print_list(results)
    
    def _remove_property(self) -> None:
        """Удалить объект с подтверждением."""
        if not self.app.items:
            print("Коллекция пуста.")
            return
        
        print("\nСписок объектов:")
        for i, item in enumerate(self.app.items):
            self._print_item(item, i)
        
        index = self._input_int("\nИндекс объекта для удаления: ")
        
        try:
            # Сначала находим объект
            if index < 0 or index >= len(self.app.items):
                raise ItemNotFoundError(f"Объект с индексом {index} не найден")
            
            item = self.app.items[index]
            
            # Показываем, что будем удалять
            print("\nВы собираетесь удалить:")
            self._print_item(item)
            
            # Запрашиваем подтверждение
            confirm = input(f'\nУдалить "{item.address}"? (y/n): ').lower()
            
            if confirm == 'y':
                self.app.remove_by_index(index)
                print(f" Объект удалён: {item.address}")
            else:
                print("Удаление отменено")
                
        except ItemNotFoundError as e:
            print(f" Ошибка: {e}")
    
    def _sort_menu(self) -> None:
        print("\n--- СОРТИРОВКА ---")
        print("1. По цене")
        print("2. По площади")
        print("3. По адресу")
        field = self._input_int("Критерий: ")
        
        print("1. По возрастанию")
        print("2. По убыванию")
        reverse = self._input_int("Выбор: ") == 2
        
        if field == 1:
            results = self.app.sort_by_price(reverse)
        elif field == 2:
            results = self.app.sort_by_area(reverse)
        elif field == 3:
            results = self.app.sort_by_address(reverse)
        else:
            print("Неверный критерий")
            return
        
        self._print_list(results)
    
    def _show_stats(self) -> None:
        stats = self.app.get_statistics()
        print("\n--- СТАТИСТИКА ---")
        print(f"Всего объектов: {stats['total']}")
        print(f"Квартир: {stats['apartments']}")
        print(f"Домов: {stats['houses']}")
        if stats['total'] > 0:
            print(f"Средняя цена: {stats['avg_price']:.0f}руб.")
            print(f"Средняя площадь: {stats['avg_area']:.1f}м2")