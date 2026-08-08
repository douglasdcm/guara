# Guará — AI Agent Steering Guide

## 1. Purpose

Guará is a Python framework for modeling and executing meaningful application actions through **Transactions**.

AI agents working in this repository MUST understand the existing architecture before modifying code.

The primary goal is to evolve Guará without breaking its architectural concepts, public APIs, execution semantics, tests, documentation, or backward compatibility.

Do not treat Guará as a generic test-automation library. Its Transaction model is intended to represent meaningful actions that can be used in automated testing as well as production-oriented applications.

Core architectural concepts include:

* Intent-Driven Design
* Transactions as meaningful application actions
* Applications as orchestration mechanisms
* Drivers as external dependencies
* Assertions as explicit validation mechanisms
* Synchronous and asynchronous execution
* Replayable execution history
* Undo/compensation
* Dry-run execution
* Retry and pacing policies
* Composable Transactions
* Executable narratives

---

# 2. Golden Rules for AI Agents

Before changing code:

1. Read the relevant implementation.
2. Read the relevant unit tests.
3. Read the relevant documentation.
4. Search for usages of the API being changed.
5. Understand whether the change affects public behavior.
6. Preserve existing architectural boundaries.
7. Add or update tests for behavioral changes.
8. Update documentation when public behavior changes.
9. Do not invent APIs, classes, methods, configuration variables, or behavior.
10. Prefer the smallest change that correctly solves the problem.

Never modify an API merely because another design would look cleaner.

Existing behavior is part of the framework contract unless the task explicitly requests a breaking change.

---

# 3. Architectural Mental Model

Guará should be understood using the following separation:

```text
Application
    |
    | orchestrates
    v
Transaction
    |
    | expresses intent
    v
Domain/Application behavior
    |
    | uses
    v
Driver / Repository / External Dependency
```

The important distinction is:

```text
Intent
    !=
Orchestration
    !=
Implementation
```

### Transaction

A Transaction represents a meaningful action.

Examples conceptually include:

```text
CreateUser
RegisterProduct
AddProductToCart
Login
Checkout
CalculateTotal
```

A Transaction should express **what the application wants to accomplish**, not merely expose low-level technical operations.

### Application

The Application coordinates Transactions and execution flow.

It should not become a dump for domain logic.

### Driver

A driver is an injected external dependency.

It may be:

* a browser driver
* database connection
* API client
* repository
* custom external service
* another infrastructure dependency

The Transaction should not unnecessarily hard-code infrastructure dependencies.

### Assertion

Assertions represent explicit validation of expected behavior.

### Infrastructure

Infrastructure implements the mechanisms required to perform the intent.

The framework should preserve dependency direction and avoid coupling domain concepts directly to infrastructure details.

---

# 4. Intent-Driven Design

Guará uses Transactions to make application behavior explicit and readable.

A good Transaction describes an intention:

```python
class RegisterProduct(AbstractTransaction):

    def do(self, name, price):
        ...
```

rather than exposing an implementation detail as the primary abstraction:

```python
class ClickRegisterButton(AbstractTransaction):
    ...
```

Low-level actions may exist when necessary, but the preferred abstraction is the meaningful operation.

AI agents should favor code that allows an execution to read like an executable narrative.

For example:

```python
given(...)
when(...)
then(...)
```

or equivalent Application/Transaction flows should make the business intent understandable without requiring the reader to understand implementation details.

---

# 5. AbstractTransaction

The synchronous Transaction base class is located at:

```text
guara/abstract_transaction.py
```

The asynchronous counterpart is located at:

```text
guara/asynchronous/abstract_transaction.py
```

`AbstractTransaction` is the fundamental abstraction for synchronous Transactions.

Its responsibilities include:

* holding the injected driver
* defining Transaction execution
* supporting dry-run behavior
* supporting undo/reversion
* defining retry configuration
* defining pacing configuration
* validating Transaction class configuration
* providing a Transaction name

