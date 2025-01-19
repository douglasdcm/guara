from guara.asynchronous.transaction import AbstractTransaction
from examples.unit_test.async_todo_list.async_todo import AsyncToDo


class Add(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: AsyncToDo

    async def do(self, task):
        return await self._driver.add_task(task)


class Remove(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: AsyncToDo

    async def do(self, task):
        return await self._driver.remove_task(task)


class ListTasks(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: AsyncToDo

    async def do(self):
        return await self._driver.list_tasks()


class PrintDict(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: AsyncToDo

    async def do(self):
        return await self._driver.to_dict()


class GetBy(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: AsyncToDo

    async def do(self, index):
        return await self._driver.get_by_index(index)
