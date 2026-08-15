# Architectural Model

The feature set establishes four distinct concerns.

## 1. Intent

Represented by the transaction itself.

```text
CustomerPlacesOrder
ProcessPayment
ConfirmOrder
```

## 2. Contracts

Represented by `requires` and `ensures`.

```text
Requires:
    CustomerExists

Ensures:
    OrderIsConfirmed
```

## 3. Execution

Represented by `TransactionPolicy` and application execution controls.

```text
retry
pacing
dry run
disable
exception handling
```

## 4. Observability and Recovery

Represented by execution history, dump, replay and filtering.

```text
execute
   ↓
record
   ↓
dump
   ↓
replay
```

This separation is one of the most important architectural aspects of the feature.


## Example Workflow

A production workflow can therefore be modeled conceptually as:

```python
app.given(CustomerExists).when(CustomerPlacesOrder).when(PaymentIsProcessed).then(
    OrderIsConfirmed
)
```

With transaction contracts:

```text
CustomerPlacesOrder

Requires:
    CustomerExists

Ensures:
    OrderExists
```

```text
PaymentIsProcessed

Requires:
    OrderExists
    PaymentInformationAvailable

Ensures:
    PaymentProcessed
```

```text
OrderIsConfirmed

Requires:
    PaymentProcessed

Ensures:
    OrderConfirmed
```

Execution behavior can then be configured independently:

```text
TransactionPolicy
    ├── retries
    ├── retryable exceptions
    ├── pacing
    └── dry-run behavior
```

The resulting model is:

```text
                ┌──────────────────┐
                │ Application      │
                │ Orchestration    │
                └────────┬─────────┘
                         │
                 ┌───────▼────────┐
                 │ Transaction     │
                 │ Intent         │
                 └───────┬────────┘
                         │
             ┌───────────┼───────────┐
             ↓           ↓           ↓
         requires      do()       ensures
             │           │           │
             └───────────┼───────────┘
                         ↓
                TransactionPolicy
                         │
                         ↓
                Execution History
                         │
              ┌─────────────────────┐
              ↓                     ↓
            dump                 replay
```


## Architectural Value

The feature is more than a collection of execution controls.

It establishes Guará as an **application orchestration layer with explicit execution semantics**.

A conventional service method commonly combines:

```text
business intent
validation
execution
retry logic
logging
recovery
```

Guará can separate those concerns:

```text
Intent
  ↓
Transaction

Contract
  ↓
requires / ensures

Execution
  ↓
TransactionPolicy

Recovery / Observability
  ↓
history / dump / replay
```

This separation makes complex application workflows easier to inspect, operate, and reproduce.

However, Guará should not replace conventional domain objects, repositories, framework controllers, or infrastructure components merely because these features exist. Its strongest architectural role is to coordinate meaningful application operations and make their execution explicit.
