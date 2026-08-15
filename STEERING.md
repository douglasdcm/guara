Yes. In that case, `STEERING.md` should behave more like an **internal maintainer/developer contract for AI agents** than a user/developer guide.

The key focus should be:

* how the Guará source code is organized;
* coding conventions;
* Python/version compatibility;
* naming and documentation conventions;
* test architecture and testing strategy;
* mutation testing;
* async/sync parity;
* API compatibility;
* error handling and logging;
* repository hygiene;
* documentation expectations;
* how an AI should investigate an issue before changing code;
* what it must never do;
* architectural rules that are relevant to **maintaining the framework itself**, not teaching someone how to use Guará.

I would also explicitly tell the agent that **English is the project language**, including code comments, docstrings, test names, commit-oriented descriptions, and documentation.

Here is a more implementation-focused version:

# Guará — Steering Instructions for AI Coding Agents

## 1. Purpose

Guará is a Python framework. This document defines the rules and conventions that AI coding agents MUST follow when modifying, fixing, extending, refactoring, testing, or documenting the Guará source code.

This document is about **maintaining and evolving the Guará framework itself**.

It is NOT a guide for using Guará in external projects.

AI agents must prioritize:

1. correctness;
2. backward compatibility;
3. consistency with the existing implementation;
4. testability;
5. maintainability;
6. API stability;
7. architectural consistency;
8. minimal and focused changes.

Never introduce a new design simply because it is technically interesting or more modern. First understand the existing design and determine whether the requested change actually requires architectural modification.

---

# 2. Repository Is the Source of Truth

Before modifying code, inspect the repository.

The agent MUST NOT assume that a requested behavior already exists or that a proposed implementation is compatible with the framework.

Use the following order of investigation:

1. implementation;
2. unit tests;
3. integration tests;
4. existing usages inside the repository;
5. documentation;
6. configuration files;
7. historical or inferred behavior.

When implementation, tests, and documentation disagree, investigate the discrepancy before changing behavior.

Tests are especially important because they frequently define the precise behavioral contract of the framework.

---

# 3. Project Language

The official language of the Guará codebase is **English**.

All newly created or modified:

* source-code comments;
* docstrings;
* test names;
* test descriptions;
* exception messages;
* warning messages;
* logging messages;
* documentation;
* configuration descriptions;
* CLI messages;

MUST be written in English unless there is a specific technical reason otherwise.

Do not introduce Portuguese text into the framework source code.

Existing Portuguese text should not be translated merely as part of an unrelated change.

When modifying an existing Portuguese comment or documentation section, translate it only when the requested change already requires modifying that content.

---

# 4. Supported Python Version

Before using new Python syntax or standard-library functionality, inspect:

```text
pyproject.toml
```

The declared Python compatibility is authoritative.

Do not introduce syntax, typing features, or APIs that are unavailable in the project's supported Python versions.

Prefer standard-library functionality when it is sufficient.

Do not add a third-party dependency for a small utility that can reasonably be implemented using the existing Python standard library.

---

# 5. Repository Structure

The main implementation is located under:

```text
guara/
```

Current structure:

```text
guara/
├── abstract_transaction.py
├── application.py
├── assertion.py
├── constants.py
├── guara.py
├── it.py
├── transaction.py
├── utils.py
│
├── asynchronous/
│   ├── abstract_transaction.py
│   ├── application.py
│   ├── assertion.py
│   ├── guara.py
│   ├── it.py
│   └── transaction.py
│
└── cli/
    ├── main.py
    └── commands/
        └── replay.py
```

Tests are divided into:

```text
tests/
├── unit_test/
├── integration/
└── performance/
```

Documentation is under:

```text
docs/
```

Do not create new top-level directories or architectural layers without first determining that the existing structure cannot support the requested behavior.

---

# 6. Main Implementation Areas

Before changing a component, identify its architectural responsibility.

### `abstract_transaction.py`

Defines the fundamental synchronous Transaction abstraction.

### `transaction.py`

Contains Transaction-related concrete framework behavior.

### `application.py`

Contains Application-level orchestration and execution management.

### `assertion.py`

Contains assertion-related framework behavior.

### `constants.py`

Contains framework constants and environment-derived configuration.

### `utils.py`

Contains reusable framework utilities.

Do not move unrelated functionality into `utils.py` merely because it is convenient.

### `guara.py`

Contains framework-level functionality exposed by the Guará package.

