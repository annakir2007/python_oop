"""
Модуль коллекции объектов недвижимости с поддержкой функционального стиля.
"""

from typing import Callable, List, Any
from copy import deepcopy


class ApartmentCollection:
    """Коллекция объектов недвижимости."""
    
    def __init__(self, items: List[Any] = None):
        """Инициализация коллекции."""
        self._items = items if items is not None else []
    
    def __iter__(self):
        """Итератор по элементам."""
        return iter(self._items)
    
    def __len__(self):
        """Количество элементов."""
        return len(self._items)
    
    def __getitem__(self, index):
        """Получение элемента по индексу."""
        return self._items[index]
    
    def add(self, item):
        """Добавление объекта в коллекцию."""
        self._items.append(item)
    
    def sort_by(self, key_func: Callable):
        """Сортировка коллекции по функции-ключу.
        
        Args:
            key_func: функция-ключ для сортировки
            
        Returns:
            Новая отсортированная коллекция
        """
        sorted_items = sorted(self._items, key=key_func)
        return ApartmentCollection(sorted_items)
    
    def filter_by(self, predicate: Callable):
        """Фильтрация коллекции по предикату.
        
        Args:
            predicate: функция-предикат
            
        Returns:
            Новая отфильтрованная коллекция
        """
        filtered_items = list(filter(predicate, self._items))
        return ApartmentCollection(filtered_items)
    
    def apply(self, func: Callable):
        """Применение функции ко всем элементам.
        
        Args:
            func: функция для применения
            
        Returns:
            Новая коллекция с обработанными элементами
        """
        items_copy = deepcopy(self._items)
        processed_items = [func(item) for item in items_copy]
        return ApartmentCollection(processed_items)
    
    def to_list(self):
        """Получение списка элементов."""
        return list(self._items)
    
    def clone(self):
        """Создание копии коллекции."""
        return ApartmentCollection(deepcopy(self._items))