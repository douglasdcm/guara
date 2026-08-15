# Recording workflows – Quick Reference
## Execution History

Guará records transaction execution history.

The history can be used to:

* Inspect previous executions
* Dump execution information
* Identify specific executions
* Replay transactions
* Resume interrupted workflows

Execution history can be dumped to a JSON file for later inspection or replay.

The resulting file contains the information required to reconstruct the recorded execution without serializing runtime infrastructure such as drivers.

```python
    (
        Application()
        .given(MyTransaction, secret=secret)
        ...
        .asserts(it.IsEqualTo, secret)
        .dump_history("dump.json)
    )
```

```json
{
  "application": null,
  "started_at": "2026-08-14T23:32:48.930791+00:00",
  "finished_at": "2026-08-14T23:32:48.933663+00:00",
  "status": "succeeded",
  "transactions": [
    {
      "id": "e6f3bec4b9604cf69d3b4b97ce7f9941",
      "policy": {
        "retry_on_exceptions": [
          "<class 'PermissionError'>"
        ],
        "abort_on_exceptions": null,
        "continue_on_exceptions": null,
        "rollback_on_failure": null,
        "disable": null,
        "dry_run": null,
        "pacing_time": 10,
        "retries_on_failure": null,
        "return_on_dry_run": null
      },
      "name": "MyTransaction",
      "module": "tests.unit_test.test_application_history_dump",
      "parameters": {
        "secret": "********",
      },
      "status": "succeeded",
      "started_at": "2026-08-14T23:32:48.932041+00:00",
      "finished_at": "2026-08-14T23:32:48.932076+00:00",
      "attempts": 1,
      "exception_type": null,
      "exception_message": null,
      "replayable": true
    },
    {
      "id": "addd20aadad94f148c775e98d8f7c1eb",
      "policy": {
        "retry_on_exceptions": [
          "<class 'PermissionError'>"
        ],
        "abort_on_exceptions": null,
        "continue_on_exceptions": null,
        "rollback_on_failure": null,
        "disable": null,
        "dry_run": null,
        "pacing_time": 10,
        "retries_on_failure": null,
        "return_on_dry_run": null
      },
      "name": "MyOtherTransaction",
      "module": "tests.unit_test.test_application_history_dump",
      "parameters": {
        "credit_card": "7654..."
      },
      "status": "succeeded",
      "started_at": "2026-08-14T23:32:48.933298+00:00",
      "finished_at": "2026-08-14T23:32:48.933329+00:00",
      "attempts": 1,
      "exception_type": null,
      "exception_message": null,
      "replayable": true
    }
  ]
}
```
