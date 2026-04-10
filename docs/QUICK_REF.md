# Quick Overview

## Application Quick Reference

The `Application` class is the execution engine of Guará. It orchestrates transactions and validations in a fluent, readable flow. Methods like `given`, `when`, `and_`, and `execute` all perform transactions, while `asserts`, `expects`, and `then` validate results using assertions. The `result` attribute always holds the output of the last executed transaction, and `undo` allows reverting executed actions when supported. The different method names exist only to improve readability and allow writing scenarios in a business-oriented style.

```{toctree}
:maxdepth: 1

APP_QUICK_REF
```

## Transaction – Quick Guide

The Transaction is the core abstraction used to define actions in Guará. A transaction represents a single, reusable unit of behavior, such as clicking a button, creating a user, calling an API, or applying business logic.

```{toctree}
:maxdepth: 1

TRANSACTION_QUICK_REF
```

## Assertions Quick Reference

Assertions in Guará validate the outcome of transactions using a consistent interface. Each assertion checks a specific condition, such as equality, presence in collections, numeric comparisons, string patterns, or state changes. All assertions follow the same pattern: they receive the actual value (from the last transaction) and compare it against an expected value or condition. This allows tests to remain expressive and focused on behavior rather than implementation details, while still covering simple and advanced validation needs.

```{toctree}
:maxdepth: 1

ASSERTION_QUICK_REF
```