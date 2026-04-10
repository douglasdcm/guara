# Transaction – Quick Guide

The Transaction is the core abstraction used to define actions in Guará. A transaction represents a single, reusable unit of behavior, such as clicking a button, creating a user, calling an API, or applying business logic.

## What is a Transaction

A transaction is a class that inherits from `AbstractTransaction` and implements the `do` method. This method contains the logic that will be executed when the transaction runs.

Each transaction:

* Encapsulates one action
* Receives input via keyword arguments
* Optionally returns a result
* Can be reused across scenarios

## Basic Structure

```python
class MyTransaction(AbstractTransaction):
    def do(self, **kwargs):
        # implement logic here
        return result
```

The `do` method is required. If not implemented, it raises an error.

## Execution Flow

When used with the `Application` class:

1. The transaction is instantiated with a driver or None
2. The `act` method is called
3. `act` internally calls `do`
4. The result is returned and stored in `Application.result`

You should not call `do` directly. The framework handles execution through `act`.