### `it.py`

Contains framework constructs related to the test/execution interface.

### `asynchronous/`

Contains asynchronous counterparts of framework components.

### `cli/`

Contains command-line adapters.

CLI code must not become the location for core framework behavior.

---

# 7. Synchronous and Asynchronous Parity

Guará contains synchronous and asynchronous implementations.

Whenever modifying a synchronous framework abstraction, determine whether an equivalent asynchronous implementation exists.

For example:

```text
guara/abstract_transaction.py
guara/asynchronous/abstract_transaction.py
```

Do not blindly duplicate code between the two implementations.

Instead, determine:

* whether the behavior is applicable to both;
* whether asynchronous semantics require different handling;
* whether exceptions behave consistently;
* whether lifecycle behavior is equivalent;
* whether tests exist for both;
* whether documentation promises parity.

If a feature is intentionally synchronous-only, preserve that distinction.

If behavior should exist in both APIs, maintain semantic parity.

---

# 8. Public API Stability

Guará is a framework. Public APIs must be treated as contracts.

Before changing:

* class names;
* method names;
* method signatures;
* parameters;
* return values;
* exception behavior;
* import paths;
* environment variables;
* serialized structures;
* CLI commands;
* execution-history structures;

search the entire repository for usages.

Prefer backward-compatible changes.

Do not rename or remove an existing API merely to improve naming.

If a breaking change is explicitly required, identify all affected areas and update tests and documentation accordingly.

---

# 9. Minimal Change Principle

Implement the smallest change that correctly solves the problem.

Avoid unrelated:

* refactoring;
* renaming;
* formatting;
* dependency changes;
* file movements;
* architecture changes;
* test rewrites.

For example, if a bug exists in retry validation, do not refactor the entire Transaction hierarchy unless that refactoring is necessary to fix the bug.

Focused changes make framework behavior easier to review and reduce regression risk.

---

# 10. Code Style

Follow the style already established in the repository.

Prefer:

* explicit code;
* descriptive names;
* type annotations;
* small focused methods;
* single responsibility;
* clear control flow;
* standard Python idioms;
* existing project abstractions.

Avoid:

* unnecessary abstractions;
* deeply nested conditionals;
* clever one-liners;
* premature optimization;
* hidden side effects;
* duplicated logic;
* broad exception handling;
* unnecessary metaprogramming.

Do not change formatting conventions globally as part of a functional change.

---

# 11. Naming Conventions

Use standard Python naming conventions.

### Classes

Use PascalCase:

```python
class AbstractTransaction: ...
```

### Functions and methods

Use snake_case:

```python
def validate_transaction(): ...
```

### Variables

Use descriptive snake_case names:

```python
transaction_class
execution_history
retry_count
```

Avoid cryptic names unless they are conventional and local in scope.

### Private members

Use a leading underscore:

```python
self._driver
```

Do not expose an internal implementation detail as public API without a reason.

---

# 12. Type Annotations

Use type annotations consistently.

Prefer precise types when they improve understanding.

For example:

```python
def process(value: str) -> bool: ...
```

Avoid adding meaningless annotations merely to increase annotation coverage.

When the framework intentionally accepts arbitrary external dependencies, `Any` may be appropriate.

For example, the Transaction driver is intentionally generic.

Do not replace meaningful generic abstractions with artificial concrete types.

---

# 13. Docstrings

Public classes, methods, and functions should have useful docstrings when appropriate.

Docstrings should describe:

* purpose;
* important parameters;
* return value;
* exceptions when relevant;
* behavior that is not obvious from the implementation.

Do not write docstrings that merely repeat the function name.

Prefer:

```python
def act(...):
    """
    Executes the transaction while respecting dry-run configuration.
    """
```

over:

```python
def act(...):
    """Acts."""
```

Docstrings must be written in English.

---

# 14. Comments

Comments should explain **why**, not merely **what**.

Prefer:

```python
# Preserve the original parameters because execution history must
# contain masked values without modifying the actual transaction input.
```

over:

```python
# Mask parameters.
```

Do not add comments that become incorrect if the implementation changes.

Remove obsolete comments when modifying the affected code.

---

# 15. Formatting

Follow the formatting configuration already defined by the repository.

Before introducing a formatting tool or changing formatting rules, inspect:

```text
pyproject.toml
tox.ini
pytest.ini
```

Do not reformat unrelated files.

A functional change should not produce a large formatting-only diff.

