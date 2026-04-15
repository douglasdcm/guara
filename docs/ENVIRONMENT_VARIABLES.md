# Environment Variables

Guará utilizes environment variables to manage global configurations. This allows for flexible test execution across different environments (Local, Staging, CI/CD) without the need to modify the source code.

---

## Available Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DRY_RUN` | Boolean | `false` | When enabled, logs transactions without executing driver actions. |
| `RETRIES_ON_FAILURE` | Integer | `0` | Defines how many times a transaction should retry before failing. |
| `GUARA_DISABLE_LOGS` | Boolean | `false` | When enabled, logs at or bellow the level INFO are suppresed. |

---

## Detailed Configuration

### 1. DRY_RUN
This variable is used to validate the flow of your automation suite without triggering actual browser or device interactions.

* **Usage**: Set to `true` to enable.
* **Effect**: The `is_dry_run()` utility will return `True`. Transactions will skip the `.do()` implementation and a warning will be logged: 
  > `DRY_RUN: True. Dry run is enabled. No action was taken on drivers.`

### 2. RETRIES_ON_FAILURE
This variable enables automatic recovery for flaky transactions. If a transaction fails due to an exception, the `Application.at()` method will catch it and attempt to re-run the transaction.

* **Usage**: Set to a positive integer (e.g., `3`).
* **Effect**: 
    * If a transaction fails, it will be retried up to the specified number of times.
    * If it fails after all retry attempts, the last exception is raised.
    * When active, the log will show: `RETRIES_ON_FAILURE: <value>. Transactions will be retried on failure.`

### 3. GUARA_DISABLE_LOGS
This variable disables logs at or bellow the level INFO. If a transaction fails due to an exception, this logs are still presented.

```bash
2026-04-15 00:23:23.010 ERROR Transaction 'HasNotStudent' failed on attempt 0
2026-04-15 00:23:23.010 ERROR Student exists
Traceback (most recent call last):
  File "~/guara/transaction.py", line 85, in at
    self._result = self._transaction.act(**kwargs)
  File "~/guara/abstract_transaction.py", line 60, in act
    return self.do(**kwargs)
  File "~/guara/examples/domain_driven_design/transactions.py", line 200, in do
    raise Exception("Student exists")
Exception: Student exists
```

* **Usage**: Set to `true` to disable the logs. Any other value enables the log again.
* **Effect**:
    * If no error or exception happens, then no log is presented.
    * If a transaction or assertion fails the errors are logged.

---

## How to Set Environment Variables

Environment variables should be set in your shell or terminal. Guará does **not** use a `.env` file.

### Linux and macOS
```bash
export DRY_RUN=false
export RETRIES_ON_FAILURE=3