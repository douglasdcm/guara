# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The test script for testing asynchronuous transactions on a
To-Do List.
"""

from examples.unit_test.async_todo_list.async_todo import AsyncToDo
from guara.asynchronous.transaction import Application
from pytest_asyncio import fixture
from typing import List, Coroutine, Any
from examples.unit_test.async_todo_list.operations import Add, Remove, ListTasks
from guara.asynchronous.it import IsEqualTo, IsNotEqualTo, Contains, DoesNotContain
from pytest import mark


@mark.skip("Not work with python3.6")
class TestAsyncToDo:
    """
    The test class for asynchronuous To-Do List.
    """

    @fixture(loop_scope="function")
    async def setup_test(self) -> None:
        """
        Setting up for the test.

        Returns:
            (None)
        """
        self._todo: Application = Application(AsyncToDo())

    @mark.asyncio
    async def test_async_add_task(self, setup_test: Coroutine[Any, Any, None]) -> None:
        """
        Testing the add task transaction.

        Args:
            setup_test: (Coroutine[Any, Any, None]): Setting up for the test.

        Returns:
            (None)
        """
        task: str = "buy cheese"
        expected: List[str] = [task]
        await self._todo.at(transaction=Add, task=task).asserts(IsEqualTo, expected).perform()

    @mark.asyncio
    async def test_async_remove_task(self, setup_test: Coroutine[Any, Any, None]) -> None:
        """
        Testing the remove task transaction.

        Args:
            setup_test: (Coroutine[Any, Any, None]): Setting up for the test.

        Returns:
            (None)
        """
        task: str = "buy cheese"
        expected: List[str] = []
        await self._todo.at(transaction=Add, task=task).perform()
        await self._todo.at(transaction=Remove, task=task).asserts(IsEqualTo, expected).perform()

    @mark.asyncio
    async def test_async_list_tasks(self, setup_test: Coroutine[Any, Any, None]) -> None:
        """
        Testing the listing of the tasks transaction.

        Args:
            setup_test: (Coroutine[Any, Any, None]): Setting up for the test.

        Returns:
            (None)
        """
        task: str = "any task"
        expected: List[str] = [task]
        await self._todo.at(transaction=Add, task=task).perform()
        await self._todo.at(ListTasks).asserts(IsEqualTo, expected).perform()

    @mark.asyncio
    async def test_async_list_tasks_many_assertions(
        self, setup_test: Coroutine[Any, Any, None]
    ) -> None:
        """
        Testing the listing transaction.

        Args:
            setup_test: (Coroutine[Any, Any, None]): Setting up for the test.

        Returns:
            (None)
        """
        task: str = "any task"
        other_task: str = "other task"
        expected: List[str] = [task]
        other_expected: List[str] = [other_task]
        await self._todo.at(transaction=Add, task=task).perform()
        await self._todo.at(ListTasks).asserts(IsEqualTo, expected).perform()
        await self._todo.at(ListTasks).asserts(IsNotEqualTo, other_expected).perform()
        await self._todo.at(ListTasks).asserts(Contains, task).perform()
        await self._todo.at(ListTasks).asserts(DoesNotContain, other_task).perform()