If formatting is required, restrict it to the modified code whenever possible.

---

# 16. Imports

Keep imports clean and deterministic.

Prefer:

1. standard library;
2. third-party dependencies;
3. Guará/internal imports.

Avoid unused imports.

Avoid wildcard imports:

```python
from module import *
```

unless the existing architecture explicitly requires them.

Do not introduce circular imports to solve local problems.

When a circular dependency appears, reconsider the dependency direction instead of adding import hacks.

---

# 17. Logging

Use Python's logging infrastructure.

The framework already uses:

```python
from logging import Logger, getLogger
```

and module-level loggers.

Prefer logging over `print()` in framework code.

Do not log sensitive values.

Log messages should:

* be concise;
* provide useful diagnostic information;
* be written in English;
* use the appropriate logging level.

Do not use warnings or errors as normal control flow.

---

# 18. Exception Handling

Do not silently swallow exceptions.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

unless there is a clearly documented reason.

When catching an exception:

* catch the narrowest meaningful type;
* preserve useful information;
* avoid hiding programming errors;
* maintain the framework's existing exception semantics.

Do not introduce new exception types unless there is a clear architectural need.

Before changing exception behavior, inspect existing tests for expected exceptions.

---

# 19. Validation

Validation should be deterministic and explicit.

When validating configuration:

1. determine the accepted values;
2. preserve existing defaults;
3. reject invalid values consistently;
4. follow existing logging/error conventions;
5. add tests for valid and invalid cases.

If an invalid value currently results in a reset to `None`, do not silently change that behavior unless the task explicitly requires it.

---

# 20. Global State and Environment Variables

Inspect:

```text
guara/constants.py
docs/ENVIRONMENT_VARIABLES.md
tests/unit_test/test_enviroment_variables.py
```

before changing environment-driven behavior.

Avoid introducing new mutable global state.

If global configuration is required, follow the existing configuration mechanism.

Environment variables must:

* have predictable defaults;
* handle invalid values consistently;
* be documented;
* have tests.

Do not duplicate environment-variable parsing throughout the codebase.

---

# 21. Transaction Base Class

The main Transaction abstraction is:

```text
guara/abstract_transaction.py
```

The current class contains configuration such as:

```python
pacing_time
retries_on_failure
return_on_dry_run
retry_on_exceptions
```

and execution methods such as:

```python
do()
act()
undo()
revert_action()
```

When modifying this class, consider that it is a foundational abstraction.

A small change can affect:

* all Transactions;
* Application execution;
* retries;
* dry-run;
* undo;
* execution history;
* tests;
* asynchronous equivalents.

Always inspect dependent code before changing it.

---

# 22. `do()` vs `act()`

This distinction is important.

`do()` represents the concrete Transaction implementation.

`act()` represents framework-controlled execution.

Current semantics include dry-run handling in `act()`.

Do not bypass framework-level execution behavior accidentally by replacing:

```python
transaction.act(...)
```

with:

```python
transaction.do(...)
```

unless the change explicitly requires that behavior.

When modifying either method, inspect dry-run tests and Transaction execution tests.

---

# 23. Dry Run

Dry-run behavior is controlled by:

```python
GUARA_DRY_RUN
```

Current behavior includes:

```text
act()
 |
 +-- dry run
 |     |
 |     +-- Exception -> raise it
 |     +-- other value -> return it
 |
 +-- normal execution -> do()
```

Do not duplicate dry-run logic throughout Transactions.

Framework-wide behavior belongs in the framework execution layer.

---

# 24. Retry and Pacing

Retry behavior is cross-cutting framework behavior.

When modifying:

```text
pacing_time
retries_on_failure
retry_on_exceptions
```

inspect:

```text
tests/unit_test/test_transaction_pacing_time.py
tests/unit_test/test_transaction_retries_on_faliure.py
tests/unit_test/test_transaction_retry_on_exceptions.py
tests/unit_test/test_application_retry_on_exceptions.py
```

Test:

* valid configuration;
* invalid configuration;
* boundary values;
* exception filtering;
* number of retries;
* final failure;
* pacing behavior;
* interaction with dry-run when applicable.

Do not test only the happy path.

---

# 25. Undo and Reversion

When modifying:

```python
undo()
revert_action()
```

inspect:

```text
tests/unit_test/test_undo.py
docs/UNDO.md
```

Preserve the distinction between:

