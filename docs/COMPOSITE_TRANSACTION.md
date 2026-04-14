# Understanding the Composite Approach

The Composite approach is a simple and powerful way to **combine multiple operations into a single, unified action**. Instead of executing steps one by one manually, you group them into a higher-level structure that behaves like a single operation.

This is especially useful when you have **repetitive sequences of actions** or when you want to simplify complex workflows.

## The Core Idea

Instead of doing this:

```python
app.execute(DoThis)
app.execute(DoThat)
app.execute(DoOtherThing)
```

You create a single structure that represents all of them:

```python
class DoAll(AbstractTransaction):
    # do all
```

Internally, `DoAll` executes each step in order.

## Why Use Composite?

The Composite approach helps you:

* Reduce duplication
* Improve readability
* Encapsulate workflows
* Reuse sequences of actions
* Simplify complex logic

## Composite Classes

You can model this using transactions:

```python
class DeductStock(AbstractTransaction):
    def execute(self, product, qty):
        print("Deducting stock")

class EmitReceipt(AbstractTransaction):
    def execute(self, product, qty):
        print("Emitting receipt")
```

Now create the composite:

```python
class SellProduct:
    def __init__(self):
        self.steps = [
            DeductStock,
            EmitReceipt
        ]

    def execute(self, product, qty):
        for step in self.steps:
            step().execute(product, qty)
```

Usage:

```python
SellProduct().execute("Bread", 2)
```

## More Flexible Composite

You can also make it dynamic:

```python
class CompositeTransaction(AbstractTransaction):
    def do(self, steps, **kwargs):
        results = []
        for step in steps:
            result = step().do(**kwargs)
            results.append(result)
        return results
```

Usage:

```python
app.when(
    CompositeTransaction,
    steps=[DeductStock, EmitReceipt],
    product="Bread",
    qty=2
).then(it.ContainsAll, ["all", "expecetd", "results"])
```

## When Should You Use Composite?

Use it when:

* You have a sequence of steps that always run together
* You want to simplify complex flows
* You want to reuse workflows across the system
* You want to hide internal details from the caller

Avoid it when:

* The steps are unrelated
* You need highly dynamic or conditional flows (unless you handle conditions inside)

## Benefits

* Cleaner code
* Better abstraction
* Easier maintenance
* Improved readability
* Reusable workflows

## Final Thought

The Composite approach is about **thinking in flows instead of isolated actions**.

Instead of asking:

* “What functions should I call?”

You start asking:

* “What is the complete action the user wants?”

And then model that action as a single, reusable unit.