Conceptually:

```text
AbstractTransaction
    |
    +-- driver
    |
    +-- do()
    |
    +-- act()
    |
    +-- undo()
    |
    +-- revert_action()
    |
    +-- retry configuration
    |
    +-- pacing configuration
    |
    +-- dry-run configuration
```

---

# 6. Transaction Execution Semantics

The fundamental execution method is:

```python
do(**kwargs)
```

Subclasses implement the actual Transaction behavior.

`do()` is intentionally abstract-by-convention and currently raises:

```python
NotImplementedError
```

Agents MUST NOT silently change this contract.

The public execution path is:

```python
act(**kwargs)
```

Its behavior is:

```text
GUARA_DRY_RUN enabled?
    |
    +-- yes --> return return_on_dry_run
    |             or raise it when it is an Exception
    |
    +-- no --> execute do(**kwargs)
```

Therefore:

* `do()` contains the actual operation.
* `act()` controls dry-run semantics.
* Code that bypasses `act()` may bypass framework execution behavior.
* Do not replace calls to `act()` with `do()` unless the task explicitly requires it.

---

# 7. Dry Run

Dry-run behavior is controlled by:

```python
GUARA_DRY_RUN
```

When dry-run is enabled, `act()` does not execute `do()`.

Instead:

```python
return_on_dry_run
```

is returned.

If `return_on_dry_run` is an Exception, it is raised.

This behavior is intentional.

Do not make dry-run logic part of individual Transaction implementations unless there is a specific architectural reason.

The framework should centrally control execution semantics.

---

# 8. Undo and Reversion

Transactions may define:

```python
undo()
```

to reverse actions performed by:

```python
do()
```

The framework exposes:

```python
revert_action()
```

which respects dry-run mode.

Conceptually:

```text
act()
  |
  +-- do()

revert_action()
  |
  +-- undo()
```

Do not assume that every Transaction is automatically reversible.

A Transaction must explicitly implement meaningful compensation when reversal is possible.

For production-oriented operations, consider:

* partial failure
* idempotency
* compensation
* transaction boundaries
* external side effects

Do not invent automatic rollback semantics.

---

# 9. Transaction Configuration

Transactions may configure:

```python
pacing_time
retries_on_failure
return_on_dry_run
retry_on_exceptions
```

These values are class-level configuration.

The current `AbstractTransaction` validates configuration when a Transaction instance is created.

### pacing_time

Controls the local pacing interval between retries.

Invalid values are reset to:

```python
None
```

Valid values are non-negative integers.

### retries_on_failure

Controls the local retry count.

Valid values are non-negative integers.

Invalid values are reset to:

```python
None
```

### retry_on_exceptions

Defines exceptions eligible for retry.

Invalid configuration is reset to:

```python
None
```

### return_on_dry_run

Defines the value returned by a Transaction when dry-run mode is active.

Do not confuse this with the result of normal execution.

---

# 10. Driver Injection

`AbstractTransaction` accepts:

```python
driver: Any = None
```

The driver is stored internally.

The framework intentionally does not restrict the driver to a specific technology.

This allows Transactions to work with different kinds of external dependencies.

Do not introduce unnecessary coupling such as:

```python
from selenium import webdriver
```

into the Transaction base abstraction merely because one use case uses Selenium.

The driver abstraction must remain generic.

---

# 11. Transaction Naming

The Transaction name is derived from the concrete class:

```python
self.__class__.__name__
```

The `__name__` property therefore represents the concrete Transaction class name.

Agents modifying execution history, replay, logging, serialization, or reporting MUST consider the stability of Transaction names.

Transaction names may become part of persisted execution information.

Do not casually rename Transaction classes without checking:

* tests
* execution history
* replay behavior
* documentation
* serialized data
* external consumers

---

# 12. Applications

The main Application implementation is:

```text
guara/application.py
```

The asynchronous implementation is:

