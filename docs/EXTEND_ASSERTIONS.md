# Extending assertions

The strategies to assert the result can e extended by inheriting from `IAssertion` as following:

```python
# The code is the same of the previous session.
# The unnecessary details were not duplicated
# import IAssertion 
from guara.transaction import Application, IAssertion

# Implements a new assertion to check variations of the expected value
class IsEqualToVariationsOf(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        if actual.lower() == expected.lower():
            return True
        raises AssertionError

def test_google_search(setup_app):
    app = setup_app
    
    # The new assertion is used to check variations of 'All', like 'aLL' or 'ALL'
    app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "All")

```