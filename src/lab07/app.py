"""Бизнес-логика приложения"""
import sys
import os
from typing import List, Any

# Добавляем src в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем модели
from lab01.model import Apartment
from lab03.models import NewBuilding, SecondaryProperty
from lab04.models import House
from lab07.exceptions import ItemNotFoundError, DuplicateItemError


class App:
    """Управление коллекцией недвижимости."""
    
    def __init__(self) -> None:
        self._items: List[Any] = []
    
    @property
    def items(self) -> List[Any]:
        return self._items
    
    def add_apartment(self, address: str, area: float, rooms: int,
                      price: float, floor: int, year: int) -> Apartment:
        self._check_duplicate(address)
        apartment = Apartment(address, area, rooms, price, floor, year)
        self._items.append(apartment)
        return apartment
    
    def add_new_building(self, address: str, area: float, rooms: int,
                         price: float, floor: int, year: int,
                         developer: str, completion: str,
                         finishing: str, parking: bool) -> NewBuilding:
        self._check_duplicate(address)
        nb = NewBuilding(address, area, rooms, price, floor, year,
                        developer, completion, finishing, parking)
        self._items.append(nb)
        return nb
    
    def add_secondary(self, address: str, area: float, rooms: int,
                      price: float, floor: int, year: int,
                      owners: int, condition: str, debts: bool) -> SecondaryProperty:
        self._check_duplicate(address)
        sp = SecondaryProperty(address, area, rooms, price, floor, year,
                              owners, condition, debts)
        self._items.append(sp)
        return sp
    
    def add_house(self, address: str, area: float, land_area: float,
                  floors: int, price: float, year: int,
                  has_garage: bool) -> House:
        self._check_duplicate(address)
        house = House(address, area, land_area, floors, price, year, has_garage)
        self._items.append(house)
        return house
    
    def remove_by_index(self, index: int) -> Any:
        if index < 0 or index >= len(self._items):
            raise ItemNotFoundError(f"Объект с индексом {index} не найден")
        return self._items.pop(index)
    
    def find_by_address(self, query: str) -> List[Any]:
        query_lower = query.lower()
        return [item for item in self._items 
                if query_lower in item.address.lower()]
    
    def filter_by_price(self, min_price: float, max_price: float) -> List[Any]:
        return [item for item in self._items 
                if min_price <= item.price <= max_price]
    
    def filter_by_area(self, min_area: float, max_area: float) -> List[Any]:
        return [item for item in self._items 
                if min_area <= item.area <= max_area]
    
    def filter_by_type(self, obj_type: str) -> List[Any]:
        if obj_type == 'new_building':
            return [item for item in self._items if isinstance(item, NewBuilding)]
        elif obj_type == 'secondary':
            return [item for item in self._items if isinstance(item, SecondaryProperty)]
        elif obj_type == 'house':
            return [item for item in self._items if isinstance(item, House)]
        elif obj_type == 'apartment':
            return [item for item in self._items 
                    if isinstance(item, Apartment) 
                    and not isinstance(item, (NewBuilding, SecondaryProperty))]
        return []
    
    def sort_by_price(self, reverse: bool = False) -> List[Any]:
        return sorted(self._items, key=lambda x: x.price, reverse=reverse)
    
    def sort_by_area(self, reverse: bool = False) -> List[Any]:
        return sorted(self._items, key=lambda x: x.area, reverse=reverse)
    
    def sort_by_address(self, reverse: bool = False) -> List[Any]:
        return sorted(self._items, key=lambda x: x.address, reverse=reverse)
    
    def get_statistics(self) -> dict:
        if not self._items:
            return {"total": 0, "avg_price": 0, "avg_area": 0,
                    "apartments": 0, "houses": 0}
        
        apartments = sum(1 for item in self._items 
                        if isinstance(item, Apartment) 
                        and not isinstance(item, House))
        houses = sum(1 for item in self._items if isinstance(item, House))
        
        return {
            "total": len(self._items),
            "apartments": apartments,
            "houses": houses,
            "avg_price": sum(item.price for item in self._items) / len(self._items),
            "avg_area": sum(item.area for item in self._items) / len(self._items)
        }
    
    def _check_duplicate(self, address: str) -> None:
        for item in self._items:
            if item.address.lower() == address.lower():
                raise DuplicateItemError(
                    f"Объект с адресом '{address}' уже существует"
                )