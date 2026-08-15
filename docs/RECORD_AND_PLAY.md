# Execution History

Guará records transaction execution history.

The history provides information about what was executed and supports operational capabilities such as:

* inspecting previous executions;
* dumping execution history;
* filtering transactions;
* replaying previous executions;
* resuming workflows.

Execution history is particularly valuable for workflows involving multiple meaningful transactions.

Conceptually:

```text
Application
    │
    ├── Transaction A
    ├── Transaction B
    ├── Transaction C
    └── Transaction D
             │
             ↓
       Execution History
```

The history becomes an execution record of the application narrative.


## Dump

Execution history can be dumped to a persistent representation.

The dump functionality supports filtering by transaction ID, allowing a specific execution to be isolated from the complete history.

This enables scenarios such as:

```text
Application execution
        ↓
    Dump history
        ↓
Select transaction
        ↓
Replay / inspect
```

Dumping is particularly useful for debugging, operational recovery, and reproducibility.

```json
{
  "application": null,
  "started_at": "2026-08-14T02:33:31.001386+00:00",
  "finished_at": "2026-08-14T02:33:31.030245+00:00",
  "status": "succeeded",
  "transactions": [
    {
      "id": "b1d22238e487488ea370a2762d7cfa17",
      "policy": {
        "retry_on_exceptions": null,
        "abort_on_exceptions": null,
        "continue_on_exceptions": null,
        "rollback_on_failure": null,
        "disable": null,
        "dry_run": null,
        "pacing_time": null,
        "retries_on_failure": null,
        "return_on_dry_run": null
      },
      "name": "ListUsers",
      "module": "bakery.backend.transactions",
      "parameters": {},
      "status": "succeeded",
      "started_at": "2026-08-14T02:33:31.027050+00:00",
      "finished_at": "2026-08-14T02:33:31.029926+00:00",
      "attempts": 1,
      "exception_type": null,
      "exception_message": null,
      "replayable": true
    }
  ]
}
```

## Replay

Guará supports replaying previously dumped executions.

Replay allows a previously recorded execution to be reconstructed without manually reproducing the original workflow.

A replay can target a specific transaction:

```text
Dump
  ↓
transaction_id
  ↓
Replay transaction
```

This is useful when investigating failures or reproducing operational behavior.


## Driver Injection During Replay

Replay supports providing a driver to the `Application`.

This is important for executions whose transactions depend on external infrastructure.

The replay architecture therefore separates:

```text
Execution history
        │
        ├── transaction information
        ├── parameters
        └── execution metadata
                │
                ↓
          Application
                │
                └── Driver
                      ↓
                Infrastructure
```

The driver is an execution dependency and should not be serialized as part of the execution history.

Instead, it is supplied when replay starts.

This keeps persisted execution history independent from the concrete infrastructure instance used to execute it.

```python
from selenium import webdriver


def create_driver():
    driver = webdriver.Chrome()
    driver.get("https://myapplication.com")
```