```text
guara/asynchronous/application.py
```

Applications are responsible for orchestration.

Do not move every behavior into `Application`.

A useful separation is:

```text
Application
    coordinates

Transaction
    expresses intent

Driver / Repository / Adapter
    performs infrastructure work
```

Application code should remain readable and should expose the execution narrative.

---

# 13. Synchronous and Asynchronous APIs

Guará has separate asynchronous implementations under:

```text
guara/asynchronous/
```

Important files include:

```text
abstract_transaction.py
application.py
assertion.py
guara.py
it.py
transaction.py
```

When changing a synchronous concept, determine whether an equivalent asynchronous implementation exists.

Do not automatically copy synchronous code into the asynchronous package.

First understand:

* whether semantics are equivalent
* whether execution is awaitable
* how exceptions propagate
* how retry behavior works
* how Application state is handled
* how assertions are executed

If a feature is expected to exist in both APIs, maintain semantic consistency while respecting their execution models.

---

# 14. Composite Transactions

Guará supports composite Transactions.

Relevant documentation:

```text
docs/COMPOSITE_TRANSACTION.md
```

A Composite Transaction combines multiple meaningful operations.

Do not flatten Composite Transactions into unrelated low-level operations.

The composition should preserve:

* execution order
* meaningful intent
* error behavior
* execution history
* undo semantics where applicable

---

# 15. Assertions

Assertion implementation:

```text
guara/assertion.py
```

Asynchronous implementation:

```text
guara/asynchronous/assertion.py
```

Assertions are separate from Transactions.

Do not turn every Transaction into an assertion.

A Transaction performs an action.

An Assertion verifies a condition.

Keep these responsibilities distinct.

---

# 16. CLI

The CLI implementation is located under:

```text
guara/cli/
```

Current structure includes:

```text
guara/cli/main.py
guara/cli/commands/replay.py
```

The CLI is an adapter around existing Guará functionality.

The CLI should NOT become the place where core execution logic is implemented.

Preferred structure:

```text
CLI
 |
 +-- parse arguments
 |
 +-- invoke existing Guará APIs
 |
 +-- translate result to CLI output / exit code
```

Use `argparse` consistently with the existing implementation.

Keep `main()` thin.

CLI output and application logging should remain conceptually separate.

When modifying CLI behavior, verify:

* command parsing
* exit codes
* invalid arguments
* successful execution
* failure execution
* replay behavior
* package entry points

---

# 17. Replay

Guará supports replaying dumped execution information.

Replay functionality is located under:

```text
guara/cli/commands/replay.py
```

Execution history and replay are important framework features.

When changing Transaction identification or execution serialization, verify replay compatibility.

Replay requires enough information to identify and reconstruct the original Transaction.

Do not use short class names when the system requires a complete importable module path.

For class identification, prefer the complete qualified path:

```text
package.module.ClassName
```

over:

```text
ClassName
```

When implementing module-path behavior, use Python's actual module metadata rather than assuming the file name or package structure.

---

# 18. Execution History

Execution history is part of the framework behavior.

Relevant implementation is primarily associated with:

```text
guara/application.py
```

and tests such as:

```text
tests/unit_test/test_application_history_dump.py
```

History may be used by:

* debugging
* reporting
* replay
* auditing
* execution analysis

Changes to execution-history structures should therefore be treated as potentially breaking changes.

When modifying history:

1. inspect serialization
2. inspect dump behavior
3. inspect replay
4. inspect tests
5. inspect sensitive-data masking
6. preserve backward compatibility when possible

Sensitive parameters must not accidentally be persisted in clear text.

---

# 19. Environment Configuration

Global behavior may be controlled through environment variables.

Relevant files:

```text
guara/constants.py
docs/ENVIRONMENT_VARIABLES.md
tests/unit_test/test_enviroment_variables.py
```

Do not introduce hard-coded environment behavior inside unrelated classes.

