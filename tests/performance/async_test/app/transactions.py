# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.asynchronous.transaction import AbstractTransaction


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

    async def do(self, task: str):
        if not task.strip():
            raise ValueError("Invalid task")
        self._driver.tasks.append(task)
        return self._driver.tasks


class Remove(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    async def do(self, task):
        try:
            self._driver.tasks.remove(task)
            return self._driver.tasks
        except ValueError:
            return f"Taks '{task}' not found"


class ListTasks(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    async def do(self):
        return self._driver.tasks


class PrintDict(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDoPrototype

    async def do(self):
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

    async def do(self, index):
        try:
            return self._driver.tasks[index]
        except IndexError:
            return "No task"
