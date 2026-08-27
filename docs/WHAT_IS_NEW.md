# What's New
## 0.0.26rc1
This release improves the validation of transaction contracts (`requires` and `ensures`) to allow users to return truthy values in positive paths and falsy values in negative paths.

```python
class MyContract(AbstractTransaction):
    def do(self, param):
        return object() if param > 10 else None


class MainTransaction(AbstractTransaction):
    requires = [MyContract]

    def do(self, param): ...
```

If the contract is violated then a `ContractError` exception is raised.

## 0.0.25

This release introduces a major evolution of Guará's execution model, with new capabilities for **transaction control, execution policies, contracts, dry runs, execution history, replay, and application-level orchestration**.

The main goal is to make Guará Transactions more expressive and reliable for production application workflows while keeping execution behavior declarative and centralized.

### Transaction Execution Policies

Transaction execution behavior can now be configured through an `TransactionPolicy`.

Instead of scattering execution parameters across transaction definitions, policies provide a centralized way to configure concerns such as:

* Retry behavior
* Retryable exceptions
* Pacing between executions
* Dry-run behavior
* Other execution-related policies

This makes execution behavior explicit while keeping the Transaction implementation focused on its actual intent.

```python
class CreateProduct(AbstractTransaction):
    policy = TransactionPolicy(
        pacing_time=1,
        retries_on_failure=3,
    )

    def do(self, name, price): ...
```

Application-level policies are also supported, allowing execution behavior to be configured at the orchestration level.

### Dry Run

Transactions and Applications now support **dry-run execution**.

A dry run allows a workflow to be executed without performing its actual side effects. This is useful for validating execution flows, inspecting what would happen, and safely evaluating application operations.

Dry-run behavior can be controlled through execution policy, including whether a transaction should return its normal result during a dry run.

### Transaction Contracts

Transactions now support declarative contracts through `requires` and `ensures`.

#### Requires

`requires` defines conditions that must be satisfied before a Transaction executes.

```python
class CreateProduct(AbstractTransaction):
    requires = [
        ProductDataIsValid,
        UserIsAuthorized,
    ]
```

#### Ensures

`ensures` defines conditions that must be satisfied after the Transaction completes.

```python
class CreateProduct(AbstractTransaction):
    ensures = [
        ProductWasCreated,
        StockWasInitialized,
    ]
```

This separates the **contract of a Transaction** from its implementation.

The previous precondition and postcondition mechanisms were removed in favor of this more explicit contract model.

### Application Contracts

Contract conditions can also be associated with the Application orchestration layer.

This makes it possible to express constraints around complete application workflows rather than only individual Transactions.

The resulting architecture distinguishes between:

* **Application-level contracts** — constraints around workflows
* **Transaction-level contracts** — constraints around individual operations
* **Transaction implementation** — the actual behavior

### Transaction Enable / Disable

Transactions can now be disabled.

This allows an application to retain a Transaction in its workflow definition while preventing its execution when required.

This capability can be useful for:

* Feature switches
* Optional workflow steps
* Operational controls
* Temporarily disabling integrations
* Environment-specific behavior

### Improved Retry and Execution Control

Transaction execution now provides more control over failures and retries.

The execution model supports:

* Configurable retry behavior
* Restricted exception handling
* Pacing between attempts
* Application-level execution policies
* Transaction-level execution policies

This allows retry behavior to be treated as an execution concern rather than being embedded directly into business logic.

### Execution History and Dump

Guará now provides improved execution-history capabilities.

Execution history can be dumped and inspected, including support for filtering executions by transaction ID.

This provides a persistent representation of what was executed and makes execution information useful beyond the lifetime of the current Application instance.

### Replay Execution

Dumped execution history can now be replayed.

Replay reconstructs the execution flow from the stored history, making it possible to reproduce previous executions.

The replay functionality was also extended to support:

* Transaction selection by ID
* Resuming execution
* Driver injection through the replay command

This is particularly useful for operational troubleshooting and reproducing application workflows.

### Resume Replay

Replay can now resume an execution from a specific point in the recorded workflow.

Instead of replaying an entire execution history, applications can continue from the selected transaction.

This provides a foundation for recovering and continuing interrupted workflows.

### Driver Injection During Replay

The replay command can now receive a driver and provide it to the `Application`.

This makes replay useful for workflows that depend on external infrastructure or technical drivers rather than only pure Python Transactions.

### Application Improvements

The `Application` abstraction received several improvements:

* Application names
* Application-level execution policies
* Application enable/disable behavior
* Application-level dry runs
* Restricted exception handling
* Improved lifecycle logging
* Improved execution logging

These changes strengthen the role of `Application` as the orchestration boundary for Guará workflows.

### Async Dry Run

Dry-run support was also extended to asynchronous execution.

This keeps the execution model consistent between synchronous and asynchronous workflows.

### Improved Logging

Logging was significantly improved throughout the framework.

Changes include:

* Structured JSON logging
* Improved Application lifecycle logs
* Improved transaction execution logs
* Better error information
* More consistent logging behavior

These improvements make Guará execution easier to observe in production environments.

### Code Quality and Documentation

The release also includes several internal improvements:

* Improved documentation and docstrings
* Improved readability of `transaction.py`
* Ruff formatting and linting
* Removal of deprecated `setup.py` files
* Environment variables centralized in constants
* Improved test coverage
* Additional tests for execution policies, retries, pacing, dump/replay, and new transaction features
* Cleanup of example and test structures

### Architectural Direction

These changes continue Guará's evolution from a framework primarily focused on test automation toward a more general **application orchestration framework**.

The central model is becoming:

```text
Application
    │
    ├── Execution Policy
    │
    ├── Contract
    │
    └── Transaction
            │
            ├── Policy
            ├── Requires
            ├── Implementation
            └── Ensures
```

This allows application workflows to express **intent**, while execution policies, contracts, history, replay, and infrastructure remain separate concerns.

### Summary

The most important additions in this release are:

* **TransactionPolicy** for centralized execution behavior
* **Dry-run execution** for Applications and Transactions
* **`requires` / `ensures` contracts**
* **Transaction enable/disable**
* **Retry and pacing controls**
* **Execution history dumping**
* **Transaction ID filtering**
* **Execution replay**
* **Replay resume**
* **Driver injection during replay**
* **Application-level policies and contracts**
* **Async dry-run support**
* **Improved structured logging**
* **Expanded automated test coverage**

Together, these features provide a stronger foundation for building **observable, controllable, replayable, and contract-driven application workflows with Guará**.
