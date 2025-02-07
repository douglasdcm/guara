# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from tests.performance.sync_test.app import transactions
from guara.transaction import Application
from guara import it


class App:
    def __init__(self):
        self._todo = Application(transactions.ToDoPrototype())

    def run(self):
        task_1 = "buy banana"
        task_2 = "buy apple"
        task_3 = "buy orange"
        expected = [task_1, task_2, task_3]
        self._todo.at(transactions.Add, task=task_1).asserts(it.IsEqualTo, [task_1])
        self._todo.at(transactions.Add, task=task_2)
        self._todo.at(transactions.Add, task=task_3)

        sub_set = [task_1, task_3]
        result = self._todo.at(transactions.ListTasks).result
        it.HasSubset().validates(result, sub_set)
        it.IsSortedAs().validates(result, expected)

        key_value = {"1": task_1}
        self._todo.at(transactions.PrintDict).asserts(it.HasKeyValue, key_value)

        task_4 = "buy watermelon"
        index = 3
        pattern = "(.*)melon"
        self._todo.at(transactions.Add, task=task_4)
        self._todo.at(transactions.GetBy, index=index).asserts(it.MatchesRegex, pattern)

        self._todo.at(transactions.Remove, task=task_1)
        self._todo.at(transactions.Remove, task=task_2)
        self._todo.at(transactions.Remove, task=task_3)
        self._todo.at(transactions.Remove, task=task_4)
