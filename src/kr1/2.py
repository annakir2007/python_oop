class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self._owner = owner
        self._balance = balance


    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0")
        self._balance += amount


    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть > 0")
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")
        self._balance -= amount


    def get_balance(self):
        return self._balance


    def __str__(self):
        return f"{self._owner}: {self._balance:.2f} руб."


class SavingsAccount(BankAccount):
    """Накопительный счёт: нельзя снять если остаток < 1000 руб."""
    def __init__(self, owner: str, balance: float = 0):
        super().__init__(owner, balance)
        self._min_balance = 1000
    
    def withdraw(self, amount:float):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть > 0")
        if self._balance - amount < self._min_balance:
            raise ValueError(f"Невозможно снять {amount:.2f} руб. " f"Минимальный остаток: {self._min_balance:.2f} руб.")
        self._balance -= amount
