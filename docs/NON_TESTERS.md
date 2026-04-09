# Non-Testers Usage

Page Transactions is primarily based on the Command Pattern (GoF), making it suitable for product development as well, even though that is not its primary intent. This section is dedicated to showcasing other uses of the framework that are unrelated to automation testing.

## Ubiquitous language

This article presents an approach to eliminate the gap between business language and software implementation by using the Guará framework to model workflows as code. Instead of translating business requirements into technical artifacts, it proposes writing code that directly reflects business intent through small, reusable transactions orchestrated in a readable, natural-language style. By extending generic constructs like “given, when, then” into domain-specific terms—such as financial expressions—the same code can be used for both production and testing, improving clarity, reusability, and alignment across developers, testers, analysts, and Product Owners. Ultimately, the article positions this approach as a way to turn code into living documentation that mirrors real-world processes.

```{toctree}
:maxdepth: 1

UBIQUITOUS_LANGUAGE
```

## Modeling

Guará can be used to model system behavior at a high level using transactions that represent real user actions. Developers can describe use cases in a simple and expressive way, focusing on **what the system should do** instead of how it is implemented. These models can then be directly transformed into production code and also executed as validation scenarios. This makes Guará especially useful for designing applications from the ground up, where requirements, implementation, and tests evolve together from the same source. Example of Guará being used to describe the use cases, production code and tests of a Wine Application

```{toctree}
:maxdepth: 1

MODELING
```

## Prototyping

Software engineers, UX designers with some knowledge of programming, and software students can leverage this project to build simple applications that are testable by default. For example, [To-Do List web application](https://github.com/douglasdcm/guara/blob/main/examples/prototyping) was built with Guara and PyScript.

## Crawler

Page transactions can be used to organize procedural code of crawlers. Here is an [example of a crawler](https://github.com/douglasdcm/guara/tree/main/examples/crawler) to get information from airports in Spain
