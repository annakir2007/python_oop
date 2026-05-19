"""вход в консольное приложение."""
import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab07.app import App
from lab07.cli import CLI
from lab07.storage import save_to_json, load_from_json

DATA_FILE = os.path.join(os.path.dirname(__file__), "properties.json")


def main() -> None:
    """Главная функция. Загружает данные, запускает CLI, сохраняет при выходе."""
    app = App()
    
    if os.path.exists(DATA_FILE):
        items = load_from_json(DATA_FILE)
        app._items = items
    else:
        print("Файл данных не найден, начата пустая коллекция")
    
    cli = CLI(app)
    
    try:
        cli.run()
    finally:
        save_to_json(app.items, DATA_FILE)
        print(f"Данные сохранены ({len(app.items)} объектов)")


if __name__ == "__main__":
    main()