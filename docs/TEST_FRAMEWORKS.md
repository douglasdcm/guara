# Introduction
Guara can e executed with many test frameworks other than `pytest`, for example [`unitest`](https://docs.python.org/3.6/library/unittest.html) and [`testify`](https://github.com/Yelp/Testify). Here are the command examples and their outputs.

## unittest

```shell
python -m unittest -v
```

Output

```shell
test_add_returns_3_when_adding_1_and_2 (examples.unit_test.calculator.test_calculator.TestCalculatorTestCase.test_add_returns_3_when_adding_1_and_2) ... 2025-01-15 23:11:52.585 INFO Transaction 'operations.Add'
2025-01-15 23:11:52.585 INFO  a: 1
2025-01-15 23:11:52.585 INFO  b: 2
2025-01-15 23:11:52.585 INFO Assertion 'IsEqualTo'
2025-01-15 23:11:52.585 INFO  actual:   '3'
2025-01-15 23:11:52.585 INFO  expected: '3'
ok
test_list_tasks_many_assertions (examples.unit_test.todo_list.test_todo.TestToTestCase.test_list_tasks_many_assertions) ... 2025-01-15 23:11:52.585 INFO Transaction 'operations.Add'
2025-01-15 23:11:52.585 INFO  task: buy cheese
2025-01-15 23:11:52.585 INFO Transaction 'operations.Add'
2025-01-15 23:11:52.585 INFO  task: buy apple
2025-01-15 23:11:52.586 INFO Transaction 'operations.Add'
2025-01-15 23:11:52.586 INFO  task: buy orange
2025-01-15 23:11:52.586 INFO Transaction 'operations.ListTasks'
2025-01-15 23:11:52.586 INFO Assertion 'HasSubset'
2025-01-15 23:11:52.586 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-15 23:11:52.586 INFO  expected: '['buy cheese', 'buy orange']'
2025-01-15 23:11:52.586 INFO Assertion 'IsSortedAs'
2025-01-15 23:11:52.586 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-15 23:11:52.586 INFO  expected: '['buy cheese', 'buy apple', 'buy orange']'
2025-01-15 23:11:52.586 INFO Transaction 'operations.PrintDict'
2025-01-15 23:11:52.586 INFO Assertion 'HasKeyValue'
2025-01-15 23:11:52.586 INFO  actual:   '{'1': 'buy cheese', '2': 'buy apple', '3': 'buy orange'}'
2025-01-15 23:11:52.586 INFO  expected: '{'1': 'buy cheese'}'
2025-01-15 23:11:52.586 INFO Transaction 'operations.Add'
2025-01-15 23:11:52.586 INFO  task: buy watermelon
2025-01-15 23:11:52.586 INFO Transaction 'operations.GetBy'
2025-01-15 23:11:52.586 INFO  index: 3
2025-01-15 23:11:52.586 INFO Assertion 'MatchesRegex'
2025-01-15 23:11:52.587 INFO  actual:   'buy watermelon'
2025-01-15 23:11:52.587 INFO  expected: '(.*)melon'
ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK

```

## Testify
```shell
testify examples/unit_test/calculator/test_calculator.py -v
```

Output

```shell
examples.unit_test.calculator.test_calculator TestifiedTestCalculatorTestCase.test_add_returns_3_when_adding_1_and_2 ... 2025-01-15 23:34:17.251 INFO Transaction 'operations.Add'
2025-01-15 23:34:17.251 INFO  a: 1
2025-01-15 23:34:17.251 INFO  b: 2
2025-01-15 23:34:17.251 INFO Assertion 'IsEqualTo'
2025-01-15 23:34:17.251 INFO  actual:   '3'
2025-01-15 23:34:17.251 INFO  expected: '3'
ok in 0.00s
examples.unit_test.calculator.test_calculator TestCalculatorTestify.test_add_returns_3_when_adding_1_and_2 ... 2025-01-15 23:34:17.252 INFO Transaction 'operations.Add'
2025-01-15 23:34:17.252 INFO  a: 1
2025-01-15 23:34:17.252 INFO  b: 2
2025-01-15 23:34:17.252 INFO Assertion 'IsEqualTo'
2025-01-15 23:34:17.252 INFO  actual:   '3'
2025-01-15 23:34:17.252 INFO  expected: '3'
ok in 0.00s

PASSED.  2 tests / 2 cases: 2 passed, 0 failed.  (Total test time 0.00s)
```

## [Nose](https://pypi.org/project/nose/)

Not working as there is an associated [issue](https://github.com/nose-devs/nose/issues/1127#issuecomment-2594272171) in Nose with Python 3.10+

## [stestr](https://github.com/mtreinish/stestr)

```shell
stestr run -v
```

Output

```shell
initialize_app
prepare_to_run_command Run
2025-01-16 00:26:33.648 INFO Transaction 'operations.Add'
2025-01-16 00:26:33.648 INFO  a: 1
2025-01-16 00:26:33.648 INFO  b: 2
2025-01-16 00:26:33.648 INFO Assertion 'IsEqualTo'
2025-01-16 00:26:33.648 INFO  actual:   '3'
2025-01-16 00:26:33.648 INFO  expected: '3'
{1} examples.unit_test.calculator.test_calculator.TestCalculatorTestCase.test_add_returns_3_when_adding_1_and_2 [0.000655s] ... ok
2025-01-16 00:26:33.651 INFO Transaction 'operations.Add'
2025-01-16 00:26:33.651 INFO  task: buy cheese
2025-01-16 00:26:33.651 INFO Transaction 'operations.Add'
2025-01-16 00:26:33.651 INFO  task: buy apple
2025-01-16 00:26:33.651 INFO Transaction 'operations.Add'
2025-01-16 00:26:33.652 INFO  task: buy orange
2025-01-16 00:26:33.652 INFO Transaction 'operations.ListTasks'
2025-01-16 00:26:33.652 INFO Assertion 'HasSubset'
2025-01-16 00:26:33.652 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:26:33.652 INFO  expected: '['buy cheese', 'buy orange']'
2025-01-16 00:26:33.652 INFO Assertion 'IsSortedAs'
2025-01-16 00:26:33.652 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:26:33.652 INFO  expected: '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:26:33.652 INFO Transaction 'operations.PrintDict'
2025-01-16 00:26:33.652 INFO Assertion 'HasKeyValue'
2025-01-16 00:26:33.652 INFO  actual:   '{'1': 'buy cheese', '2': 'buy apple', '3': 'buy orange'}'
2025-01-16 00:26:33.652 INFO  expected: '{'1': 'buy cheese'}'
2025-01-16 00:26:33.652 INFO Transaction 'operations.Add'
2025-01-16 00:26:33.652 INFO  task: buy watermelon
2025-01-16 00:26:33.652 INFO Transaction 'operations.GetBy'
2025-01-16 00:26:33.652 INFO  index: 3
2025-01-16 00:26:33.652 INFO Assertion 'MatchesRegex'
2025-01-16 00:26:33.653 INFO  actual:   'buy watermelon'
2025-01-16 00:26:33.653 INFO  expected: '(.*)melon'
{0} examples.unit_test.todo_list.test_todo.TestToTestCase.test_list_tasks_many_assertions [0.001642s] ... ok

======
Totals
======
Ran: 2 tests in 0.0050 sec.
 - Passed: 2
 - Skipped: 0
 - Expected Fail: 0
 - Unexpected Success: 0
 - Failed: 0
Sum of execute time for each test: 0.0023 sec.

==============
Worker Balance
==============
 - Worker 0 (1 tests) => 0:00:00.001642
 - Worker 1 (1 tests) => 0:00:00.000655
clean_up Run

```

## [Green](https://github.com/CleanCut/green)

```shell
green -vvv
```

Output

```
Green 4.0.2, Coverage 7.6.10, Python 3.11.9

examples.unit_test.calculator.test_calculator
  TestCalculatorTestCase
    test_add_returns_3_when_adding_1_and_22025-01-16 00:33:45.281 INFO Transaction 'operations.Add'
2025-01-16 00:33:45.282 INFO  a: 1
2025-01-16 00:33:45.282 INFO  b: 2
2025-01-16 00:33:45.282 INFO Assertion 'IsEqualTo'
2025-01-16 00:33:45.282 INFO  actual:   '3'
2025-01-16 00:33:45.282 INFO  expected: '3'
2025-01-16 00:33:45.283 INFO Transaction 'operations.Add'
2025-01-16 00:33:45.283 INFO  task: buy cheese
.   test_add_returns_3_when_adding_1_and_2
2025-01-16 00:33:45.283 INFO Transaction 'operations.Add'
2025-01-16 00:33:45.283 INFO  task: buy apple
2025-01-16 00:33:45.283 INFO Transaction 'operations.Add'
2025-01-16 00:33:45.284 INFO  task: buy orange
examples.unit_test.todo_list.test_todo
  TestToTestCase
    test_list_tasks_many_assertions2025-01-16 00:33:45.284 INFO Transaction 'operations.ListTasks'
2025-01-16 00:33:45.284 INFO Assertion 'HasSubset'
2025-01-16 00:33:45.284 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:33:45.284 INFO  expected: '['buy cheese', 'buy orange']'
2025-01-16 00:33:45.284 INFO Assertion 'IsSortedAs'
2025-01-16 00:33:45.284 INFO  actual:   '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:33:45.284 INFO  expected: '['buy cheese', 'buy apple', 'buy orange']'
2025-01-16 00:33:45.284 INFO Transaction 'operations.PrintDict'
2025-01-16 00:33:45.284 INFO Assertion 'HasKeyValue'
2025-01-16 00:33:45.284 INFO  actual:   '{'1': 'buy cheese', '2': 'buy apple', '3': 'buy orange'}'
2025-01-16 00:33:45.285 INFO  expected: '{'1': 'buy cheese'}'
2025-01-16 00:33:45.285 INFO Transaction 'operations.Add'
2025-01-16 00:33:45.285 INFO  task: buy watermelon
2025-01-16 00:33:45.285 INFO Transaction 'operations.GetBy'
2025-01-16 00:33:45.285 INFO  index: 3
2025-01-16 00:33:45.285 INFO Assertion 'MatchesRegex'
2025-01-16 00:33:45.285 INFO  actual:   'buy watermelon'
2025-01-16 00:33:45.285 INFO  expected: '(.*)melon'
.   test_list_tasks_many_assertions

Ran 2 tests in 0.059s using 4 processes

OK (passes=2)
```

## [Coverage](https://coverage.readthedocs.io/en/7.6.10/)

```shell
python -m coverage run -m pytest -k test_calculator.py
```

Output

```shell
/home/douglas/repo/guara/venv/lib/python3.11/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
============================================================ test session starts =============================================================
platform linux -- Python 3.11.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/douglas/repo/guara
configfile: pytest.ini
plugins: playwright-0.6.2, base-url-2.1.0, asyncio-0.25.1, xdist-3.6.1
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None
collected 40 items / 36 deselected / 4 selected

examples/unit_test/calculator/test_calculator.py ....
```

Generate HTML
```
coverage html
```
Output
```
Wrote HTML report to htmlcov/index.html
```
![alt text](images/calculator_coverage.png)