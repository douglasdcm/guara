# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class Add(AbstractTransaction):
    def do(self, task):
        return self._driver.add_task(task)


class Remove(AbstractTransaction):
    def do(self, task):
        return self._driver.remove_task(task)


class ListTasks(AbstractTransaction):
    def do(self):
        return self._driver.list_tasks()


class PrintDict(AbstractTransaction):
    def do(self):
        return self._driver.to_dict()


class GetBy(AbstractTransaction):
    def do(self, index):
        return self._driver.get_by_index(index)
