# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from tests.performance.async_test.app import transactions
from guara.asynchronous.transaction import Application
from guara.asynchronous import it


class App:
    def __init__(self):
        self._todo = Application(transactions.ToDoPrototype())

    async def run(self):
        task_1 = "buy banana"
        task_2 = "buy apple"
        task_3 = "buy orange"
        await self._todo.at(transactions.Add, task=task_1).asserts(it.IsEqualTo, [task_1]).perform()
        await self._todo.at(transactions.Add, task=task_2).perform()
        await self._todo.at(transactions.Add, task=task_3).perform()

        (await self._todo.at(transactions.ListTasks).asserts(it.Contains, task_1).perform())

        await self._todo.at(transactions.Remove, task=task_1).perform()
        await self._todo.at(transactions.Remove, task=task_2).perform()
        await self._todo.at(transactions.Remove, task=task_3).perform()
