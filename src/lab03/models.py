from datetime import datetime
import sys
import os
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_path)
sys.path.append(os.path.join(src_path, 'lab01'))
sys.path.append(os.path.join(src_path, 'lab02'))
from lab01.model import Apartment
from lab02.collection import Apartment_collection

class NewBuilding(Apartment):
    """Класс для новостроек."""
    
    # Типы отделки
    FINISHING_NONE = "без отделки"
    FINISHING_ROUGH = "черновая"
    FINISHING_FINE = "чистовая"
    FINISHING_DESIGNER = "дизайнерская"
    
    def __init__(self, address: str, area: float, rooms: int, price: float,
                 floor: int = 1, construction_year: int = None,
                 developer: str = "", completion_date: str = "",
                 finishing_type: str = None, has_underground_parking: bool = False):
        super().__init__(address, area, rooms, price, floor, construction_year)
        
        # Новые атрибуты
        self.__developer = developer
        self.__completion_date = completion_date
        if finishing_type:
            self.__finishing_type = finishing_type
        else:
            self.__finishing_type = self.FINISHING_ROUGH
        self.__has_underground_parking = has_underground_parking
        self.__mortgage_programs = []
        self.__construction_stage = "строится"
    
    @property
    def developer(self):
        return self.__developer
    
    @developer.setter
    def developer(self, value):
        if not value.strip():
            raise ValueError("Название застройщика не может быть пустым")
        self.__developer = value.strip()
    
    @property
    def completion_date(self):
        return self.__completion_date
    
    @property
    def finishing_type(self):
        return self.__finishing_type
    
    @property
    def has_underground_parking(self):
        return self.__has_underground_parking
    
    @property
    def construction_stage(self):
        return self.__construction_stage
    
    # Новый метод 1
    def add_mortgage_program(self, bank: str, rate: float, min_down_payment: float):
        """Добавить ипотечную программу."""
        program = {'bank': bank, 'rate': rate, 'min_down_payment': min_down_payment}
        self.__mortgage_programs.append(program)
        return f"Добавлена ипотека от {bank}: {rate}%"
    
    # Новый метод 2
    def get_best_mortgage(self):
        """Найти лучшую ипотечную программу."""
        if not self.__mortgage_programs:
            return None
        best_program = self.__mortgage_programs[0]
        best_rate = best_program['rate']
        for program in self.__mortgage_programs:
            if program['rate'] < best_rate:
                best_program = program
                best_rate = program['rate']
        return best_program
    
    # Новый метод 3
    def calculate_finishing_cost(self):
        """Рассчитать стоимость отделки."""
        prices = {
            self.FINISHING_NONE: 0,
            self.FINISHING_ROUGH: 3000,
            self.FINISHING_FINE: 8000,
            self.FINISHING_DESIGNER: 15000
        }
        return round(self.area * prices.get(self.__finishing_type, 0), 2)
    
    # Переопределение __str__ 
    def __str__(self):
        # Получаем базовую информацию через родительский __str__
        base_info = f"Адрес: {self.address}\n"
        base_info += f"Площадь: {self.area:.1f} кв.м.\n"
        base_info += f"Количество комнат: {self.rooms}\n"
        base_info += f"Этаж: {self.floor}\n"
        base_info += f"Год постройки: {self.construction_year}\n"
        base_info += f"Цена: {self.price:,.0f} руб.\n"
        base_info += f"Статус: {self.status}"
        
        parking_text = "есть" if self.__has_underground_parking else "нет"
        finishing_cost = self.calculate_finishing_cost()
        
        result = base_info
        result += "\nХарактеристики новостройки:"
        result += f"\nЗастройщик: {self.__developer}"
        result += f"\nСдача: {self.__completion_date}"
        result += f"\nОтделка: {self.__finishing_type}"
        result += f"\nПаркинг: {parking_text}"
        result += f"\nСтоимость отделки: {finishing_cost:,.0f} руб."
        return result
    
    # Полиморфный метод
    def calculate_monthly_payment(self, years, percent):
        """Расчёт ипотеки с учётом скидки от застройщика."""
        # Базовая стоимость с отделкой и паркингом
        total_price = self.price + self.calculate_finishing_cost()
        if self.__has_underground_parking:
            total_price += 800000
        
        # Расчёт ипотеки от полной стоимости
        months = years * 12
        monthly_rate = percent / 100 / 12
        
        if monthly_rate == 0:
            return round(total_price / months, 2)
        
        payment = total_price * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
        return round(payment, 2)


