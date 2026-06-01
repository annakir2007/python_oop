from typing import TypeVar, Generic, Callable
from abc import ABC, abstractmethod

class Apartment:
    agency_commission_percent = 3

    def __init__(self, address, area, rooms, price, floor):
        # address
        address = address.strip()
        if not address:
            raise ValueError("Адрес не может быть пустым")
        self.__address = address

        # area
        if area <= 0:
            raise ValueError("Площадь должна быть > 0")
        self.__area = area

        # rooms
        if not isinstance(rooms, int) or rooms < 1 or rooms > 10:
            raise ValueError("Комнат должно быть от 1 до 10")
        self.__rooms = rooms

        # price
        if price <= 0:
            raise ValueError("Цена должна быть > 0")
        self.__price = price

        # floor
        if not isinstance(floor, int) or floor < 1 or floor > 100:
            raise ValueError("Этаж должен быть от 1 до 100")
        self.__floor = floor

        # is_sold
        self.__is_sold = False

    #Свойства
    @property
    def address(self):
        return self.__address

    @property
    def area(self):
        return self.__area

    @property
    def rooms(self):
        return self.__rooms

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть > 0")
        self.__price = value

    @property
    def floor(self):
        return self.__floor

    @property
    def is_sold(self):
        return self.__is_sold

    #Методы
    def price_per_meter(self):
        return self.__price / self.__area

    def total_with_commission(self):
        return self.__price * (1 + Apartment.agency_commission_percent / 100)

    def mark_as_sold(self):
        if self.__is_sold:
            raise ValueError("Квартира уже продана")
        self.__is_sold = True

    # Специальные методы
    def __str__(self):
        return (f"{self.__address} — {self.__rooms}-комн., "
                f"{self.__area:.1f} м², {self.__floor} этаж, "
                f"{self.__price:.1f} руб.")

    def __eq__(self, other):
        if not isinstance(other, Apartment):
            return NotImplemented
        return self.__address == other.__address and self.__floor == other.__floor

# Generic-реестр
T = TypeVar('T', bound=Apartment)

class Listing(Generic[T]):
    def __init__(self):
        self.__items: list[T] = []
        self.__observers: list[Observer] = []

    def add(self, item: T) -> None:
        self.__items.append(item)

    def get_active(self) -> list[T]:
        return [i for i in self.__items if not i.is_sold]

    def find(self, predicate: Callable[[T], bool]) -> list[T]:
        return [i for i in self.__items if predicate(i)]

    def mark_sold(self, item: T) -> None:
        if item.is_sold: raise ValueError("Квартира уже продана")
        item.mark_as_sold()
        self.__notify({"type": "sold", "address": item.address, "price": item.price})

    def apply_valuation(self, strategy: 'ValuationStrategy') -> dict[str, float]:
        return {i.address: strategy.estimate(i) for i in self.get_active()}

    def subscribe(self, observer: 'Observer') -> None:
        self.__observers.append(observer)

    def unsubscribe(self, observer: 'Observer') -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def __notify(self, event: dict) -> None:
        for o in self.__observers:
            o.update(event)

    def __iter__(self):
        return iter(self.__items)

    def __len__(self):
        return len(self.__items)


#Стратегии оценки стоимости
class ValuationStrategy(ABC):
    @abstractmethod
    def estimate(self, apartment: Apartment) -> float: pass

class MarketValuation(ValuationStrategy):
    def __init__(self, ppm: float):
        self.__ppm = ppm
    def estimate(self, a: Apartment) -> float:
        return a.area * self.__ppm

class FloorAdjustedValuation(ValuationStrategy):
    def __init__(self, base: float, first_pen: float, top_pen: float):
        self.__base = base
        self.__first_pen = first_pen
        self.__top_pen = top_pen
    def estimate(self, a: Apartment) -> float:
        base_price = a.area * self.__base
        if a.floor == 1:
            return base_price * self.__first_pen
        elif a.floor > 20:
            return base_price * self.__top_pen
        return base_price

class ComparativeValuation(ValuationStrategy):
    def __init__(self, similar: list[Apartment]):
        self.__similar = similar
    def estimate(self, a: Apartment) -> float:
        if not self.__similar: return 0.0
        avg = sum(x.price_per_meter() for x in self.__similar) / len(self.__similar)
        return a.area * avg


#Наблюдатель
class Observer(ABC):
    @abstractmethod
    def update(self, event: dict) -> None: pass

class EmailNotifier(Observer):
    def __init__(self, email: str):
        self.__email = email
    def update(self, event: dict) -> None:
        if event["type"] == "sold":
            print(f"[Email → {self.__email}]: квартира продана — {event['address']}, {event['price']} руб.")

class StatsCollector(Observer):
    def __init__(self):
        self.__stats: dict[str, int] = {}
    def update(self, event: dict) -> None:
        t = event["type"]
        self.__stats[t] = self.__stats.get(t, 0) + 1
    def get_stats(self) -> dict[str, int]:
        return dict(self.__stats)


# Пример входных данных
registry: Listing[Apartment] = Listing()
registry.add(Apartment('ул. Ленина 5', 75, 3, 12_000_000, 4))
registry.add(Apartment('пр. Мира 10', 50, 2, 8_000_000, 1))
registry.add(Apartment('ул. Дубова 2', 100, 4, 20_000_000, 22))

stats = StatsCollector()
registry.subscribe(EmailNotifier('agent@office.ru'))
registry.subscribe(stats)

registry.mark_sold(registry.find(lambda a: a.rooms == 2)[0])
print(stats.get_stats())               # {'sold': 1}
print(registry.apply_valuation(MarketValuation(180000)))        # {'ул. Ленина 5': 13500000, 'ул. Дубова 2': 18000000}
print(registry.apply_valuation(FloorAdjustedValuation(180000, 0.9, 0.95)))    # {'ул. Ленина 5': 13500000, 'ул. Дубова 2': 17100000.0}
print(len(registry.get_active()))       # # 2  (одна продана)