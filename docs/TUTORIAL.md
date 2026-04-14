# Tutorial

Page Transactions is primarily based on the Command Pattern (GoF), making it suitable for product development and test automation. This section is dedicated to showcasing uses of the framework.

## Domain Driven Design

This article presents a complete example of how to build a CLI-based education platform using the Guará framework. The goal is to demonstrate how business requirements can be translated directly into executable use cases, and how those same use cases drive implementation and testing.
Instead of separating requirements, application logic, and tests, Guará allows you to express everything through a unified approach based on transactions and fluent scenarios. This results in a system where behavior is explicit, traceable, and aligned with business intent.

```{toctree}
:maxdepth: 1

DDD
COMPOSITE_TRANSACTION
MIGRATE_CODE
```

## Modeling

Guará can be used to model system behavior at a high level using transactions that represent real user actions. Developers can describe use cases in a simple and expressive way, focusing on **what the system should do** instead of how it is implemented. These models can then be directly transformed into production code and also executed as validation scenarios. This makes Guará especially useful for designing applications from the ground up, where requirements, implementation, and tests evolve together from the same source. Example of Guará being used to describe the use cases, production code and tests of a Wine Application

```{toctree}
:maxdepth: 1

MODELING
```

## Automation Testing

This is the simplest implementation of a UI automation to warm up the framework. It uses the `OpenApp` and `CloseApp` transactions to open the web page of Google, to assert the title of the page is `Google` and to close the web application.

```{toctree}
:maxdepth: 1

TUTORIAL_TESTING
PT_AND_POM
OTHER_DRIVERS
TEST_FRAMEWORKS
ASYNC
LOGS
```

## Ubiquitous language

This article presents an approach to eliminate the gap between business language and software implementation by using the Guará framework to model workflows as code. Instead of translating business requirements into technical artifacts, it proposes writing code that directly reflects business intent through small, reusable transactions orchestrated in a readable, natural-language style. By extending generic constructs like “given, when, then” into domain-specific terms—such as financial expressions—the same code can be used for both production and testing, improving clarity, reusability, and alignment across developers, testers, analysts, and Product Owners. Ultimately, the article positions this approach as a way to turn code into living documentation that mirrors real-world processes.

```{toctree}
:maxdepth: 1

UBIQUITOUS_LANGUAGE
```

## Prototyping

Software engineers, UX designers with some knowledge of programming, and software students can leverage this project to build simple applications that are testable by default. For example, [To-Do List web application](https://github.com/douglasdcm/guara/blob/main/examples/prototyping) was built with Guara and PyScript.

## Crawler

Page transactions can be used to organize procedural code of crawlers. Here is an [example of a crawler](https://github.com/douglasdcm/guara/tree/main/examples/crawler) to get information from airports in Spain

## Extending Assertions

This example demonstrates how Guará allows you to extend its assertion mechanism by creating custom strategies tailored to your domain needs. By inheriting from `IAssertion`, you can define your own validation logic beyond the built-in assertions, enabling more flexible and expressive test scenarios. In this case, the custom assertion ignores case sensitivity when comparing values, showing how you can encapsulate reusable validation rules and seamlessly integrate them into your scenarios using the same fluent syntax.

```{toctree}
:maxdepth: 1

EXTEND_ASSERTIONS
```

## Debug

This example shows how Guará surfaces assertion failures in a clear and debuggable way. When an assertion does not pass, the framework propagates the error with detailed information, including the `actual` and `expected` values, along with the exact location in the test where the failure occurred. This makes it easy to understand what went wrong and why, without requiring additional debugging tools. Since assertions are implemented as Python code, you also benefit from standard traceback information, allowing you to quickly trace issues back to your custom logic or transaction behavior.

```{toctree}
:maxdepth: 1

DEBUG
```