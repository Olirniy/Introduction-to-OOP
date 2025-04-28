# Задание: Применение Принципа Открытости/Закрытости (Open/Closed Principle) в Разработке Простой Игры

# Задача: Разработать простую игру, где игрок может использовать различные типы оружия для борьбы с монстрами.

# Исходные данные:
# - Есть класс `Fighter`, представляющий бойца.
# - Есть класс `Monster`, представляющий монстра.
# - Игрок управляет бойцом и может выбирать для него одно из вооружений для боя.

# Требования к заданию:
# - Программа должна демонстрировать применение принципа открытости/закрытости:
# новые типы оружия можно легко добавлять, не изменяя существующие классы бойцов и механизм боя.
# - Программа должна выводить результат боя в консоль.

# Пример результата:

# Боец выбирает меч.
# Боец наносит удар мечом.
# Монстр побежден!

# Боец выбирает лук.
# Боец наносит удар из лука.
# Монстр побежден!


from abc import ABC, abstractmethod


# Шаг 1: Абстрактный класс оружия
class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass


# Шаг 2: Конкретные реализации оружия
class Sword(Weapon):
    def attack(self):
        return "наносит удар мечом"


class Bow(Weapon):
    def attack(self):
        return "стреляет из лука"


class Axe(Weapon):
    def attack(self):
        return "рубит топором"


# Класс бойца
class Fighter:
    def __init__(self, name):
        self.name = name
        self.weapon = None  # Изначально оружия нет

    def change_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"{self.name} выбирает {weapon.__class__.__name__.lower()}.")

    def attack(self):
        if self.weapon:
            action = self.weapon.attack()
            print(f"{self.name} {action}.")
            return True
        else:
            print(f"{self.name} не имеет оружия!")
            return False


# Класс монстра
class Monster:
    def __init__(self, name):
        self.name = name
        self.is_defeated = False

    def defeat(self):
        self.is_defeated = True
        print(f"{self.name} побежден!\n")


# Механизм боя
def battle(fighter: Fighter, monster: Monster):
    if fighter.attack():
        monster.defeat()


# Демонстрация
if __name__ == "__main__":
    hero = Fighter("Боец")
    monster = Monster("Монстр")

    # Бой с разным оружием
    hero.change_weapon(Sword())
    battle(hero, monster)

    hero.change_weapon(Bow())
    battle(hero, monster)

    # Добавляем новое оружие без изменения существующего кода
    hero.change_weapon(Axe())
    battle(hero, monster)