If an environment variable is required:

1. define it consistently
2. document it
3. add tests
4. preserve existing defaults
5. consider invalid values

---

# 20. Tests

Tests are a first-class part of the Guará architecture.

Main test areas:

```text
tests/unit_test/
tests/integration/
tests/performance/
```

Unit tests cover framework behavior including:

```text
test_dry_run.py
test_undo.py
test_transaction_pacing_time.py
test_transaction_retries_on_faliure.py
test_transaction_retry_on_exceptions.py
test_transaction_composite.py
test_application_history_dump.py
test_application_retry_on_exceptions.py
```

When modifying behavior, find the existing test that describes the behavior before writing a new implementation.

Preferred process:

```text
Understand existing test
        |
        v
Identify expected behavior
        |
        v
Modify implementation
        |
        v
Add/update focused tests
        |
        v
Run broader test suite
```

Do not delete or weaken tests merely because they make implementation changes inconvenient.

---

# 21. Mutation Testing

The repository contains:

```text
mutation.sh
```

and tests are expected to provide meaningful behavioral coverage.

When adding functionality, avoid tests that only verify implementation details.

Prefer tests that fail when the intended behavior is broken.

Mutation testing should be considered when determining whether a feature is genuinely covered.

A high line coverage number does not necessarily mean the behavior is adequately tested.

---

# 22. Performance Tests

Performance tests live under:

```text
tests/performance/
```

Do not modify performance tests as a shortcut to make functional tests pass.

Performance-related changes should be evaluated independently from correctness changes.

---

# 23. Documentation

Documentation lives under:

```text
docs/
```

Important architectural documents include:

```text
DDD.md
MODELING.md
PT_AND_POM.md
THE_PATTERN_EXPLAINED.md
TRANSACTION_QUICK_REF.md
COMPOSITE_TRANSACTION.md
UNDO.md
ASYNC.md
OTHER_DRIVERS.md
BEST_PRACTICES.md
```

Before changing architecture, read the relevant documentation.

When changing public behavior, update documentation when appropriate.

Documentation is part of the framework contract.

Do not allow implementation and documentation to describe different APIs.

---

# 24. Page Transactions and Page Objects

Guará supports the Page Transaction approach and integrates concepts related to Page Objects.

Relevant documentation:

```text
docs/PT_AND_POM.md
```

Page Objects should primarily represent UI structure and interaction primitives.

Transactions should represent meaningful operations.

Prefer:

```text
Page Object
    |
    | provides UI interaction primitives
    v
Transaction
    |
    | expresses meaningful operation
    v
Application
```

Do not put complete application workflows into Page Objects merely because the workflow happens through a UI.

---

# 25. DDD and Layering

Guará should preserve clear boundaries between layers.

A useful conceptual model is:

```text
Presentation / CLI / UI
          |
          v
      Application
          |
          v
       Domain
          |
          v
   Ports / Interfaces
          |
          v
     Adapters
          |
          v
 Infrastructure
```

The exact project structure does not have to mirror this diagram literally.

The important principle is dependency direction.

Domain/application concepts should not unnecessarily depend on concrete infrastructure.

Avoid creating circular dependencies.

---

# 26. Business Logic

Do not turn Transactions into giant business-logic classes.

A Transaction may coordinate domain behavior, but complex domain rules should remain appropriately separated.

Avoid:

```python
class HugeTransaction(AbstractTransaction):
    def do(self):
        # validation
        # database access
        # HTTP calls
        # business rules
        # formatting
        # logging
        # retries
        # persistence
        # reporting
        # everything else
```

Prefer clear separation of responsibilities.

The Transaction should remain the meaningful entry point for the action.

---

# 27. Error Handling

Do not catch exceptions merely to hide failures.

Preserve meaningful exception information.

When implementing retry behavior, distinguish between:

```text
recoverable failure
        vs.
non-recoverable failure
```

Retry configuration should be explicit.

