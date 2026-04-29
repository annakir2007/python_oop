"""
Модуль interfaces.py
Содержит абстрактные базовые классы (интерфейсы) для системы недвижимости.
"""

from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    """
    Интерфейс для объектов, которые могут быть представлены в виде строки.
    Обязывает реализовать метод to_string().
    """

    @abstractmethod
    def to_string(self) -> str:
        """Возвращает строковое представление объекта."""
        pass


class Comparable(ABC):
    """
    Интерфейс для объектов, которые можно сравнивать между собой.
    Обязывает реализовать метод compare_to().
    """

    @abstractmethod
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает текущий объект с другим.
        
        Returns:
            отрицательное число, если self < other
            0, если self == other
            положительное число, если self > other
        """
        pass