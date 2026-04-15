# Logs

The framework has a default log that reports
* the transaction being executed, its parameters names and values
* the assertion names, its actual (received) and expected values
* reverted transation, if any
* erros in transactions and assertions

**Note**: the value of parameters with `secret` in their names is hidden in the logs by default

```bash
2026-04-15 01:19:41.635 INFO Running transaction 'Login'
2026-04-15 01:19:41.635 INFO  With paramater 'my_secret' set to '*****'
```

## Log of successful operations

```bash
2025-01-09 06:39:41 INFO Running transaction 'OpenApp'
2025-01-09 06:39:41 INFO  With parameter 'url' set to 'file:////...sample.html'
2025-01-09 06:39:41 INFO  With parameter window_width set to '1094'
2025-01-09 06:39:41 INFO  With parameter window_height set to '765'
2025-01-09 06:39:41 INFO  With parameter implicitly_wait set to '0.5'
2025-01-09 06:39:41 INFO Asserting 'IsEqualTo'
2025-01-09 06:39:41 INFO  Actual  : 'Sample page'
2025-01-09 06:39:41 INFO  Expected: 'Sample page'
2025-01-09 06:39:41 INFO Running transaction 'SubmitText'
2025-01-09 06:39:41 INFO  With parameter 'text' set to 'cheese'
2025-01-09 06:39:41 INFO Asserting 'IsEqualTo'
2025-01-09 06:39:41 INFO  Actual  : 'It works! cheese!'
2025-01-09 06:39:41 INFO  Expected: 'It works! cheese!'
2025-01-09 06:39:41 INFO Running transaction 'SubmitText'
2025-01-09 06:39:41 INFO  With parameter 'text' set to 'cheese'
2025-01-09 06:39:41 INFO Asserting 'IsNotEqualTo'
2025-01-09 06:39:41 INFO  Actual  : 'It works! cheesecheese!'
2025-01-09 06:39:41 INFO  Expected: 'Any'
2025-01-09 06:39:41 INFO Running transaction 'CloseApp'
```

## Log of failed operations

```bash
2026-04-15 01:24:13.379 ERROR Transaction 'HasNotStudent' failed on attempt 0
2026-04-15 01:24:13.379 ERROR Student exists
Traceback (most recent call last):
  File "~/guara/transaction.py", line 87, in at
    self._result = self._transaction.act(**kwargs)
  File "~/guara/abstract_transaction.py", line 60, in act
    return self.do(**kwargs)
  File "~/examples/domain_driven_design/transactions.py", line 200, in do
    raise Exception("Student exists")
Exception: Student exists
```


## Logs in test execution
It is recommended to use `pytest`

```bash
# Executes reporting the complete log
python -m pytest
```
Options of logging can be customized through your `pytest.ini` file. Refer to [Pytest documentaion](https://docs.pytest.org/en/stable/how-to/logging.html).

```ini
# pytest.ini
[pytest]
log_format = %(asctime)s.%(msecs)03d %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
log_cli = true
log_cli_level = INFO
asyncio_default_fixture_loop_scope="function"
```

The logs can be viewed using [Allure reporter](https://pypi.org/project/allure-pytest/)
