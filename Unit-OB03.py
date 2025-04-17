# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`)
# и методы (`make_sound()`, `eat()`) для всех животных.
#
# 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`,
# которые наследуют от класса `Animal`. Добавьте специфические атрибуты и переопределите методы,
# если требуется (например, различный звук для `make_sound()`).
#
# 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`,
# которая принимает список животных и вызывает метод `make_sound()` для каждого животного.
#
# 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках.
# Должны быть методы для добавления животных и сотрудников в зоопарк.
#
# 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`,
# которые могут иметь специфические методы
# (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).
#
# Дополнительно:
# Попробуйте добавить дополнительные функции в вашу программу,
# такие как сохранение информации о зоопарке в файл и возможность её загрузки,
# чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.


import json
from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def make_sound(self):
        pass

    def eat(self):
        print(f"{self.name} ест")


class Bird(Animal):
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        print(f"{self.name} поет: Чик-чирик!")

    def fly(self):
        print(f"{self.name} летает с размахом крыльев {self.wingspan} см")


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} издает звук: Гррр!")

    def run(self):
        print(f"{self.name} бежит")


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} шипит: Шшшс!")

    def bask_in_sun(self):
        print(f"{self.name} греется на солнце")


class ZooStaff(ABC):
    def __init__(self, name, position):
        self.name = name
        self.position = position

    @abstractmethod
    def perform_duty(self):
        pass


class ZooKeeper(ZooStaff):
    def __init__(self, name):
        super().__init__(name, "Смотритель")

    def perform_duty(self):
        print(f"{self.name} кормит животных")

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}")
        animal.eat()


class Veterinarian(ZooStaff):
    def __init__(self, name):
        super().__init__(name, "Ветеринар")

    def perform_duty(self):
        print(f"{self.name} проверяет здоровье животных")

    def heal_animal(self, animal):
        print(f"{self.name} осматривает {animal.name}")
        print(f"{animal.name} проходит медицинский осмотр")


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"{animal.name} добавлен(а) в {self.name}")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"{staff_member.name} ({staff_member.position}) добавлен(а) в персонал")

    def show_animals(self):
        print(f"\nЖивотные в {self.name}:")
        for animal in self.animals:
            print(f"- {animal.name} ({animal.__class__.__name__}), возраст: {animal.age}")

    def show_staff(self):
        print(f"\nПерсонал {self.name}:")
        for staff in self.staff:
            print(f"- {staff.name} ({staff.position})")

    def save_to_file(self, filename):
        data = {
            "zoo_name": self.name,
            "animals": [
                {
                    "type": animal.__class__.__name__,
                    "name": animal.name,
                    "age": animal.age,
                    **({"wingspan": animal.wingspan} if isinstance(animal, Bird) else {}),
                    **({"fur_color": animal.fur_color} if isinstance(animal, Mammal) else {}),
                    **({"scale_type": animal.scale_type} if isinstance(animal, Reptile) else {})
                } for animal in self.animals
            ],
            "staff": [
                {
                    "type": staff.__class__.__name__,
                    "name": staff.name
                } for staff in self.staff
            ]
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Данные зоопарка сохранены в {filename}")

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        zoo = cls(data["zoo_name"])

        for animal_data in data["animals"]:
            animal_type = animal_data.pop("type")
            if animal_type == "Bird":
                zoo.add_animal(Bird(**animal_data))
            elif animal_type == "Mammal":
                zoo.add_animal(Mammal(**animal_data))
            elif animal_type == "Reptile":
                zoo.add_animal(Reptile(**animal_data))

        for staff_data in data["staff"]:
            staff_type = staff_data.pop("type")
            if staff_type == "ZooKeeper":
                zoo.add_staff(ZooKeeper(**staff_data))
            elif staff_type == "Veterinarian":
                zoo.add_staff(Veterinarian(**staff_data))

        print(f"Данные зоопарка загружены из {filename}")
        return zoo


def animal_sound(animals):
    print("\nЗвуки животных:")
    for animal in animals:
        animal.make_sound()


def check_all_interactions(zoo):
    """Проверка всех взаимодействий между сотрудниками и животными"""
    print("\n")
    print("ПОЛНАЯ ПРОВЕРКА ВЗАИМОДЕЙСТВИЙ")



    # Вариант 1
    print("\n")
    print("Вариант 1")
    for staff in zoo.staff:
        for animal in zoo.animals:
            try:
                if isinstance(staff, ZooKeeper):
                    staff.feed_animal(animal)
                elif isinstance(staff, Veterinarian):
                    staff.heal_animal(animal)
            except Exception as e:
                print(f"Ошибка! {staff.name} не может взаимодействовать с {animal.name}: {str(e)}")

    # Вариант 2: Вывод в таблице
    print("\n")
    print("Вариант 2: Таблица взаимодействий")
    print(f"\n{'Сотрудник':<15} | {'Должность':<12} | {'Животное':<10} | {'Тип':<10} | Действие")
    print("-" * 60)
    for staff in zoo.staff:
        for animal in zoo.animals:
            action = ""
            if isinstance(staff, ZooKeeper):
                action = "Кормление"
                staff.feed_animal(animal)
            elif isinstance(staff, Veterinarian):
                action = "Осмотр"
                staff.heal_animal(animal)

            print(
                f"{staff.name:<15} | {staff.position:<12} | {animal.name:<10} | {animal.__class__.__name__:<10} | {action}")


# Основная программа
if __name__ == "__main__":
    # Создаем зоопарк
    my_zoo = Zoo("Дикий рай")

    # Добавляем животных разных типов
    my_zoo.add_animal(Bird("Кеша", 2, 15))
    my_zoo.add_animal(Mammal("Барсик", 4, "рыжий"))
    my_zoo.add_animal(Reptile("Гена", 5, "крупная чешуя"))


    # Добавляем персонал
    my_zoo.add_staff(ZooKeeper("Иван"))
    my_zoo.add_staff(Veterinarian("Мария"))


    # Показываем информацию о зоопарке
    my_zoo.show_animals()
    my_zoo.show_staff()

    # Демонстрируем полиморфизм
    animal_sound(my_zoo.animals)

    # Проверяем все виды взаимодействий
    check_all_interactions(my_zoo)

    # Сохраняем и загружаем данные
    my_zoo.save_to_file("zoo_data.json")
    loaded_zoo = Zoo.load_from_file("zoo_data.json")
    loaded_zoo.show_animals()
    loaded_zoo.show_staff()