```text
action
reversal request
dry-run behavior
```

Do not assume every Transaction is reversible.

Do not invent automatic rollback semantics.

---

# 26. Execution History and Serialization

Execution history is a compatibility-sensitive area.

When changing history-related code, inspect:

```text
tests/unit_test/test_application_history_dump.py
```

and all code involved in:

* history creation;
* serialization;
* masking;
* replay;
* persistence;
* Transaction identification.

Sensitive values must not be persisted or logged accidentally.

If a Transaction class needs to be identified for replay, use a stable fully qualified module path where required:

```text
package.module.ClassName
```

Do not assume a class name alone is sufficient.

---

# 27. Replay

Replay is implemented under:

```text
guara/cli/commands/replay.py
```

Although replay is exposed through the CLI, its behavior depends on framework execution information.

When changing:

* Transaction identification;
* execution history;
* parameter serialization;
* module paths;
* import behavior;

inspect replay behavior.

Do not fix replay by introducing special cases that violate the framework's general model.

---

# 28. CLI Boundaries

The CLI is an adapter.

Core framework logic should remain outside:

```text
guara/cli/
```

CLI code should primarily:

1. parse input;
2. call framework APIs;
3. format results;
4. return appropriate exit status.

Do not duplicate Application or Transaction behavior inside CLI commands.

---

# 29. Testing Philosophy

Tests are part of the framework's specification.

A test should verify **behavior**, not merely implementation details.

Prefer:

```python
assert result == expected
```

or observable state/behavior assertions over assertions that a private implementation detail happened to be called.

Mock only where isolation requires it.

Do not mock everything.

Over-mocking can make tests pass while the actual framework behavior is broken.

---

# 30. Unit Tests

Unit tests are located under:

```text
tests/unit_test/
```

Use unit tests for:

* validation;
* state transitions;
* retry logic;
* dry-run;
* undo;
* parameter handling;
* utility functions;
* Application behavior;
* Transaction behavior;
* exception behavior.

Tests should be focused and deterministic.

Avoid dependencies on:

* network;
* real browsers;
* real external services;
* system-specific state;

unless the test is explicitly an integration or performance test.

---

# 31. Integration Tests

Integration tests are located under:

```text
tests/integration/
```

Use them when multiple Guará components need to work together.

Do not move every unit test into integration tests merely because it is easier.

Keep fast deterministic behavior in unit tests whenever possible.

---

# 32. Performance Tests

Performance tests are located under:

```text
tests/performance/
```

Do not use performance tests to validate ordinary functional behavior.

Do not modify performance tests simply to make functional tests pass.

Performance changes should be intentional and measurable.

---

# 33. Test Naming

Use descriptive test names that communicate the behavior being verified.

Prefer:

```python
def test_invalid_retry_count_is_reset_to_none(): ...
```

over:

```python
def test_retry(): ...
```

A test name should help a maintainer understand what behavior failed without opening the test immediately.

Test code is part of the project's documentation.

---

# 34. Edge Cases

When fixing or implementing behavior, consider at least:

* `None`;
* empty values;
* zero;
* negative values;
* incorrect types;
* boundary values;
* repeated execution;
* exceptions;
* partial failures;
* dry-run;
* retry configuration;
* asynchronous execution when applicable.

Do not add speculative behavior merely because an edge case exists.

Test behavior that is part of the intended contract.

---

# 35. Mutation Testing

The repository contains mutation-testing support:

```text
mutation.sh
```

Mutation testing is used to identify weaknesses in the test suite.

When implementing a bug fix, write a test that would fail against the broken implementation.

Do not create tests that only execute a line.

A good test should detect a meaningful mutation of the behavior.

For example, if a bug involves:

```python
value >= 0
```

the test should distinguish that behavior from:

```python
value > 0
```

when the boundary is part of the contract.

---

# 36. Regression Tests

Every bug fix should normally have a regression test.

The preferred pattern is:

```text
bug
 |
 v
minimal reproducer
 |
 v
regression test
 |
 v
implementation fix
 |
 v
existing test suite
```

Do not fix a bug without verifying the original failure when practical.

The regression test should describe the expected behavior, not reproduce an implementation detail.

---

# 37. Tests Must Not Be Weakened

Never:

* remove a failing test just because the implementation changed;
* make assertions less strict to make tests pass;
* skip a test without a documented reason;
* replace behavioral assertions with `assert True`;
* mock the component under test so aggressively that the bug disappears.

