# Frequently Asked Questions (FAQ)

## Q: How do I move my legacy code to Page Transactions Pattern?  
**A:** You can do it in a safe way following the steps in this [documentation](https://guara.readthedocs.io/en/latest/MIGRATE_CODE.html).

## Q: My `do` method is too big  
**A:** Guará is Python code, so you can break the `do` method into smaller functions following patterns like Facade.

## Q: The code I want to use in a `do` method is in another `do` method  
**A:** It is Python code. You can call the transaction `do` method directly.

```python
class DoThat(AbstractTransaction):
    def do(self, ...):
        # do something I need

class DoIt(AbstractTransaction):
    def do(self, ...):
        DoThat().do(...)
```

## Q: Can I wrap many transactions in a single one?

**A:** You can use the Composite Transactions pattern to execute multiple transactions in sequence.

```python
class DoThat(AbstractTransaction):
    def do(self, **kwargs):
        return f"do that {kwargs.get('param')}"

class DoIt(AbstractTransaction):
    def do(self, **kwargs):
        return f"do it {kwargs.get('param')}"

# Composite class
class DoAll(AbstractTransaction):
    def do(self, **kwargs):
        results = []
        to_dos = [DoIt, DoThat]
        for to_do in to_dos:
            result = to_do().do(**kwargs)
            results.append(result)
        return results

Application().when(DoAll, param="foo").then(it.ContainsAll, ["do that foo", "do it foo"])
```

## Q: Does Guará support all Gherkin verbs?

**A:** No, but verbs like OR and BUT can be implemented indirectly.

```python
# Example (conceptual)
if app.execute(ActionA).result == "foo" or app.execute(ActionB).result == "bla":
   app.when(ActionC).asserts(it.IsTrue)
else:
   app.when(ActionD).asserts(it.IsTrue)
```

## Q: Does Guará only support Gherkin verbs?

**A:**

* No. It can be extended to an ubiquitous language
* It also provides native verbs like `at` and `execute` to improve readability.

## Q: Does Guará automatically validate transaction returns?

**A:** No. You must explicitly use `asserts` (or similar verbs) in your scenarios.

## Q: Can I switch to other code styles when using Guará?

**A:** Yes. It is Python code, so you can use any valid Python approach.

```python
def helper(value):
    return "value"

class MyTransaction(AbstractTransaction):
    def do(self):
        # do something

# Following Page Transactions pattern until here
result = app.when(MyTransaction).then(it.IsTrue).result

# Changing to other style from here
if result == "foo":
   my_list = helper(result)
   
for item in my_list:
   # do other things
```

## Q: Can I change the framework behavior?

**A:** Yes. It can be configured via [environment variables](https://guara.readthedocs.io/en/latest/ENVIRONMENT_VARIABLES.html).

## Q: I couldn't find a specific assertion

**A:** You can extend assertions as described in the [documentation](https://guara.readthedocs.io/en/latest/TUTORIAL.html#ubiquitous-language).

## Q: I couldn't find a specific verb

**A:** You can extend the language to create your own [ubiquitous language](https://guara.readthedocs.io/en/latest/TUTORIAL.html#ubiquitous-language).

## Q: I'm losing track of my scenarios

**A:** Move the code into modules to improve organization.

## Q: I have lots of transactions

**A:**

* Group them by categories (Actions, Preconditions, Questions, etc.)
* Move them into modules
* Create helper modules for support logic
* Use [composite transactions](https://guara.readthedocs.io/en/latest/COMPOSITE_TRANSACTIONS.html) to simplify the exposed interface

## Q: My transaction needs methods other than `do`

**A:** It is Python code. You can create additional methods. However, the framework only calls `do`. Other methods must be invoked manually or by the `do` method.

## Q: I need to store a value in a transaction to use in [`undo`](https://guara.readthedocs.io/en/latest/UNDO.html)

**A:** It is Python code. Store it as an instance attribute.

## Q: I need to undo what a transaction did

**A:** Use the `undo` method as described in the [documentation](https://guara.readthedocs.io/en/latest/UNDO.html).

## Q: Do I always need to return values in `do`?

**A:** No. Return values only when needed, such as for assertions.

## Q: How do I name my transactions for better readability?

**A:** Follow the [best practices guide](https://guara.readthedocs.io/en/latest/BEST_PRACTICES.html).

## Q: Do I always need to assert?

**A:** No. You can use methods like `execute` when assertions are not needed.

## Q: I can't see the docstring of my `do` method in scenarios

**A:** Follow the documentation best practices for structuring and documenting transactions. (link)

## Q: Can I reuse transactions in my tests?

**A:** Yes. Tests should be written using the same syntax and transactions.

## Q: Parameters in `do` were not renamed automatically by my IDE

**A:** This is a limitation of the framework. Parameters must be updated manually.
Explanation: `do` is invoked indirectly via `given`, `when`, and `then`, using `kwargs`.

## Q: Can I pass data from one transaction to another?

**A:** Not directly, but you can use the `result` property or shared storage classes.

```python
result = app.when(CreateStudent, with_name="John").result

app.when(UseStudent, student_id=result)
```

## Q: How do I improve readability?

**A:** Build scenarios using the builder approach. See [best practices](https://guara.readthedocs.io/en/latest/BEST_PRACTICES.html).

## Q: Can I automate integration tests using the framework?

**A:** Yes. See the integration testing section in the [documentation](https://guara.readthedocs.io/en/latest/TUTORIAL.html#automation-testing).
