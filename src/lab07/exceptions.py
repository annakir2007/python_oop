"""исключения."""
class ItemNotFoundError(Exception):
    """Объект не найден в коллекции."""
    pass

class DuplicateItemError(Exception):
    """Объект с таким адресом уже существует."""
    pass