# *Дополнительное задание:
#
# Ты разрабатываешь программное обеспечение для сети магазинов. Каждый магазин в этой сети имеет свои особенности,
# но также существуют общие характеристики, такие как адрес, название и ассортимент товаров.
# Ваша задача — создать класс `Store`, который можно будет использовать для создания различных магазинов.
#
# Шаги:
#
# 1. Создай класс `Store`:
#
# -Атрибуты класса:
#
# - `name`: название магазина.
# - `address`: адрес магазина.
# - `items`: словарь, где ключ - название товара, а значение - его цена. Например, `{'apples': 0.5, 'bananas': 0.75}`.
#
# - Методы класса:
#
# - `__init__ - конструктор, который инициализирует название и адрес, а также пустой словарь для `items`.
# - метод для добавления товара в ассортимент.
# - метод для удаления товара из ассортимента.
# - метод для получения цены товара по его названию. Если товар отсутствует, возвращайте `None`.
# - метод для обновления цены товара.
#
# 2. Создай несколько объектов класса `Store`:
# Создай не менее трех различных магазинов с разными названиями, адресами и добавь в каждый из них несколько товаров.



class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}  # Пустой словарь для товаров

    def add_item(self, item_name, price):
        """Добавляет товар в ассортимент магазина"""
        self.items[item_name] = price
        print(f"Товар '{item_name}' добавлен в {self.name}")

    def remove_item(self, item_name):
        """Удаляет товар из ассортимента"""
        if item_name in self.items:
            del self.items[item_name]
            print(f"Товар '{item_name}' удален из {self.name}")
        else:
            print(f"Товар '{item_name}' не найден в {self.name}")

    def get_price(self, item_name):
        """Возвращает цену товара или None если товара нет"""
        return self.items.get(item_name)

    def update_price(self, item_name, new_price):
        """Обновляет цену товара"""
        if item_name in self.items:
            self.items[item_name] = new_price
            print(f"Цена товара '{item_name}' обновлена в {self.name}")
        else:
            print(f"Товар '{item_name}' не найден в {self.name}")

    def show_items(self):
        """Выводит список товаров магазина"""
        print(f"\nМагазин: {self.name} ({self.address})")
        if not self.items:
            print("Ассортимент пуст")
        else:
            print("Ассортимент:")
            for item, price in self.items.items():
                print(f"- {item}: {price} руб.")


# Создаем несколько магазинов
store1 = Store("Пятерочка", "ул. Ленина, 10")
store1.add_item("Молоко", 85)
store1.add_item("Хлеб", 45)
store1.add_item("Яйца", 120)

store2 = Store("Дикси", "пр. Мира, 25")
store2.add_item("Чай", 150)
store2.add_item("Кофе", 350)
store2.add_item("Сахар", 90)

store3 = Store("Магнит", "ул. Гагарина, 5")
store3.add_item("Печенье", 75)
store3.add_item("Шоколад", 110)
store3.add_item("Вода", 50)



# Демонстрация работы методов

# Пример обновления цены
store1.show_items()
store1.update_price("Молоко", 90)
print(f"Новая цена молока: {store1.get_price('Молоко')} руб.")


# Пример удаления товара
store2.show_items()
store2.remove_item("Сахар")
store2.show_items()

# Попытка получить цену несуществующего товара
store3.show_items()
print(f"Цена колбасы: {store3.get_price('Колбаса')}")