Consider:

* exception type
* retry count
* pacing
* side effects
* idempotency
* partial execution
* final exception propagation

Never add broad exception handling such as:

```python
except Exception:
    pass
```

unless there is an explicitly documented reason.

---

# 28. State Management

Be careful with mutable state in:

* Application
* Transaction
* execution history
* retry logic
* asynchronous execution
* replay

Do not introduce global mutable state when instance or execution state is more appropriate.

When changing state transitions, inspect tests involving:

* Application enter/exit
* execution status
* execution history
* retries
* failures
* replay

---

# 29. Backward Compatibility

Guará is a framework.

Framework code has consumers.

Therefore, API changes must be treated more carefully than changes to an internal application.

Before changing:

* method signatures
* class names
* import paths
* environment variables
* serialization formats
* execution-history structures
* CLI commands
* return values
* exception behavior

search the entire repository for usages.

Prefer backward-compatible solutions when possible.

If a breaking change is required, document it explicitly.

---

# 30. Python Style

Follow the existing Python project conventions.

Prefer:

* type hints
* clear names
* small focused methods
* explicit behavior
* docstrings for public APIs
* standard-library solutions when sufficient
* existing project abstractions over duplicated implementations

Avoid unnecessary abstractions.

Avoid premature optimization.

Avoid introducing dependencies for functionality that can reasonably be implemented using the existing stack.

---

# 31. Type Hints

Use modern type hints consistent with the project's supported Python versions.

Before introducing a syntax feature, inspect:

```text
pyproject.toml
```

and the project's configured Python compatibility.

Do not introduce syntax unsupported by the project's declared Python versions.

Type hints should describe actual behavior rather than merely making static analysis happy.

---

# 32. Logging

Use the existing logging mechanism.

Avoid:

```python
print(...)
```

inside framework implementation code.

Logging should provide useful diagnostic information without leaking secrets.

Do not log sensitive parameters.

When changing logging behavior, inspect:

```text
docs/LOGS.md
tests/unit_test/test_hide_secret.py
```

---

# 33. Sensitive Data

Guará can store execution information.

Therefore, sensitive data must be handled carefully.

Never introduce logging or history persistence that exposes:

* passwords
* authentication tokens
* API keys
* secrets
* credentials
* other explicitly sensitive parameters

When changing parameter serialization, inspect the existing masking behavior first.

---

# 34. Repository Structure

Important repository areas:

```text
guara/
    abstract_transaction.py
    application.py
    assertion.py
    constants.py
    guara.py
    it.py
    transaction.py
    utils.py

    asynchronous/
        abstract_transaction.py
        application.py
        assertion.py
        guara.py
        it.py
        transaction.py

    cli/
        main.py
        commands/
            replay.py

docs/
tests/
    unit_test/
    integration/
    performance/
```

Do not create new top-level architectural layers without first understanding why the existing structure is insufficient.

---

# 35. Source of Truth

When investigating behavior, prioritize sources in this order:

1. Existing implementation
2. Existing tests
3. Public API usage inside the repository
4. Architecture documentation
5. README / quick references
6. Historical assumptions

If documentation conflicts with implementation and tests, investigate the discrepancy before changing either.

Never assume documentation is automatically more correct than executable behavior.

---

# 36. AI Agent Workflow

For every non-trivial task, follow this workflow.

## Step 1 — Understand

Identify:

```text
What is being requested?
Which component owns the behavior?
Is the behavior public?
Does synchronous code have an async counterpart?
Does the CLI depend on it?
Does replay depend on it?
Does execution history depend on it?
```

## Step 2 — Search

Search for:

```text
class
method
imports
usages
tests
documentation
configuration
serialization
CLI commands
```

## Step 3 — Model

Before coding, describe internally:

```text
Current behavior
Desired behavior
Affected components
Potential compatibility risks
Required tests
```

## Step 4 — Implement

Make the smallest coherent change.

