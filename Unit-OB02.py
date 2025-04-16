# Разработай систему управления учетными записями пользователей для небольшой компании.
# Компания разделяет сотрудников на обычных работников и администраторов.
# У каждого сотрудника есть уникальный идентификатор (ID), имя и уровень доступа.
# Администраторы, помимо обычных данных пользователей, имеют дополнительный уровень доступа и могут
# добавлять или удалять пользователя из системы.
#
# Требования:
#
# 1.Класс `User*: Этот класс должен инкапсулировать данные о пользователе: ID, имя и
# уровень доступа ('user' для обычных сотрудников).
#
# 2.Класс `Admin`: Этот класс должен наследоваться от класса `User`.
# Добавь дополнительный атрибут уровня доступа, специфичный для администраторов ('admin').
# Класс должен также содержать методы `add_user` и `remove_user`, которые позволяют добавлять и удалять пользователей
# из списка (представь, что это просто список экземпляров `User`).
#
# 3.Инкапсуляция данных: Убедись, что атрибуты классов защищены от прямого доступа и модификации снаружи.
# Предоставь доступ к необходимым атрибутам через методы (например, get и set методы).



class User:
    def __init__(self, user_id, name):
        self.__id = user_id
        self.__name = name
        self._access_level = 'user'

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name

    def get_access_level(self):
        return self._access_level


class Admin(User):
    __users_list = []

    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self._access_level = 'admin'

    def add_user(self, user):
        if isinstance(user, User):
            Admin.__users_list.append(user)
            print(f"Пользователь {user.get_name()} (ID: {user.get_id()}) добавлен.")
        else:
            print("Ошибка: можно добавлять только объекты класса User.")

    def remove_user(self, user_id):
        for user in Admin.__users_list:
            if user.get_id() == user_id:
                Admin.__users_list.remove(user)
                print(f"Пользователь с ID {user_id} удален.")
                return
        print(f"Ошибка: пользователь с ID {user_id} не найден.")

    @classmethod
    def show_all_users(cls):
        print("\nСписок всех пользователей:")
        for user in cls.__users_list:
            access_type = 'Администратор' if user.get_access_level() == 'admin' else 'Пользователь'
            print(f"ID: {user.get_id()}, Имя: {user.get_name()}, Тип: {access_type}")


# Пример использования
if __name__ == "__main__":
    # Создаем администратора
    admin = Admin(1, "Иван Петров")

    # Создаем обычных пользователей
    user1 = User(2, "Мария Семенова")
    user2 = User(3, "Алексей Иванов")

    # Администратор добавляет пользователей
    admin.add_user(user1)
    admin.add_user(user2)
    admin.add_user(admin)  # Администратор может добавить себя

    # Показываем всех пользователей
    Admin.show_all_users()

    # Пытаемся добавить неверный тип данных
    admin.add_user("Некорректный пользователь")

    # Меняем имя пользователю
    user1.set_name("Мария Сидорова")
    print(f"\nНовое имя пользователя ID 2: {user1.get_name()}")

    # Пытаемся удалить несуществующего пользователя
    admin.remove_user(99)

    # Удаляем существующего пользователя
    admin.remove_user(2)

    # Показываем обновленный список
    Admin.show_all_users()