If an existing test conflicts with an intentionally changed public contract, update it deliberately and explain the contract change.

---

# 38. Test Isolation

Tests should be independent.

Avoid relying on execution order.

Avoid shared mutable state between tests.

When environment variables are modified:

* isolate the change;
* restore the original state;
* use the existing testing mechanisms.

When global framework configuration is modified, ensure subsequent tests are not affected.

---

# 39. Async Tests

Asynchronous behavior must be tested using the project's existing async testing approach.

Inspect:

```text
tests/unit_test/test_async_transaction.py
tests/unit_test/test_asynchronous_it.py
tests/integration/
```

when changing asynchronous functionality.

Do not convert asynchronous tests into synchronous tests merely to simplify implementation.

---

# 40. Documentation Changes

Documentation must remain synchronized with public framework behavior.

Relevant documentation includes:

```text
docs/TRANSACTION_QUICK_REF.md
docs/ASYNC.md
docs/UNDO.md
docs/COMPOSITE_TRANSACTION.md
docs/ENVIRONMENT_VARIABLES.md
docs/LOGS.md
docs/DEBUG.md
docs/MIGRATE_CODE.md
```

When changing public behavior, determine whether documentation must change.

Do not rewrite unrelated documentation.

Documentation changes must be written in English.

---

# 41. Dependency Management

Before adding a dependency:

1. check whether the standard library already provides the functionality;
2. check whether an existing dependency already provides it;
3. inspect `pyproject.toml`;
4. consider package size and compatibility;
5. consider whether the dependency is appropriate for a framework.

Do not add dependencies casually.

Do not introduce a dependency solely to simplify a few lines of internal code.

---

# 42. Security and Sensitive Data

Framework code may handle execution parameters and history.

Never expose sensitive values through:

* logs;
* exceptions;
* test output;
* execution history;
* debugging output;
* CLI output.

Inspect existing masking behavior before modifying parameter handling.

Relevant tests include:

```text
tests/unit_test/test_hide_secret.py
```

Security behavior must be preserved during refactoring.

---

# 43. Generated and Temporary Files

Do not commit generated artifacts, caches, or local development files.

Be especially careful with:

```text
__pycache__/
*.pyc
temporary files
coverage artifacts
mutation-testing artifacts
local IDE files
```

Respect the repository's `.gitignore`.

Do not modify generated files unless the task explicitly requires it.

---

# 44. Existing Experimental Code

The repository may contain experimental or temporary files.

Examples may include:

```text
tmp.py
dump.txt
gemini.txt
```

Do not automatically treat every file in the repository as part of the public architecture.

Before modifying an unfamiliar file, determine whether it is:

* production implementation;
* test;
* documentation;
* experiment;
* generated artifact;
* temporary development file.

Do not expand experimental code into the main architecture without explicit justification.

---

# 45. Refactoring

Refactoring is allowed when it improves the implementation without unintentionally changing behavior.

Before refactoring:

1. identify the current behavior;
2. identify tests covering it;
3. identify public APIs;
4. identify dependencies;
5. refactor incrementally;
6. run tests after the change.

Avoid large rewrites when a local refactoring is sufficient.

Do not combine architectural refactoring with an unrelated bug fix unless necessary.

---

# 46. Code Duplication

Avoid unnecessary duplication, especially between:

* synchronous and asynchronous implementations;
* validation methods;
* retry logic;
* serialization;
* CLI commands.

However, do not abstract code solely because two pieces look similar.

An abstraction is justified when the shared behavior is stable and the abstraction improves correctness or maintainability.

Prefer clear duplication over an incorrect or overly complex abstraction.

---

# 47. Internal vs Public APIs

A leading underscore generally indicates an internal implementation detail:

```python
_validate_class_variables()
_driver
```

Do not make private methods public without considering compatibility and architecture.

Likewise, do not rely on private methods from unrelated modules unless the existing design explicitly does so.

When modifying private behavior, still search for repository-wide usage because private APIs may have become de facto dependencies.

---

# 48. AI Investigation Procedure

For every issue, follow this procedure.

### Phase 1 — Locate

Find:

* relevant implementation;
* related classes;
* related methods;
* tests;
* documentation;
* configuration;
* usages.

### Phase 2 — Understand

Determine:

```text
What does the code currently do?
What behavior is expected?
What is the smallest difference between them?
Which public contracts are affected?
```

