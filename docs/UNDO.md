# Undo (experimental)

The `undo` feature allows users to revert actions performed by transactions, offering a basic form of rollback support. This can be especially useful during development or testing phases where reverting a chain of changes might be necessary.

## Experimental status

Please note that `undo` is still experimental and has known limitations:

### Some actions cannot be reverted

* Certain types of transactions cannot be undone, such as:

  * Searches on web pages
  * GET requests on REST APIs
* These actions are inherently stateless or side-effect-free, and thus do not leave a trace that can be reverted.

### Explicity reversion required

* Reverting actions involves explicitly undoing them, often by:

  * Sending compensating commands to REST endpoints
  * Directly interacting with the database
* The tool will attempt to reverse operations in the reverse order of their execution, which is crucial to preserving consistency.

## How It Works

When `undo` is invoked:

1. The tool analyzes the transaction history.
2. It determines which actions are eligible for reversion.
3. It performs the necessary operations in reverse order to roll back changes.

To enable the `undo` of a transactions it is necessary to implement its `undo` method.

* All data used by the `do` method and required by the `undo` has to be placed in instance variables as in the exemple bellow. 

```python
class Get(AbstractTransaction):
    def do(self, any_param):
        self._any_param = any_param
        return f"got {any_param}"

    # It not necessary to implement the `undo` in this case

class Post(AbstractTransaction):
    def do(self, any_param):
        # Stores the parameter in a instance variable to be used by `undo` later
        self._any_param = any_param
        return client.post(any_param)

    # Implements the actions to revert the operations done by `do`
    def undo(self):
        # Uses the stored parameter
        client.delete(self._any_param)


class TestUndo:
    def setup_method(self, method):
        self._app = Application()

    def teardown_method(self, method):
        # Calls the `undo` method of the application that in turns calls the `undo` method of
        # all transactions in reverse order
        self._app.undo()

    def test_get_post_are_executed_in_reverse_order(self):
        self._app.at(Get, any_param="any").at(Post, any_param="any")

# Output
#
# 2025-05-28 00:21:02.369 INFO Transaction: test_undo.Get
# 2025-05-28 00:21:02.369 INFO  any_param: any
# 2025-05-28 00:21:02.369 INFO Transaction: test_undo.Post
# 2025-05-28 00:21:02.369 INFO  any_param: any
# --------------------------------------------------------
# 2025-05-28 00:21:02.370 INFO Reverting 'Post' actions
# 2025-05-28 00:21:02.370 INFO Reverting 'Get' actions
```

We encourage users to experiment with the `undo` feature and provide feedback. Your input will help us evolve it into a more robust and reliable capability.

Stay tuned for updates!

