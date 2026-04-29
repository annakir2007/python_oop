"""
Класс Apartment для представления квартиры в системе недвижимости.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from validate import (validate_address, validate_area, validate_rooms, validate_price, validate_floor, validate_construction_year)

class Apartment:
    # Атрибуты класса:
    min_area = 10  # минимальная площадь
    max_area = 500  # максимальная площадь
    min_rooms = 1  # минимальное количество комнат
    max_rooms = 10  # максимальное количество комнат
    min_price = 100000  # минимальная цена
    max_price = 100000000  # максимальная цена (100 млн)
    min_floor = 1  # минимальный этаж
    max_floor = 50  # максимальный этаж
    
    # Константы состояний
    STATUS_AVAILABLE = "доступна"
    STATUS_RESERVED = "забронирована"
    STATUS_SOLD = "продана"
    STATUS_RENTED = "сдана в аренду"
    STATUS_UNDER_REPAIR = "на ремонте"
    
    def __init__(self, address: str, area: float, rooms: int, price: float, 
                 floor: int = 1, construction_year: int = None):
        # Закрытые атрибуты (с двумя подчеркиваниями)
        self.__address = None
        self.__area = None
        self.__rooms = None
        self.__price = None
        self.__floor = None
        self.__construction_year = None
        self.__status = self.STATUS_AVAILABLE  # состояние квартиры
        self.__reserved_until = None
        self.__rental_contracts = []
        
        # Устанавливаем значения через сеттеры
        self.address = address
        self.area = area
        self.rooms = rooms
        self.price = price
        self.floor = floor
        
        # Обработка года постройки
        if construction_year is None:
            construction_year = datetime.now().year
        self.construction_year = construction_year
    
    # Свойства:
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, value):
        # Используем функцию валидации из модуля validate
        self.__address = validate_address(value, "Адрес")
    
    @property
    def area(self):
        return self.__area
    
    @area.setter
    def area(self, value):
        # Используем функцию валидации с атрибутами класса
        self.__area = validate_area(value, self.min_area, self.max_area)
    
    @property
    def rooms(self):
        return self.__rooms
    
    @rooms.setter
    def rooms(self, value):
        self.__rooms = validate_rooms(value, self.min_rooms, self.max_rooms)
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        self.__price = validate_price(value, self.min_price, self.max_price)
    
    @property
    def floor(self):
        return self.__floor
    
    @floor.setter
    def floor(self, value):
        self.__floor = validate_floor(value, self.min_floor, self.max_floor)
    
    @property
    def construction_year(self):
        return self.__construction_year
    
    @construction_year.setter
    def construction_year(self, value):
        self.__construction_year = validate_construction_year(value)
    
    @property
    def status(self):
        # Проверяем, не закончилась ли бронь
        if (self.__status == self.STATUS_RESERVED and 
            self.__reserved_until and 
            datetime.now() > self.__reserved_until):
            self.__status = self.STATUS_AVAILABLE
            self.__reserved_until = None
        return self.__status
    
    @property
    def is_available(self):
        """Доступна ли квартира"""
        return self.__status == self.STATUS_AVAILABLE
    
    # Магические методы:
    
    def __str__(self):
        return (f"Адрес: {self.__address}\n"
                f"Площадь: {self.__area:.1f} кв.м.\n"
                f"Количество комнат: {self.__rooms}\n"
                f"Этаж: {self.__floor}\n"
                f"Год постройки: {self.__construction_year}\n"
                f"Цена: {self.__price:.0f} руб.\n"
                f"Статус: {self.__status}")
    
    def __repr__(self):
        return (f"Apartment(address='{self.__address}', area={self.__area}, "
                f"rooms={self.__rooms}, price={self.__price:.0f}, floor={self.__floor:.0f}, "
                f"construction_year={self.__construction_year})")
    
    def __eq__(self, other):
        """Сравнение квартир"""
        if not isinstance(other, Apartment):
            return False
        return (self.__address == other.__address and 
                self.__area == other.__area and
                self.__rooms == other.__rooms and
                self.__price == other.__price and
                self.__floor == other.__floor and
                self.__construction_year == other.__construction_year)
    
    # Бизнес-методы:
    
    def sell(self):
        """Продажа квартиры"""
        if self.__status == self.STATUS_SOLD:
            raise ValueError("Квартира уже продана")
        if self.__status == self.STATUS_RENTED:
            raise ValueError("Нельзя продать квартиру, сданную в аренду")
        
        self.__status = self.STATUS_SOLD
        self.__reserved_until = None
        return f"Квартира продана по цене {self.__price:.0f} руб."
    
    def reserve(self, days=7):
        """Бронирование квартиры"""
        if self.__status != self.STATUS_AVAILABLE:
            raise ValueError("Квартира недоступна для бронирования")
        
        self.__status = self.STATUS_RESERVED
        self.__reserved_until = datetime.now() + timedelta(days=days)
        return f"Квартира забронирована на {days} дней"
    
    def set_unavailable(self):
        """Перевод в статус 'на ремонте'"""
        self.__status = self.STATUS_UNDER_REPAIR
        self.__reserved_until = None
    
    def calculate_monthly_payment(self, years, percent):
        """Расчет ипотеки"""
        if self.__status == self.STATUS_SOLD:
            raise ValueError("Квартира уже продана")
        
        months = years * 12
        monthly_rate = percent / 100 / 12
        
        if monthly_rate == 0:
            return self.__price / months
        
        payment = self.__price * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
        return round(payment, 2)
