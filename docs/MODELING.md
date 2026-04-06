# 🍷 Modeling Use Cases as Code with Guará

## Introduction

Guará provides a simple and powerful way to model system behavior using **transactions as first-class concepts**. Instead of separating requirements, implementation, and tests, Guará allows you to describe everything using a single, consistent language.

With Guará, you can:

* Model **use cases as executable code**
* Use those same use cases to **drive production implementation**
* Reuse them directly as **test scenarios**

This approach turns your use cases into the **source of truth for your system**.

---

## 🧠 Use Cases in Guará Style

In Guará, behavior is expressed through a fluent and readable syntax:

```python
in_wine_app.when(ListWines).asserts(it.IsNotEmpty)
in_wine_app.when(AddWineToCart, with_name="Merlot", with_quantity=2)
in_wine_app.when(Checkout).asserts(it.Contains, "Purchase successful")
```

Key ideas:

* `in_wine_app` represents the application context
* `.when(Transaction, params...)` represents a user action
* `.asserts(...)` defines the expected outcome

This structure focuses entirely on **user intent**, not implementation details.

---

## 🔁 From Use Cases to Production Code

Each transaction used in a use case becomes a **concrete class in your production code**.

For example:

```python
in_wine_app.when(ListWines)
```

Directly translates to:

```python
class ListWines(AbstractTransaction):
    def do(self):
        return self.app.catalog.list_all()
```

This creates a natural flow:

* You write the use case
* You implement the transaction
* The system behavior emerges

There is no gap between **requirement and implementation**.

---

## 🏗 Example: Wine Store Implementation

Below is a simple example of how the wine store can be implemented following the use cases.

---

### Domain Model

```python
class Wine:
    def __init__(self, name, price, type):
        self.name = name
        self.price = price
        self.type = type
```

---

### Repository

```python
class WineRepository:
    def __init__(self):
        self._wines = [
            Wine("Cabernet Sauvignon", 100, "red"),
            Wine("Merlot", 80, "red"),
            Wine("Chardonnay", 70, "white"),
        ]

    def list_all(self):
        return self._wines

    def find_by_name(self, name):
        return next((w for w in self._wines if w.name == name), None)

    def filter_by_type(self, wine_type):
        return [w for w in self._wines if w.type == wine_type]
```

---

### Application State

```python
class WineStoreApp:
    def __init__(self):
        self.catalog = WineRepository()
        self.cart = []
```

---

## 🔧 Transaction Examples

### ListWines

```python
from guara import AbstractTransaction

class ListWines(AbstractTransaction):
    def do(self):
        wines = self.app.catalog.list_all()
        return [wine.name for wine in wines]
```

---

### FilterWines

```python
class FilterWines(AbstractTransaction):
    def do(self, of_type):
        wines = self.app.catalog.filter_by_type(of_type)
        return [{"name": w.name, "type": w.type} for w in wines]
```

---

### ViewWineDetails

```python
class ViewWineDetails(AbstractTransaction):
    def do(self, of_name):
        wine = self.app.catalog.find_by_name(of_name)
        if not wine:
            return "Wine not found"

        return {
            "name": wine.name,
            "price": wine.price,
            "type": wine.type
        }
```

---

### AddWineToCart

```python
class AddWineToCart(AbstractTransaction):
    def do(self, with_name, with_quantity):
        wine = self.app.catalog.find_by_name(with_name)

        if not wine:
            return "Wine not found"

        for _ in range(with_quantity):
            self.app.cart.append(wine)

        return f"{with_quantity}x {with_name} added"
```

---

### RemoveWineFromCart

```python
class RemoveWineFromCart(AbstractTransaction):
    def do(self, with_name):
        self.app.cart = [w for w in self.app.cart if w.name != with_name]
        return f"{with_name} removed"
```

---

### ViewCart

```python
class ViewCart(AbstractTransaction):
    def do(self):
        return [wine.name for wine in self.app.cart]
```

---

### CalculateTotal

```python
class CalculateTotal(AbstractTransaction):
    def do(self):
        return sum(wine.price for wine in self.app.cart)
```

---

### Checkout

```python
class Checkout(AbstractTransaction):
    def do(self):
        if not self.app.cart:
            return "Cart is empty"

        total = sum(wine.price for wine in self.app.cart)
        self.app.cart.clear()

        return f"Purchase successful. Total: {total}"
```

---

## 🧪 Using Use Cases as Tests

The same use cases can be executed to validate behavior:

```python
in_wine_app.when(AddWineToCart, with_name="Pinot Noir", with_quantity=1)

in_wine_app.when(Checkout).asserts(
    it.Contains, "Purchase successful"
)
```

This eliminates the need to rewrite tests separately.

---

## 🔄 One Language, Multiple Purposes

Guará enables a unified approach:

| Purpose        | How it is achieved              |
| -------------- | ------------------------------- |
| Requirements   | Use cases with `when(...)`      |
| Implementation | Transactions as Python classes  |
| Testing        | Assertions with `.asserts(...)` |

---

## 🚀 Benefits

* Single source of truth
* High readability
* Faster development cycle
* Strong alignment between business and code
* Reduced duplication

---

## 📌 Conclusion

Guará allows you to model your system using **use cases that are directly executable**.

With this approach:

1. You write use cases using `when(...)`
2. You implement transactions
3. You validate behavior with `asserts(...)`

There is no separation between **what the system should do** and **how it is implemented**.

---

## 💡 Final Thought

If a new requirement appears, you simply write:

```python
in_wine_app.when(AddWineToCart, with_name="Syrah", with_quantity=2)
```

Then implement the transaction.

Your **use cases become your architecture**.