class SecondaryProperty(Apartment):
    """Класс для представления вторичного жилья."""
    
    CONDITION_EXCELLENT = "отличное"
    CONDITION_GOOD = "хорошее"
    CONDITION_SATISFACTORY = "удовлетворительное"
    CONDITION_BAD = "плохое"
    
    def __init__(self, address: str, area: float, rooms: int, price: float,
                 floor: int = 1, construction_year: int = None,
                 previous_owners: int = 1, condition: str = None,
                 has_debts: bool = False):
        super().__init__(address, area, rooms, price, floor, construction_year)
        
        # Новые атрибуты
        self.__previous_owners = previous_owners
        if condition:
            self.__condition = condition
        else:
            self.__condition = self.CONDITION_GOOD
        self.__has_debts = has_debts
        self.__renovation_history = []
    
    @property
    def previous_owners(self):
        return self.__previous_owners
    
    @property
    def condition(self):
        return self.__condition
    
    @property
    def has_debts(self):
        return self.__has_debts
    
    # Новый метод 1
    def add_renovation(self, year: int, description: str, cost: float):
        """Добавить информацию о ремонте."""
        self.__renovation_history.append({
            'year': year, 'description': description, 'cost': cost
        })
        return f"Добавлен ремонт за {year} год"
    
    # Новый метод 2
    def calculate_discount(self):
        """Рассчитать скидку за состояние."""
        discounts = {
            self.CONDITION_EXCELLENT: 0,
            self.CONDITION_GOOD: 0.05,
            self.CONDITION_SATISFACTORY: 0.15,
            self.CONDITION_BAD: 0.30
        }
        return round(self.price * discounts.get(self.__condition, 0), 2)
    
    # Новый метод 3
    def get_age(self):
        """Получить возраст объекта."""
        return datetime.now().year - self.construction_year
    
    # Переопределение __str__
    def __str__(self):
        base_info = f"Адрес: {self.address}\n"
        base_info += f"Площадь: {self.area:.1f} кв.м.\n"
        base_info += f"Количество комнат: {self.rooms}\n"
        base_info += f"Этаж: {self.floor}\n"
        base_info += f"Год постройки: {self.construction_year}\n"
        base_info += f"Цена: {self.price:,.0f} руб.\n"
        base_info += f"Статус: {self.status}"
        
        age = self.get_age()
        discount = self.calculate_discount()
        debts_text = "есть" if self.__has_debts else "нет"
        
        result = base_info
        result += "\nХарактеристики вторичного жилья"
        result += f"\nВозраст: {age} лет"
        result += f"\nВладельцев: {self.__previous_owners}"
        result += f"\nСостояние: {self.__condition}"
        result += f"\nДолги: {debts_text}"
        result += f"\nСкидка: {discount:,.0f} руб."
        
        return result
    
    # Полиморфный метод
    def sell(self):
        """Продажа вторичного жилья"""
        if self.status == self.STATUS_SOLD:
            raise ValueError("Объект уже продан")
        if self.__has_debts:
            raise ValueError("Нельзя продать объект с долгами по ЖКХ")
        
        return super().sell()


# Добавляем новые методы в существующий класс коллекции
def get_only_new_buildings(self):
    """Получить только новостройки."""
    new_coll = Apartment_collection()
    new_coll._items = [item for item in self._items if isinstance(item, NewBuilding)]
    return new_coll

def get_only_secondary(self):
    """Получить только вторичное жильё."""
    new_coll = Apartment_collection()
    new_coll._items = [item for item in self._items if isinstance(item, SecondaryProperty)]
    return new_coll

def filter_by_developer(self, developer: str):
    """Фильтрация по застройщику."""
    new_coll = Apartment_collection()
    new_coll._items = [
        item for item in self._items 
        if isinstance(item, NewBuilding) and item.developer.lower() == developer.lower()
    ]
    return new_coll

def calculate_total_price(self):
    """Расчёт общей цены всех объектов."""
    total = 0
    for item in self._items:
        if isinstance(item, NewBuilding):
            #цена + отделка + паркинг
            extra = item.calculate_finishing_cost()
            if item.has_underground_parking:
                extra += 800000
            total += item.price + extra
        elif isinstance(item, SecondaryProperty):
            #цена - скидка
            total += item.price - item.calculate_discount()
        else:
            total += item.price
    return round(total, 2)

# Добавляем методы в класс
Apartment_collection.get_only_new_buildings = get_only_new_buildings
Apartment_collection.get_only_secondary = get_only_secondary
Apartment_collection.filter_by_developer = filter_by_developer
Apartment_collection.calculate_total_price = calculate_total_price