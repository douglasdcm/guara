import unittest
from examples.unit_test.todo_list.todo import ToDo
from examples.unit_test.todo_list import operations
from guara.transaction import Application
from guara import it


class TestToDoNoseTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()  # run all tests
