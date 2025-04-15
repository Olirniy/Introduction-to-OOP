# Менеджер задач
# Задача: Создай класс `Task`, который позволяет управлять задачами (делами).
# У задачи должны быть атрибуты: описание задачи, срок выполнения и статус (выполнено/не выполнено).
# Реализуй функцию для добавления задач, отметки выполненных задач и вывода списка текущих (не выполненных) задач.

class Task:
    def __init__(self, description, due_date):
        self.description = description
        self.due_date = due_date
        self.completed = False

    def mark_as_completed(self):
        self.completed = True


    def __str__(self):
        status = "Выполнено" if self.completed else "Не выполнено"
        return f"Задача: {self.description}, Срок: {self.due_date}, Статус: {status}"



class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date):
        new_task = Task(description, due_date)
        self.tasks.append(new_task)
        print(f"Задача добавлена: {description}")

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_as_completed()
            print(f"Задача отмечена как выполненная: {self.tasks[task_index].description}")
        else:
            print("Ошибка: неверный индекс задачи")

    def show_current_tasks(self):
        current_tasks = [task for task in self.tasks if not task.completed]
        if not current_tasks:
            print("Нет текущих задач")
        else:
            print("\nТекущие задачи (не выполненные):")
            for i, task in enumerate(current_tasks):
                print(f"{i}. {task}")

    def show_all_tasks(self):
        if not self.tasks:
            print("Нет задач")
        else:
            print("\nВсе задачи:")
            for i, task in enumerate(self.tasks):
                print(f"{i}. {task}")


# Пример использования
if __name__ == "__main__":
    manager = TaskManager()

    while True:
        print("\nМенеджер задач")
        print("1. Добавить задачу")
        print("2. Отметить задачу как выполненную")
        print("3. Показать текущие задачи")
        print("4. Показать все задачи")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            description = input("Введите описание задачи: ")
            due_date = input("Введите срок выполнения: ")
            manager.add_task(description, due_date)
        elif choice == "2":
            manager.show_all_tasks()
            task_index = int(input("Введите номер задачи для отметки как выполненной: "))
            manager.complete_task(task_index)
        elif choice == "3":
            manager.show_current_tasks()
        elif choice == "4":
            manager.show_all_tasks()
        elif choice == "5":
            print("Выход из программы")
            break
        else:
            print("Неверный ввод, попробуйте снова")