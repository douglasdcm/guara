# Contract – Quick Reference
## Preconditions – `requires`

`requires` defines conditions that must be satisfied before a transaction executes.

```python
class CreateOrder(AbstractTransaction):
    requires = [CustomerExists]

    def do(self, **kwargs): ...
```

Use `requires` for application-level prerequisites such as required resources, state, or permissions.

## Postconditions – `ensures`

`ensures` defines conditions that must be satisfied after a transaction successfully executes.

```python
class CreateOrder(AbstractTransaction):
    ensures = [OrderExists]

    def do(self, **kwargs): ...
```

Use `ensures` to express the expected result or state after execution.