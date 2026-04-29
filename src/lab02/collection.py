"""
Коллекция квартир для управления объектами Apartment
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lab01.model import Apartment

class Apartment_collection:
    """Коллекция квартир"""

    def __init__(self):
        """Инициализация пустой коллекции"""
        self._items = []  #список квартир
    
    def add(self, item):
        """Добавить квартиру в коллекцию"""
        if not isinstance(item, Apartment):
            raise TypeError(f"Можно добавлять только объекты Apartment, получен {type(item).__name__}")
        
        # Проверка на дубликат
        if item in self._items:
            raise ValueError(f"Такая квартира уже добавлена: {item.address}")
        
        self._items.append(item)
        print(f"Добавлена квартира: {item.address}")
    
    def remove(self, item):
        """Удалить квартиру из коллекции"""
        if item in self._items:
            self._items.remove(item)
            print(f"Удалена квартира: {item.address}")
            return True
        print(f"Квартира не найдена: {item.address}")
        return False
    
    def get_all(self):
        """Получить список всех квартир"""
        return self._items.copy()
    
    def find_by_address(self, address):
        """Найти квартиру по адресу"""
        for item in self._items:
            if item.address == address:
                return item
        return None
    
    def find_by_price_range(self, min_price, max_price):
        """Найти квартиры в ценовом диапазоне"""
        result = []
        for item in self._items:
            if min_price <= item.price <= max_price:
                result.append(item)
        return result
    
    def find_by_rooms(self, rooms):
        """Найти квартиры по количеству комнат"""
        result = []
        for item in self._items:
            if item.rooms == rooms:
                result.append(item)
        return result
    
    def find_available(self):
        """Найти доступные квартиры"""
        result = []
        for item in self._items:
            if item.is_available:
                result.append(item)
        return result
    
    def __len__(self):
        """Возвращает количество квартир"""
        return len(self._items)
    
    def __iter__(self):
        """Позволяет итерироваться по коллекции"""
        return iter(self._items)
    
    def __getitem__(self, index):
        """Поддержка индексации collection[index]"""
        return self._items[index]
    
    def remove_at(self, index):
        """Удалить квартиру по индексу"""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        
        removed = self._items.pop(index)
        print(f"Удалена квартира с индексом {index}: {removed.address}")
        return removed
    
    def sort_by_price(self, reverse=False):
        """Сортировка по цене"""

        sorted_items = []
        for item in self._items:
            sorted_items.append(item)
        
        #сортировка
        n = len(sorted_items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if reverse:
                    # По убыванию
                    if sorted_items[j].price < sorted_items[j + 1].price:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
                else:
                    # По возрастанию
                    if sorted_items[j].price > sorted_items[j + 1].price:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
        
        new_collection = Apartment_collection()
        new_collection._items = sorted_items
        
        return new_collection

    def sort_by_area(self, reverse=False):
        """Сортировка по площади"""

        sorted_items = []
        for item in self._items:
            sorted_items.append(item)
        
        #сортировка
        n = len(sorted_items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if reverse:
                    # По убыванию
                    if sorted_items[j].area < sorted_items[j + 1].area:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
                else:
                    # По возрастанию
                    if sorted_items[j].area > sorted_items[j + 1].area:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
        
        new_collection = Apartment_collection()
        new_collection._items = sorted_items
        
        return new_collection

    def sort_by_rooms(self, reverse=False):
        """Сортировка по количеству комнат"""
        
        sorted_items = []
        for item in self._items:
            sorted_items.append(item)
        
        #сортировка
        n = len(sorted_items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if reverse:
                    # По убыванию
                    if sorted_items[j].rooms < sorted_items[j + 1].rooms:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
                else:
                    # По возрастанию
                    if sorted_items[j].rooms > sorted_items[j + 1].rooms:
                        sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
        
        new_collection = Apartment_collection()
        new_collection._items = sorted_items
        
        return new_collection
    
    def get_available(self):
        """Получить только доступные квартиры"""
        new_collection = Apartment_collection()
        new_collection._items = [item for item in self._items if item.is_available]
        return new_collection
    
    def get_expensive(self, threshold=10000000):
        """Получить дорогие квартиры (выше порога)"""
        new_collection = Apartment_collection()
        new_collection._items = [item for item in self._items if item.price > threshold]
        return new_collection
    
    def get_cheap(self, threshold=5000000):
        """Получить дешёвые квартиры (ниже порога)"""
        new_collection = Apartment_collection()
        new_collection._items = [item for item in self._items if item.price < threshold]
        return new_collection