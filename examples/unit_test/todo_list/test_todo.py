# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from unittest import TestCase
from examples.unit_test.todo_list.todo import ToDo
from examples.unit_test.todo_list import operations
from guara.transaction import Application
from guara import it


class TestToDo:
    def setup_method(self, method):
        self._todo = Application(ToDo())

    def test_add_task(self):
        task = "buy cheese"
        expected = [task]
        self._todo.at(operations.Add, task=task).asserts(it.IsEqualTo, expected)

    def test_remove_task(self):
        task = "buy cheese"
        expected = []
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.Remove, task=task).asserts(it.IsEqualTo, expected)

    def test_list_tasks(self):
        task = "any task"
        expected = [task]
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.ListTasks).asserts(it.IsEqualTo, expected)

    def test_list_tasks_many_assertions(self):
        task = "buy cheese"
        task_2 = "buy apple"
        task_3 = "buy orange"
        expected = [task, task_2, task_3]
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.Add, task=task_2)
        self._todo.at(operations.Add, task=task_3)

        sub_set = [task, task_3]
        result = self._todo.at(operations.ListTasks).result
        it.HasSubset().validates(result, sub_set)
        it.IsSortedAs().validates(result, expected)

        key_value = {"1": task}
        self._todo.at(operations.PrintDict).asserts(it.HasKeyValue, key_value)

        task = "buy watermelon"
        index = 3
        pattern = "(.*)melon"
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.GetBy, index=index).asserts(it.MatchesRegex, pattern)


class TestToTestCase(TestCase):
    def setUp(self):
        self._todo = Application(ToDo())

    def test_list_tasks_many_assertions(self):
        task = "buy cheese"
        task_2 = "buy apple"
        task_3 = "buy orange"
        expected = [task, task_2, task_3]
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.Add, task=task_2)
        self._todo.at(operations.Add, task=task_3)

        sub_set = [task, task_3]
        result = self._todo.at(operations.ListTasks).result
        it.HasSubset().validates(result, sub_set)
        it.IsSortedAs().validates(result, expected)

        key_value = {"1": task}
        self._todo.at(operations.PrintDict).asserts(it.HasKeyValue, key_value)

        task = "buy watermelon"
        index = 3
        pattern = "(.*)melon"
        self._todo.at(operations.Add, task=task)
        self._todo.at(operations.GetBy, index=index).asserts(it.MatchesRegex, pattern)
