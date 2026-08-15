# Policeis – Quick Reference
## Execution Policy

`TransactionPolicy` centralizes transaction execution configuration such as pacing, retries, retryable exceptions, and dry-run behavior.

```python
class MyTransaction(AbstractTransaction):
    policy = TransactionPolicy(
        pacing_time=1,
        retries=3,
        retry_on_exceptions=(SomeException,),
    )

    def do(self, **kwargs):
        return result
```

Policies can also be configured at the `Application` level.

## Dry Run

A transaction can be executed in dry-run mode to evaluate the workflow without performing its real side effects.

```python
app.when(MyTransaction, dry_run=True)
```

Dry-run behavior can also be controlled through the execution policy.

Dry run is different from disabling a transaction: a dry run executes the transaction according to its dry-run behavior, while a disabled transaction is not executed.

## Disable Transaction

A transaction can be disabled when its execution should be skipped.

```python
class MyTransaction(AbstractTransaction):
    enabled = False
```

This is useful for optional, environment-specific, or temporarily disabled workflow steps.

## Pacing

`pacing_time` controls the delay between transaction executions.

```python
class MyTransaction(AbstractTransaction):
    policy = TransactionPolicy(
        pacing_time=2,
    )
```

Use pacing when interacting with external systems that require controlled execution rates.

## Retries

Transactions can retry failed executions according to their execution policy.

```python
class MyTransaction(AbstractTransaction):
    policy = TransactionPolicy(
        retries=3,
    )
```

Retryable exceptions can be restricted:

```python
class MyTransaction(AbstractTransaction):
    policy = TransactionPolicy(
        retries=3,
        retry_on_exceptions=(TimeoutError,),
    )
```

Retries should generally be used with idempotent operations.

## Application-Level Policy

Execution policies can be configured at the `Application` level to provide default execution behavior for its transactions.

This allows execution concerns to be configured separately from the transaction's business intent.

```python
Application(execution_policy=ApplicationPolicy(disable=True)).given(...)
```