"""Сохранение и загрузка данных в JSON."""
import json
import sys
import os
from typing import List, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab01.model import Apartment
from lab03.models import NewBuilding, SecondaryProperty
from lab04.models import House


def save_to_json(collection: List[Any], filepath: str) -> None:
    """Сохранить коллекцию в JSON-файл."""
    data = []
    for item in collection:
        data.append(_serialize(item))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_from_json(filepath: str) -> List[Any]:
    """Загрузить объекты из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
    items = []
    for item_data in data:
        item = _deserialize(item_data)
        if item:
            items.append(item)
    return items


def _serialize(item: Any) -> dict:
    if isinstance(item, NewBuilding):
        return {
            "type": "NewBuilding",
            "address": item.address, "area": item.area,
            "rooms": item.rooms, "price": item.price,
            "floor": item.floor, "construction_year": item.construction_year,
            "developer": item.developer, "completion_date": item.completion_date,
            "finishing_type": item.finishing_type,
            "has_underground_parking": item.has_underground_parking
        }
    elif isinstance(item, SecondaryProperty):
        return {
            "type": "SecondaryProperty",
            "address": item.address, "area": item.area,
            "rooms": item.rooms, "price": item.price,
            "floor": item.floor, "construction_year": item.construction_year,
            "previous_owners": item.previous_owners,
            "condition": item.condition, "has_debts": item.has_debts
        }
    elif isinstance(item, House):
        return {
            "type": "House",
            "address": item.address, "area": item.area,
            "land_area": item.land_area, "floors": item.floors,
            "price": item.price, "construction_year": item.construction_year,
            "has_garage": item.has_garage
        }
    else:
        return {
            "type": "Apartment",
            "address": item.address, "area": item.area,
            "rooms": item.rooms, "price": item.price,
            "floor": item.floor, "construction_year": item.construction_year
        }


def _deserialize(data: dict) -> Any:
    item_type = data.get("type")
    
    if item_type == "NewBuilding":
        return NewBuilding(
            address=data["address"], area=data["area"],
            rooms=data["rooms"], price=data["price"],
            floor=data.get("floor", 1),
            construction_year=data.get("construction_year"),
            developer=data.get("developer", ""),
            completion_date=data.get("completion_date", ""),
            finishing_type=data.get("finishing_type"),
            has_underground_parking=data.get("has_underground_parking", False)
        )
    elif item_type == "SecondaryProperty":
        return SecondaryProperty(
            address=data["address"], area=data["area"],
            rooms=data["rooms"], price=data["price"],
            floor=data.get("floor", 1),
            construction_year=data.get("construction_year"),
            previous_owners=data.get("previous_owners", 1),
            condition=data.get("condition"),
            has_debts=data.get("has_debts", False)
        )
    elif item_type == "House":
        return House(
            address=data["address"], area=data["area"],
            land_area=data.get("land_area", 0),
            floors=data.get("floors", 1),
            price=data["price"],
            construction_year=data.get("construction_year"),
            has_garage=data.get("has_garage", False)
        )
    else:
        return Apartment(
            address=data["address"], area=data["area"],
            rooms=data["rooms"], price=data["price"],
            floor=data.get("floor", 1),
            construction_year=data.get("construction_year")
        )