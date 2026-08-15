# Execution Policy

`TransactionPolicy` centralizes execution-related configuration instead of requiring individual execution parameters to be repeated throughout the API.

A transaction can define its execution policy as part of its class configuration.

```python
class MyTransaction(AbstractTransaction):
    policy = TransactionPolicy(
        pacing_time=1,
        retries=3,
        retry_on_exceptions=(SomeException,),
    )

    def do(self, ...):
        ...
```

The policy controls execution concerns such as:

* pacing between executions;
* retry behavior;
* exceptions eligible for retry;
* dry-run behavior;
* execution-related failure handling.

This keeps execution configuration close to the transaction while avoiding a growing list of execution parameters on the transaction API.

## Application Policy

An execution policy can also be configured at the `Application` level.

This provides a default execution behavior for transactions executed by that application.

Transaction-specific configuration can be used when a particular transaction requires different execution semantics.

The architectural distinction is:

```text
Application
    └── default execution policy
            ↓
Transaction
    └── transaction-specific policy
```

The policy is execution infrastructure; it should not contain business rules.

```python
Application(
        execution_policy=ApplicationPolicy(
            dry_run=True,
            retry_on_exceptions=(PermissionError, ConnectionAbortedError)
        )
    )
    ...
```

## Dry Run

Transactions and applications support dry-run execution.

A dry run allows an execution to go through the orchestration path without performing operations that should have real-world side effects.

This is useful for workflows such as:

* infrastructure operations;
* migrations;
* provisioning;
* synchronization;
* administrative commands;
* operational automation.

The feature is also available for asynchronous transaction execution.

```python
Application(
    execution_policy=ApplicationPolicy(dry_run=True)
    )
    ...

class MyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(dry_run=False)
    def do(self):
        ...
```

### Dry Run vs. Disable

These features have different meanings.

**Dry run**

> Execute the transaction while preventing its real side effects according to the transaction's dry-run behavior.

**Disable**

> Do not execute the transaction.

This distinction is useful in composed workflows.

For example:

```text
Validate customer
    ↓
Create order        ← dry run
    ↓
Process payment     ← disabled
    ↓
Send notification
```

The workflow can therefore be configured independently from whether individual transactions are enabled.

```python
Application(
    execution_policy=ApplicationPolicy(disable=True)
    )
    ...
```

## Disabling Transactions

Transactions can be explicitly disabled.

A disabled transaction provides a way to retain the transaction in the application workflow while preventing its execution.

This can be useful for:

* temporarily disabling an operation;
* environment-specific behavior;
* operational controls;
* gradual rollout;
* optional workflow steps.

Disabling should not be confused with a successful transaction execution. The transaction remains part of the application narrative, but its execution is intentionally suppressed.

```python
class MyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(disable=False)

    def do(self): ...
```

## Pacing and Retries

Transactions support execution pacing and retries.

### Pacing

Pacing introduces a controlled delay between transaction executions.

This can be useful when interacting with:

* APIs with rate limits;
* external systems;
* infrastructure services;
* resource-constrained systems.

```python
class MyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(pacing_time=3)

    def do(self): ...
```

### Retries

Retry configuration allows transient failures to be retried.

Retry behavior can be restricted to specific exception types rather than retrying every failure indiscriminately.

For example:

```text
Transaction
    ↓
Failure
    ↓
Is exception retryable?
    ├── No  → fail
    └── Yes
          ↓
       retry
```

Retries should be used carefully for transactions with side effects.

For production workflows, transactions that can be retried should preferably be **idempotent**, or the workflow should provide an appropriate compensation mechanism.

```python
class MyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(retries_on_failure=3)

    def do(self): ...
```


## Restricted Exceptions

Application execution can restrict the exception types that are handled by the execution policy.

This avoids treating every exception as a recoverable execution failure.

The distinction is important:

```text
Expected/transient failure
    → policy may recover

Programming error / invariant violation
    → propagate failure
```

Execution policies should therefore not become a mechanism for hiding defects.

```python
class MyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(
        retry_on_exceptions=(PermissionError, ConnectionAbortedError)
    )

    def do(self): ...
```