Do not refactor unrelated code unless required.

## Step 5 — Test

Run focused tests first.

Then run the relevant broader test suite.

## Step 6 — Review

Check:

```text
API compatibility
Architecture
Tests
Async parity
CLI impact
Replay impact
History impact
Documentation
Security
```

## Step 7 — Explain

When presenting the change, clearly state:

* what changed
* why
* which files changed
* tests added/updated
* compatibility considerations

---

# 37. Refactoring Rules

Refactoring is allowed when it improves maintainability without changing behavior.

However:

```text
Refactoring != redesign
```

Do not redesign architecture during a bug fix unless the existing architecture prevents a correct solution.

Avoid unrelated changes such as:

* renaming unrelated classes
* formatting the entire repository
* moving files without necessity
* changing public APIs
* replacing libraries
* rewriting tests
* introducing new abstractions

Keep pull requests and commits conceptually focused.

---

# 38. Do Not Invent Missing Behavior

If the repository does not demonstrate that an API exists, do not assume it exists.

For example, do not invent:

```python
transaction.execute()
transaction.rollback()
application.replay()
application.status()
```

unless those APIs are actually present or explicitly requested.

Search the repository first.

If a requested behavior requires a new API, design it based on existing architectural patterns rather than guessing.

---

# 39. When Multiple Designs Are Possible

Prefer the design that:

1. preserves the existing public API
2. fits existing architecture
3. requires fewer changes
4. has clear tests
5. preserves synchronous/asynchronous semantics
6. maintains replay/history compatibility
7. keeps intent separate from implementation
8. avoids unnecessary dependencies

Do not choose an architecture merely because it is fashionable.

---

# 40. Production-Oriented Design

Although Guará is heavily useful for automated testing, its abstractions should remain useful for production-oriented applications.

When designing new functionality, consider:

* application boundaries
* domain behavior
* dependency inversion
* repositories
* external services
* transaction boundaries
* idempotency
* retries
* timeouts
* partial failure
* compensation
* observability
* state management

However, do not over-engineer a feature before the actual requirement exists.

Use the simplest architecture that preserves the framework's long-term design.

---

# 41. Important Architectural Principle

The central Guará concept is:

```text
A Transaction is a meaningful action,
not merely a technical operation.
```

The framework should allow an application to be understood through its actions.

Prefer:

```text
Register Product
Sell Product
Create Customer
Checkout
Login
```

over exposing implementation details as the primary application vocabulary.

The implementation may involve:

```text
HTTP
database
browser
filesystem
API
message queue
```

but those are infrastructure details.

The Transaction expresses the intent.

---

# 42. Definition of Done

A change is not complete merely because the code works locally.

For a meaningful framework change, verify:

```text
[ ] Existing behavior understood
[ ] Relevant implementation inspected
[ ] Relevant tests inspected
[ ] Public API impact considered
[ ] Synchronous behavior considered
[ ] Asynchronous behavior considered
[ ] CLI impact considered when applicable
[ ] Replay impact considered when applicable
[ ] Execution history impact considered when applicable
[ ] Sensitive data exposure considered
[ ] Unit tests added/updated
[ ] Integration tests considered
[ ] Documentation updated when necessary
[ ] No unrelated refactoring introduced
[ ] Existing tests pass
```

---

# 43. Final Rule for AI Agents

Before changing Guará, understand the intent behind the abstraction.

Do not optimize only for:

```text
"make this code pass"
```

Optimize for:

```text
"make the requested behavior correct while preserving
Guará's architectural language, public contracts,
testability, readability, and long-term evolution."
```

When uncertain, inspect the repository before making assumptions.

The existing code, tests, documentation, and public APIs are the primary evidence for how Guará is intended to work.

This version is intentionally written as **agent instructions rather than general project documentation**: it tells an AI what to inspect, what not to assume, where the important implementation lives, and which architectural invariants it must preserve.
