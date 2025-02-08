# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from examples.unit_test.todo_list.todo import ToDo


class Add(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDo

    def do(self, task):
        return self._driver.add_task(task)


class Remove(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDo

    def do(self, task):
        return self._driver.remove_task(task)


class ListTasks(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDo

    def do(self):
        return self._driver.list_tasks()


class PrintDict(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDo

    def do(self):
        return self._driver.to_dict()


class GetBy(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: ToDo

    def do(self, index):
        return self._driver.get_by_index(index)
