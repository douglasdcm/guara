# Migrating a Legacy System to Page Transactions with Guará

This guide explains how to gradually migrate a real-world system from a procedural or poorly structured codebase to the **Page Transactions pattern using Guará**, without breaking the system or requiring a full rewrite.

We will use a simple **bakery management system** as an example, with operations like:

* Add product to stock
* Sell product
* Remove product
* Emit bills

The goal is to move safely, step by step, while keeping the system working at all times.

---

## Step 1: Identify Current Use Cases (Do Not Refactor Yet)

Start by identifying what the system does today.

Example of legacy procedural code:

```python
def sell_product(stock, product_name, quantity):
    if product_name not in stock:
        return "Product not found"

    if stock[product_name] < quantity:
        return "Not enough stock"

    stock[product_name] -= quantity
    return "Sale completed"
```

At this stage:

* Do not refactor
* Do not change behavior
* Just list the main use cases

Examples:

* Sell product
* Add product to stock
* Remove product
* Emit bill

---

## Step 2: Write Use Cases in Guará Style (Even Before Refactoring)

Now, describe the behavior using Guará syntax.

```python
app.when(SellProduct, product_name="Bread", quantity=2) \
   .asserts(it.IsEqualTo, "Sale completed")
```

At this point:

* The transaction may not exist yet
* You are defining **intent first**

This becomes your **target behavior**

---

## Step 3: Wrap Existing Code into Transactions (No Logic Change)

Create transactions that simply call the existing procedural code.

```python
from guara import AbstractTransaction

class SellProduct(AbstractTransaction):
    def do(self, stock, product_name, quantity):
        return sell_product(stock, product_name, quantity)
```

Important:

* Do not improve the code yet
* Just wrap it

This gives you:

* Immediate compatibility with Guará
* Zero risk migration

---

## Step 4: Introduce Application Context

Move shared data (like stock) into an application object.

```python
class BakeryApp:
    def __init__(self):
        self.stock = {
            "Bread": 10,
            "Cake": 5
        }
```

Update transaction:

```python
class SellProduct(AbstractTransaction):
    def do(self, product_name, quantity):
        return sell_product(self.app.stock, product_name, quantity)
```

Now the system starts to become structured.

---

## Step 5: Start Writing Tests Using Transactions

Use the same use cases as tests.

```python
app = Application(BakeryApp())

app.when(SellProduct, product_name="Bread", quantity=2) \
   .asserts(it.IsEqualTo, "Sale completed")
```

At this point:

* You already have tests
* Without rewriting logic

---

## Step 6: Gradually Refactor Inside Transactions

Now that behavior is protected by tests, improve the code safely.

Replace procedural logic:

```python
class SellProduct(AbstractTransaction):
    def do(self, product_name, quantity):
        product = self.app.stock.get(product_name)

        if not product:
            return "Product not found"

        if product < quantity:
            return "Not enough stock"

        self.app.stock[product_name] -= quantity
        return "Sale completed"
```

You can:

* Remove legacy functions
* Improve naming
* Add validations

---

## Step 7: Split Large Transactions (If Needed)

If a transaction becomes too big, break it.

```python
class HasStock(AbstractTransaction):
    def do(self, product_name, quantity):
        stock = self.app.stock

        if product_name not in stock:
            raise OutOfStockException("No product in stock")

        if stock[product_name] < quantity:
            raise OutOfStockException("Not enough product in stock")
```

Reuse it:

```python
class SellProduct(AbstractTransaction):
    def do(self, product_name, quantity):
        self.app.stock[product_name] -= quantity
        return "Sale completed"
```

---

## Step 8: Improve Readability with Guará Syntax

Move from simple calls to fluent scenarios:

```python
app \
  .given(HasStock, product_name=product_name, quantity=quantity) \
  .when(SellProduct, product_name="Bread", quantity=2) \
  .asserts(it.IsEqualTo, "Sale completed") \
  .when(EmitBill, product_name="Bread", quantity=2) \
  .asserts(it.Contains, "Bill emitted")
```

Now your code:

* Reads like a business flow
* Is executable
* Is testable

---

## Step 9: Replace CLI / API with Transactions

Old CLI:

```python
if action == "sell":
    sell_product(stock, name, qty)
```

New CLI:

```python
app.when(SellProduct, product_name=name, quantity=qty)
```

Your interface becomes a thin layer.

---

## Step 10: Organize Code by Intent

Group transactions:

* `actions/` → SellProduct, AddStock
* `validations/` → HasStock
* `queries/` → ListProducts

This improves scalability.

---

## Step 11: Remove Legacy Code

Once everything is covered by transactions and tests:

* Remove old procedural functions
* Keep only transactions and domain logic

---

## Final Result

You moved from:

```python
sell_product(stock, "Bread", 2)
```

To:

```python
app.when(SellProduct, product_name="Bread", quantity=2)
```

With:

* Unified requirements, implementation, and tests
* Safer refactoring
* Better readability
* Scalable architecture

---

## Key Migration Principles

* Do not rewrite everything at once
* Wrap first, refactor later
* Use transactions as boundaries
* Protect behavior with assertions
* Improve incrementally

---

## Final Thought

You don’t adopt Guará by rewriting your system.

You adopt it by **wrapping your system with use cases**,
then **letting those use cases reshape your architecture over time**.
