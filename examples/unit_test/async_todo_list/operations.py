# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that have all of the transactions needed for the
To-Do List.
"""

from guara.asynchronous.transaction import AbstractTransaction
from typing import List, Dict


class Add(AbstractTransaction):
    """
    The addition transaction
    """

    async def do(self, task: str) -> List[str]:
        return await self._driver.add_task(task)


class Remove(AbstractTransaction):
    """
    The removal transaction.
    """

    async def do(self, task: str) -> List[str]:
        return await self._driver.remove_task(task)


class ListTasks(AbstractTransaction):
    """
    The listing transaction
    """

    async def do(self) -> List[str]:
        return await self._driver.list_tasks()


class PrintDict(AbstractTransaction):
    """
    The array to object conversion transaction.
    """

    async def do(self) -> Dict[str, str]:
        return await self._driver.to_dict()


class GetBy(AbstractTransaction):
    """
    The transaction which will get a specific task by its index.
    """

    async def do(self, index: int) -> str:
        return await self._driver.get_by_index(index)
