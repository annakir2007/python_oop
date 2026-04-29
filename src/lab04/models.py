"""
Модуль models.py
Расширяет существующие классы из lab01 и lab02,
добавляя реализацию интерфейсов, и создаёт новые классы.
"""

import sys
import os
from datetime import datetime
from typing import List, Any

# Добавляем папки с модулями в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab02'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab04'))

from interfaces import Printable, Comparable
from model import Apartment as BaseApartment
from collection import Apartment_collection as BaseCollection


class Apartment(BaseApartment, Printable, Comparable):
    """Расширенный класс квартиры."""

    def to_string(self) -> str:
        return (f"Квартира | Статус: {self.status}\n"
                f"  Адрес: {self.address}\n"
                f"  Площадь: {self.area:.1f} кв.м | Комнат: {self.rooms}\n"
                f"  Этаж: {self.floor} | Год постройки: {self.construction_year}\n"
                f"  Цена: {self.price:.0f} руб.")

    def compare_to(self, other: Any) -> int:
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только квартиры между собой")

        self_ppm = self.price / self.area
        other_ppm = other.price / other.area

        if self_ppm < other_ppm:
            return -1
        elif self_ppm > other_ppm:
            return 1
        return 0


class House(Printable, Comparable):
    """Класс дома."""

    STATUS_AVAILABLE = "доступен"
    STATUS_SOLD = "продан"
    STATUS_UNDER_CONSTRUCTION = "строится"

    def __init__(self, address: str, area: float, land_area: float,
                 floors: int, price: float, construction_year: int = None,
                 has_garage: bool = False):
        self.__address = address
        self.__area = area
        self.__land_area = land_area
        self.__floors = floors
        self.__price = price
        self.__construction_year = construction_year or datetime.now().year
        self.__has_garage = has_garage
        self.__status = self.STATUS_AVAILABLE

    def to_string(self) -> str:
        garage_info = "Гараж: есть" if self.__has_garage else "Гараж: нет"
        return (f"Дом | Статус: {self.__status}\n"
                f"  Адрес: {self.__address}\n"
                f"  Площадь: {self.__area:.1f} кв.м | Участок: {self.__land_area:.1f} сот.\n"
                f"  Этажей: {self.__floors} | Год постройки: {self.__construction_year}\n"
                f"  {garage_info}\n"
                f"  Цена: {self.__price:.0f} руб.")

    def compare_to(self, other: Any) -> int:
        if not isinstance(other, House):
            raise TypeError("Можно сравнивать только дома между собой")

        land_price_per_sotka = 50000
        self_total = self.__price + self.__land_area * land_price_per_sotka
        other_total = other.__price + other.__land_area * land_price_per_sotka

        if self_total < other_total:
            return -1
        elif self_total > other_total:
            return 1
        return 0

    @property
    def address(self):
        return self.__address

    @property
    def area(self):
        return self.__area

    @property
    def land_area(self):
        return self.__land_area

    @property
    def floors(self):
        return self.__floors

    @property
    def price(self):
        return self.__price

    @property
    def construction_year(self):
        return self.__construction_year

    @property
    def has_garage(self):
        return self.__has_garage

    @property
    def status(self):
        return self.__status

    def sell(self):
        if self.__status == self.STATUS_SOLD:
            raise ValueError("Дом уже продан")
        self.__status = self.STATUS_SOLD
        total_value = self.__price + self.__land_area * 50000
        return f"Дом по адресу {self.__address} продан за {total_value:,.0f} руб. (с учётом участка)"

    def __str__(self):
        return self.to_string()


class PropertyCollection:
    """Коллекция объектов недвижимости (без наследования от BaseCollection)."""

    def __init__(self):
        self.__items: List[Any] = []

    def add(self, item: Any):
        if not isinstance(item, (BaseApartment, House)):
            raise TypeError(
                f"Можно добавлять только объекты недвижимости, "
                f"получен {type(item).__name__}"
            )
        self.__items.append(item)

    def get_all(self) -> List[Any]:
        return self.__items.copy()

    def get_printable(self) -> List[Printable]:
        return [item for item in self.__items if isinstance(item, Printable)]

    def get_comparable(self) -> List[Comparable]:
        return [item for item in self.__items if isinstance(item, Comparable)]

    def print_all(self):
        for item in self.get_printable():
            print(item.to_string())

    def sort_by_comparison(self):
        apartments = [item for item in self.__items if isinstance(item, Apartment)]
        houses = [item for item in self.__items if isinstance(item, House)]

        for i in range(len(apartments)):
            for j in range(len(apartments) - 1 - i):
                if apartments[j].compare_to(apartments[j + 1]) > 0:
                    apartments[j], apartments[j + 1] = apartments[j + 1], apartments[j]

        for i in range(len(houses)):
            for j in range(len(houses) - 1 - i):
                if houses[j].compare_to(houses[j + 1]) > 0:
                    houses[j], houses[j + 1] = houses[j + 1], houses[j]

        other_items = [item for item in self.__items
                       if not isinstance(item, (Apartment, House))]
        self.__items = apartments + houses + other_items

    def __len__(self):
        return len(self.__items)