### Phase 3 — Reproduce

If possible, reproduce the issue with the smallest example.

For a bug:

```text
current behavior -> failing test
```

### Phase 4 — Implement

Make the smallest correct change.

### Phase 5 — Test

Run:

1. new/modified tests;
2. related unit tests;
3. broader test suite when appropriate.

### Phase 6 — Review

Check:

* API compatibility;
* sync/async parity;
* error behavior;
* logging;
* security;
* documentation;
* formatting;
* unrelated changes.

---

# 49. Before Creating a New Class

Do not create a class simply because the code can be organized into one.

Before adding a class, ask:

1. Does an existing abstraction already represent this responsibility?
2. Is the new abstraction part of the public API?
3. Does it introduce a new architectural concept?
4. Will it be reusable?
5. Does it simplify the design?
6. Can the behavior be implemented within an existing abstraction?

Prefer existing framework abstractions when appropriate.

---

# 50. Before Changing a Method Signature

Before changing:

```python
def method(...):
```

search for:

* direct calls;
* subclasses;
* overrides;
* tests;
* mocks;
* documentation;
* CLI usage;
* asynchronous counterparts.

Method signatures are API contracts.

Do not add parameters simply because they make one implementation easier.

---

# 51. Before Removing Code

Before deleting code:

1. search for references;
2. inspect tests;
3. inspect documentation;
4. determine whether it is public;
5. determine whether it is part of serialization/replay;
6. determine whether the asynchronous equivalent depends on it.

Dead-code assumptions must be verified, not guessed.

---

# 52. Pull Request / Change Quality

A high-quality framework change should have:

* a focused scope;
* a clear behavioral reason;
* tests;
* minimal unrelated changes;
* consistent naming;
* consistent formatting;
* English documentation/messages;
* preserved API behavior unless intentionally changed.

Avoid giant diffs.

A reviewer should be able to understand why each modified line is necessary.

---

# 53. What AI Agents Must Not Do

AI agents MUST NOT:

* invent framework APIs;
* silently change public behavior;
* remove tests to make the suite pass;
* weaken assertions;
* swallow exceptions;
* add unnecessary dependencies;
* introduce Portuguese into new framework content;
* rewrite unrelated modules;
* perform broad formatting changes unnecessarily;
* introduce architecture without evidence;
* bypass existing abstractions without understanding them;
* duplicate existing framework functionality;
* ignore the asynchronous implementation when relevant;
* ignore execution-history/replay implications when relevant;
* expose sensitive values;
* use `print()` as framework logging;
* modify generated artifacts unnecessarily;
* assume documentation is correct without checking implementation and tests;
* assume implementation is correct without checking tests.

---

# 54. Preferred Decision Hierarchy

When choosing between implementations, prioritize:

```text
1. Existing public contract
2. Existing tests
3. Existing architecture
4. Simplicity
5. Maintainability
6. Performance
7. New abstractions
```

Do not sacrifice compatibility or correctness for theoretical elegance.

---

# 55. Definition of Done

A framework change is considered complete only when applicable items below have been considered:

```text
[ ] Relevant implementation inspected
[ ] Relevant tests inspected
[ ] Existing usages searched
[ ] Public API impact evaluated
[ ] Synchronous implementation considered
[ ] Asynchronous implementation considered when applicable
[ ] Retry behavior considered when applicable
[ ] Dry-run behavior considered when applicable
[ ] Undo behavior considered when applicable
[ ] Execution history considered when applicable
[ ] Replay considered when applicable
[ ] Sensitive data handling considered
[ ] Regression test added for bug fixes
[ ] Boundary/edge cases tested
[ ] Existing tests preserved
[ ] Mutation resistance considered
[ ] Documentation updated when public behavior changed
[ ] English used for new project content
[ ] No unnecessary dependency introduced
[ ] No unrelated refactoring introduced
[ ] Formatting consistent with repository
[ ] Existing test suite passes
```

---

# 56. Final Instruction

The Guará framework should evolve through **small, evidence-based, test-driven changes**.

Before writing code, understand the existing code.

Before changing behavior, understand the tests.

Before changing an API, search its consumers.

Before creating an abstraction, understand the existing abstractions.

Before fixing a bug, create or identify a regression scenario.

Before refactoring, preserve the behavioral contract.

The goal of an AI coding agent is not merely to produce code that works for the immediate request.

The goal is to produce code that **belongs in the Guará framework**.
