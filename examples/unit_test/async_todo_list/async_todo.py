# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that will have the class where the tasks will be
stored.
"""

from typing import List, Dict


class AsyncToDo:
    def __init__(self):
        """
        Initializing the class.
        """
        self._tasks: List[str] = []
        """
        The list of the tasks
        """

    async def add_task(self, task: str) -> List[str]:
        """
        Adding task.

        Args:
            task: (str): The task to be added.

        Returns:
            (List[str])
        """
        self._tasks.append(task)
        return self._tasks

    async def remove_task(self, task) -> List[str]:
        """
        Removing task.

        Args:
            task: (str): The task to be removed.

        Returns:
            (List[str])
        """
        self._tasks.remove(task)
        return self._tasks

    async def list_tasks(self) -> List[str]:
        """
        Retrieving the list of the tasks.

        Returns:
            (List[str])
        """
        return self._tasks

    async def get_by_index(self, index: int) -> str:
        """
        Retrieving a task at a specific index.

        Args:
            index: (int): The index of the task.

        Returns:
            (str)
        """
        return self._tasks[index]

    async def to_dict(self) -> Dict[str, str]:
        """
        Converting the list of tasks into an object.

        Returns:
            (Dict[str, str])
        """
        result: Dict[str, str] = {}
        for index in range(0, len(self._tasks), 1):
            result[str(index + 1)] = self._tasks[index]
        return result
