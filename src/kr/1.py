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

a = Apartment('ул. Ленина 5', 75, 3, 12_000_000, 4)
print(a)                         # ул. Ленина 5 — 3-комн., 75.0 м², 4 этаж, 12000000.0 руб.
print(a.price_per_meter())       # 160000.0
print(a.total_with_commission()) # 12360000.0

Apartment.agency_commission_percent = 5
print(a.total_with_commission()) # 12600000.0

a.mark_as_sold()
# a.mark_as_sold()  # ValueError: Квартира уже продана

# Проверка ошибок:
# Apartment('', 50, 2, 1, 1)      # ValueError: адрес
# Apartment('ул.X', -5, 2, 1, 1)  # ValueError: площадь
# Apartment('ул.X', 50, 11, 1, 1) # ValueError: комнат