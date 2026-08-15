# Policies, Contracts and CLI

## Overview

```{toctree}
:maxdepth: 1

ARCHITECTURE
POLICIES
CONTRACT
CLI
RECORD_AND_PLAY
```

Guará now provides a unified execution model for controlling, validating, observing, and replaying `Transaction` execution.

The feature set introduces:

* `TransactionPolicy` for controlling transaction execution behavior.
* Transaction-level `requires` and `ensures` contracts.
* Dry-run execution.
* Transaction enable/disable control.
* Retry and pacing configuration.
* Restricted exception handling.
* Execution history dumping and filtering.
* Replay of previous executions.
* Driver injection during replay.
* Application-level execution policies.

The goal is to make transaction execution **explicit, controllable, observable, and reproducible**, while keeping the business intent represented by the transaction separate from execution mechanics.

## Execution Lifecycle

The resulting transaction lifecycle can be viewed as:

```text
Application
    │
    ↓
Transaction selected
    │
    ↓
Is transaction enabled?
    │
    ├── No → skip execution
    │
    └── Yes
          │
          ↓
       requires
          │
          ↓
       dry-run?
          │
          ↓
       policy
          │
          ↓
       pacing/retry
          │
          ↓
       Transaction.do()
          │
          ↓
       ensures
          │
          ↓
     execution history
```

The exact internal implementation remains an implementation concern; the important architectural separation is between **intent**, **execution policy**, **contracts**, and **history**.
