from pyscript import document
from guara.transaction import AbstractTransaction, Application
from guara import it


class ToDoPrototype:
    def __init__(self):
        """Internal storage to store the tasks in memory"""
        self._tasks = []

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, task):
        self._tasks.append(task)


class Add(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    def do(self, task: str):
        if not task.strip():
            raise ValueError("Invalid task")
        self._driver.tasks.append(task)
        return self._driver.tasks


class Remove(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    def do(self, task):
        self._driver.tasks.remove(task)
        return self._driver.tasks


class ListTasks(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    def do(self):
        return self._driver.tasks


class PrintDict(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    def do(self):
        result = {}
        count = 1
        for task in self._driver.tasks:
            result[str(count)] = task
            count += 1
        return result


class GetBy(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    def do(self, index):
        try:
            return self._driver.tasks[index]
        except IndexError:
            return "No task"


# For front-end
todo_prototype = ToDoPrototype()
app = Application(todo_prototype)

add = Add(todo_prototype)
remove = Remove(todo_prototype)
list = ListTasks(todo_prototype)
print_dict = PrintDict(todo_prototype)
get_by = GetBy(todo_prototype)


def add_task(event):
    try:
        task = document.querySelector("#task").value
        # add.do(task)
        app.at(Add, task=task).asserts(it.IsEqualTo, list.do())
        document.querySelector("#output").innerText = f"Task '{task}' added"
    except Exception as e:
        document.querySelector("#output").innerText = str(e)


def remove_task(event):
    task = document.querySelector("#task").value
    remove.do(task)
    document.querySelector("#output").innerText = f"Task '{task}' removed"


def print_task_dict(event):
    document.querySelector("#output").innerText = print_dict.do()


def list_tasks(event):
    document.querySelector("#output").innerText = list.do()


def get_task(event):
    value = document.querySelector("#index-input").value
    if not value:
        value = 0
    index = int(value) - 1
    document.querySelector("#output").innerText = str(get_by.do(index=index))
