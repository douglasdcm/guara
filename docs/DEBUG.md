# Debugging

Errors in assertions are printed like this. Got the same example above. Notice the `actual` and `expected` values do not match.

```shell
_____________________________________________________________ test_google_search _____________________________________________________________

setup_app = <guara.transaction.Application object at 0x7f3c42bf6f90>

    def test_google_search(setup_app):
        app = setup_app
>       app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "ALL")

test_tmp.py:30: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv/lib/python3.11/site-packages/guara/transaction.py:27: in asserts
    it().asserts(self._result, expected)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <test_tmp.IsEqualToVariationsOf object at 0x7f3c4349fc10>, actual = 'alls', expected = 'all'

    def asserts(self, actual, expected):
>       assert actual.lower() == expected.lower()
E       AssertionError: assert 'alls' == 'all'
E         
E         - alls
E         ?    -
E         + all

```