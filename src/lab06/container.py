"""
Содержит Generic-класс TypedCollection и протоколы для структурной типизации.
"""

from typing import TypeVar, Generic, Callable, Optional
from copy import deepcopy


# Базовый TypeVar без ограничений
T = TypeVar('T')
R = TypeVar('R')  # Для map() с изменением типа результата


class TypedCollection(Generic[T]):
    """
    Generic-версия коллекции объектов недвижимости.
    """
    
    def __init__(self) -> None:
        """Инициализация пустой коллекции."""
        self._items: list[T] = []
    
    def add(self, item: T) -> None:
        """Добавление объекта в коллекцию.
        
        Args:
            item: объект типа T для добавления
        """
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        """Удаление объекта из коллекции."""
        self._items.remove(item)
    
    def get_all(self) -> list[T]:
        """Получение списка всех элементов коллекции."""
        return list(self._items)
    
    def __iter__(self):
        """Итератор по элементам коллекции."""
        return iter(self._items)
    
    def __len__(self) -> int:
        """Количество элементов в коллекции."""
        return len(self._items)
    
    def __getitem__(self, index: int) -> T:
        """Получение элемента по индексу."""
        return self._items[index]
    
    def remove_at(self, index: int) -> T:
        """Удаление элемента по индексу."""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items.pop(index)
    
    def sort_by(self, key_func: Callable[[T], float]) -> 'TypedCollection[T]':
        """Сортировка коллекции по функции-ключу."""
        sorted_items = sorted(self._items, key=key_func)
        new_collection = TypedCollection[T]()
        new_collection._items = sorted_items
        return new_collection
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Поиск первого элемента, удовлетворяющего условию."""
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Фильтрация элементов по условию."""
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> list[R]:
        """Применение функции-преобразования ко всем элементам."""
        return [transform(item) for item in self._items]

from typing import Protocol


class Displayable(Protocol):
    """Протокол для объектов, которые умеют отображать информацию."""
    def display(self) -> str:
        ...


class Scorable(Protocol):
    """Протокол для объектов, которые имеют числовую оценку/рейтинг."""
    def score(self) -> float:
        ...


# TypeVar с ограничениями на основе протоколов
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)