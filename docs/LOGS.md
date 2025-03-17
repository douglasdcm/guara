# Execution

It is recommended to use `pytest`

```
# Executes reporting the complete log
python -m pytest
```
Options of logging can be customized through your `pytest.ini` file. Refer to [Pytest documentaion](https://docs.pytest.org/en/stable/how-to/logging.html).
```
# pytest.ini
[pytest]
log_format = %(asctime)s.%(msecs)03d %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
log_cli = true
log_cli_level = INFO
asyncio_default_fixture_loop_scope="function"
```
The output is similar to it
```
--------------------------------------------------------------- live log setup ---------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'OpenApp'
2025-01-09 06:39:41 INFO  url: file:////...sample.html
2025-01-09 06:39:41 INFO  window_width: 1094
2025-01-09 06:39:41 INFO  window_height: 765
2025-01-09 06:39:41 INFO  implicitly_wait: 0.5
2025-01-09 06:39:41 INFO Assertion 'IsEqualTo'
2025-01-09 06:39:41 INFO  actual:   'Sample page'
2025-01-09 06:39:41 INFO  expected: 'Sample page'
--------------------------------------------------------------- live log call ----------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'SubmitText'
2025-01-09 06:39:41 INFO  text: cheese
2025-01-09 06:39:41 INFO Assertion 'IsEqualTo'
2025-01-09 06:39:41 INFO  actual:   'It works! cheese!'
2025-01-09 06:39:41 INFO  expected: 'It works! cheese!'
2025-01-09 06:39:41 INFO Transaction 'SubmitText'
2025-01-09 06:39:41 INFO  text: cheese
2025-01-09 06:39:41 INFO Assertion 'IsNotEqualTo'
2025-01-09 06:39:41 INFO  actual:   'It works! cheesecheese!'
2025-01-09 06:39:41 INFO  expected: 'Any'
PASSED                                                                                                                                 [100%]
------------------------------------------------------------- live log teardown --------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'CloseApp'
```

The logs can be viewed using [Allure reporter](https://pypi.org/project/allure-pytest/)
