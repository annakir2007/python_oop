from model import Apartment

# Создаем несколько квартир
apt1 = Apartment("ул. Пушкина, 10", 45.5, 2, 5500000, 3, 2015)
apt2 = Apartment("ул. Лермонтова, 15", 62.3, 3, 7800000, 7, 2018)
apt3 = Apartment("ул. Толстого, 5", 85.0, 4, 12000000, 5, 2020)
apt4 = Apartment("ул. Пушкина, 10", 45.5, 2, 5500000, 3, 2015)  #копия apt1
print("Три экземпляра класса Apartment с разными параметрами:")
print(f"1) {apt1}")  # вызывает __str__
print()
print(f"2) {apt2}")
print()
print(f"3) {apt3}")
print("repr представление:")
print(repr(apt1))
print(repr(apt2))
print(repr(apt3))  # вызывает __repr__

print("Сравнение apt1 и apt2 (разные квартиры)")
if apt1 == apt2:  # вызывает __eq__
    print("Это одна и та же квартира")
else:
    print("Это разные квартиры")

print("Сравнение apt1 и apt4 (одинаковые квартиры)")
if apt1 == apt4:  # вызывает __eq__
    print("Это одна и та же квартира")
else:
    print("Это разные квартиры")
print()
print("Обработка ошибок:")

print('Ошибка: адрес передан как число')
try:
    apt5 = Apartment(123, 45.5, 2, 5500000, 3, 2015)
except (ValueError, TypeError) as e:
    print(f"Квартира не создалась, потому что {e}\n")

print('Ошибка: адрес пустой')
try:
    apt1.address = ""  # пробуем изменить адрес
except (ValueError, TypeError) as e:
    print(f"Не удалось изменить адрес, потому что {e}\n")

print('Ошибка: отрицательная площадь')
try:
    apt1.area = -10
except (ValueError, TypeError) as e:
    print(f"Не удалось изменить площадь, потому что {e}\n")

print("Демонстрация атрибутов класса:")

print(f"Доступ через класс:")
print(f"   Минимальная площадь: {Apartment.min_area} кв.м")
print(f"   Максимальная цена: {Apartment.max_price:.0f} руб.")
print(f"   Максимальный этаж: {Apartment.max_floor}")

print(f"Доступ через экземпляр:")
print(f"   Минимальная площадь: {apt1.min_area} кв.м")
print(f"   Максимальная цена: {apt1.max_price:.0f} руб.")
print()
print("СЦЕНАРИЙ 1: Покупка квартиры")

print(f"Начальное состояние квартиры apt2:")
print(apt2)

print(f"Проверка, можно ли продать: {apt2.can_be_sold()}")
print(f"Продажа квартиры...")
result = apt2.sell()
print(f"   {result}")
print(f"Состояние после продажи:")
print(apt2)

print(f"Попытка продать еще раз:")
try:
    apt2.sell()
except ValueError as e:
    print(f"Ошибка: {e}")

print()
print("СЦЕНАРИЙ 2: Бронирование и ипотека")

print(f"Начальное состояние квартиры apt3:")
print(apt3)

print(f"Бронирование квартиры на 5 дней...")
result = apt3.reserve(5)
print(f"   {result}")

print(f"Расчет ипотеки для забронированной квартиры:")
payment = apt3.calculate_monthly_payment(20, 10)
print(f"   Ежемесячный платеж на 20 лет под 10%: {payment:.2f} руб.")

print(f"Попытка забронировать уже забронированную квартиру:")
try:
    apt3.reserve(3)
except ValueError as e:
    print(f"Ошибка: {e}")
print()
print("СЦЕНАРИЙ 3: Ремонт и изменение состояния")

print(f"Начальное состояние квартиры apt1:")
print(apt1)

print(f"Переводим квартиру в статус 'на ремонте'...")
apt1.set_unavailable()
print(f"Статус изменен")

print(f"Пытаемся продать квартиру на ремонте:")
try:
    apt1.sell()
except ValueError as e:
    print(f"Ошибка: {e}")

print(f"Проверяем, можно ли продать: {apt1.can_be_sold()}")