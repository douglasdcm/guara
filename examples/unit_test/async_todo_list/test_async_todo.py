import pytest_asyncio
import pytest
from examples.unit_test.async_todo_list.async_todo import AsyncToDo
from examples.unit_test.async_todo_list import operations
from guara.asynchronous.transaction import Application
from guara.asynchronous import it


class TestAsyncToDo:
    @pytest_asyncio.fixture(loop_scope="function")
    async def setup_test(self):
        self._todo = Application(AsyncToDo())

    @pytest.mark.asyncio
    async def test_async_add_task(self, setup_test):
        task = "buy cheese"
        expected = [task]
        await self._todo.at(operations.Add, task=task).asserts(
            it.IsEqualTo, expected
        ).perform()

    @pytest.mark.asyncio
    async def test_async_remove_task(self, setup_test):
        task = "buy cheese"
        expected = []
        await self._todo.at(operations.Add, task=task).perform()
        await self._todo.at(operations.Remove, task=task).asserts(
            it.IsEqualTo, expected
        ).perform()

    @pytest.mark.asyncio
    async def test_async_list_tasks(self, setup_test):
        task = "any task"
        expected = [task]
        await self._todo.at(operations.Add, task=task).perform()
        await self._todo.at(operations.ListTasks).asserts(
            it.IsEqualTo, expected
        ).perform()

    @pytest.mark.asyncio
    async def test_async_list_tasks_many_assertions(self, setup_test):
        TASK = "any task"
        OTHER_TASK = "other task"
        expected = [TASK]
        await self._todo.at(operations.Add, task=TASK).perform()
        await self._todo.at(operations.ListTasks).asserts(
            it.IsEqualTo, expected
        ).perform()
        await self._todo.at(operations.ListTasks).asserts(
            it.IsNotEqualTo, [OTHER_TASK]
        ).perform()
        await self._todo.at(operations.ListTasks).asserts(it.Contains, TASK).perform()
        await self._todo.at(operations.ListTasks).asserts(
            it.DoesNotContain, OTHER_TASK
        ).perform()
