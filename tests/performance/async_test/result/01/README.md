# Profile

Test executed on Guará commit 0f96115cba2df18647ea2bd8f9f5f304610b7681

## Host configuration
```
uname --all
Linux douglas 5.4.0-204-generic #224-Ubuntu SMP Thu Dec 5 13:38:28 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
```

## Setup
- Close all apps leaving just the terminal open

## Script
- script_1.py

## Load

- Rump up: 0
- Execution time: `60 * 5 SECONDS`
- Pacing: 0
- Think Time: 0
- Rump down: 0

Description
- Ramp up: the elapsed time seting up the resources before the main execution
- Execution time: is the elapsed time the test was executed
- Pacing: the sleep time between on iteration to other
- Think time: the sleep time between one transaction to other
- Rump down: the elapsed time disposing the resources raised in the rump up

## Execution

```
python -m pytest -k test_performance_async.py
```

## Analysis

![alt text](image.png)

- All metrics are stable (no increasing) during the tests
- There are some CPU spikes, but they are constant during the execution