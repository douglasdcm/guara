# Contracts
## Preconditions: `requires`

Transactions can declare conditions that must be satisfied before execution.

The purpose of `requires` is to express **execution prerequisites**.

Conceptually:

```python
class CustomerPlacesOrder(AbstractTransaction):

    requires = [CustomerExists, ProductIsAvailable,...]

    def do(self, ...):
        ...
```

A transaction should not execute its main operation when a required condition is not satisfied.

### Why `requires`?

A prerequisite represents something that must already be true before the transaction can safely perform its operation.

Examples include:

* the customer must exist;
* the user must be authenticated;
* an account must be active;
* required input must be available;
* an external resource must be accessible.

This is different from putting the validation directly into `do()`.

Instead of:

```python
def do(self, customer):
    if not customer:
        raise ...
```

the transaction contract can communicate:

```text
Requires:
    CustomerExists
```

The resulting transaction becomes easier to understand as an executable narrative.

---

## Postconditions: `ensures`

Transactions can also declare conditions that must hold after execution.

The `ensures` contract expresses the expected state after the transaction completes successfully.

Conceptually:

```python
class CustomerPlacesOrder(AbstractTransaction):

    ensures = [OrderIsCreated, ...]

    def do(self, ...):
        ...
```

Examples include:

* an order must be confirmed;
* stock must have been reduced;
* a payment must have been processed;
* a customer must have an updated balance.

The conceptual lifecycle is:

```text
requires
    ↓
Transaction execution
    ↓
ensures
```

This establishes an explicit contract around the transaction without mixing the contract itself with its implementation.

---

## Preconditions and Postconditions vs. Business Rules

`requires` and `ensures` should not become a replacement for domain modeling.

They are most valuable when expressing **application-level execution contracts**.

For example:

```text
CustomerPlacesOrder

Requires:
    CustomerExists
    ProductIsAvailable

Does:
    CreateOrder

Ensures:
    OrderIsCreated
```

The transaction orchestrates the operation.

Business invariants that belong to domain entities, aggregates, or domain services should remain there.

This distinction is important:

```text
Domain
    Business rules and invariants

Transaction
    Application intent and orchestration

TransactionPolicy
    Execution mechanics
```
