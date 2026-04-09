# Modeling Business Workflows as Code with Guará

## Overview

In many software projects, there is a persistent gap between how business stakeholders describe a system and how developers implement it. Product Owners and analysts define workflows using business language, while developers translate those ideas into technical code. Testers then validate behavior using yet another layer of abstraction.

This separation introduces:
- Miscommunication
- Ambiguity
- Misalignment between expectations and implementation

Even with practices like the Three Amigos, there is still a translation step between business intent and executable code.

This tutorial presents an alternative approach using the Guará framework: writing software where business language, implementation, and validation are aligned into a single expressive model.

## Goal

By the end of this tutorial, you will understand how to:

- Model business workflows using code
- Use a shared language across business, development, and testing
- Structure systems using reusable transactions
- Extend a generic framework into a domain-specific language (DSL)
- Reuse the same logic in both production and testing

## Core Concept: Transactions

Guará is based on a simple idea:

Break your system into small actions (called transactions) and validate their results.

Each transaction:
- Encapsulates a unit of behavior
- Can return a result
- Can be reused across multiple scenarios

## Writing Readable Workflows

With Guará, you can express workflows using a structured, readable syntax:

```python
app.given(UserLoggedIn) \
   .when(Search, product="notebook") \
   .then(ReportChart) \
   .expects(IsEqualTo, 1)
````

This approach provides:

* A clear execution flow
* Improved readability
* A structure that resembles natural language

At this stage, the code already improves test readability. However, it still uses generic terms.

## Moving to Business Language

To fully align code with business thinking, you can extend the framework into a domain-specific language.

For example, in a financial context:

```python
fin_app.account_with(HasBalance) \
       .execute(BuyAsset, symbol="AAPL", amount=2000) \
       .settles(UpdatePortfolio) \
       .reconciles(ExpectedPortfolio, 20)
```

This version expresses:

* Business intent
* Domain terminology
* Execution flow

The code is no longer just a test. It becomes executable business logic.

## Implementing Transactions

Transactions encapsulate behavior and can be used in both production and testing.

Example:

```python
class BuyAsset(AbstractTransaction):
    def do(self, symbol, amount):
        DataBase.balance -= amount
```

This implementation represents a real business operation:

* A user buys an asset
* The system deducts the corresponding amount from the balance

Because transactions are reusable, they can be used across:

* Application logic
* Test scenarios
* Simulations

This eliminates duplication and ensures consistency.

## Framework Architecture

The framework is built around three core components:

### Transactions

Small, reusable units of work.

Example:

* BuyAsset
* UpdatePortfolio

### Application

The orchestrator that executes transactions in sequence.

### Assertions

Validation mechanisms that verify results.

## Execution Flow

The framework follows a structured execution pattern:

* given / when / then → execute transactions
* asserts / expects → validate results

All execution is coordinated by the Application class.

## Extending to a Domain-Specific Language

One of the key strengths of this approach is the ability to extend the framework into a ubiquitous language.

### Generic Terms

* given
* when
* then
* asserts

### Financial Domain Mapping

* given → account_with, portfolio_with, positioned_with
* when → execute, trade
* then → settles, result_in
* asserts → reconciles, balances

This mapping transforms technical steps into meaningful business expressions.

## Example: Financial Application

Below is a simplified example of extending the framework for a financial domain:

```python
from guara.transaction import Application, AbstractTransaction
from guara import it

class FinancialApplication(Application):
    def __init__(self, driver=None):
        super().__init__(driver)

    def account_with(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    def execute(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    def settles(self, transaction, **kwargs):
        super().then(transaction, **kwargs)
        return self

    def reconciles(self, assertion, expected):
        super().asserts(assertion, expected)
        return self


class BuyAsset(AbstractTransaction):
    def do(self, symbol, amount):
        DataBase.balance -= amount


class ExpectedPortfolio(it.IsEqualTo):
    def __init__(self):
        super().__init__()


def main():
    fin_app = FinancialApplication()
    (
        fin_app.account_with(HasBalance)
        .execute(BuyAsset, symbol="AAPL", amount=2000)
        .settles(UpdatePortfolio)
    )


def test_extend_ubiquitous_language():
    fin_app = FinancialApplication()
    (
        fin_app.account_with(HasBalance)
        .execute(BuyAsset, symbol="AAPL", amount=2000)
        .settles(UpdatePortfolio)
        .reconciles(ExpectedPortfolio, 20)
    )
```

## Key Benefits

### Alignment Between Roles

Developers, testers, analysts, and Product Owners can all understand the same code.

### Reusability

Transactions are reusable across:

* Tests
* Production workflows
* Simulations

### Readability

Code expresses intent clearly, reducing the need for external documentation.

### Maintainability

Changes in business logic are localized within transactions.

### Living Documentation

Test scenarios double as documentation of system behavior.

## From Testing to System Design

What starts as a testing pattern evolves into a broader architectural approach:

* Modeling workflows as code
* Defining domain behavior explicitly
* Bridging the gap between business and implementation

Instead of writing code and then explaining it, you write code that already explains itself.

## Conclusion

When code reflects the language of the business:

* Communication improves
* Complexity is reduced
* Systems become easier to evolve

If your code cannot be understood by the business, only part of the team can effectively work with it.

If your code speaks the language of the business, you are not just implementing features.

You are modeling reality.

