# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from typing import ClassVar

from guara import it
from guara.transaction import AbstractTransaction, Application


class IsUserLoggedIn(AbstractTransaction):
    def do(self):
        pass


class IsManager(AbstractTransaction):
    def do(self):
        pass


class AreValidValuesToRegistreProduct(AbstractTransaction):
    def do(self, minimum_stock):
        assert minimum_stock is not None


class HasNotRegistredProduct(AbstractTransaction):
    def do(self):
        pass


class ProductExists(AbstractTransaction):
    def do(self, name):
        assert name is not None


class CreateProduct(AbstractTransaction):
    requires: ClassVar = [
        IsUserLoggedIn,
        IsManager,
        AreValidValuesToRegistreProduct,
        HasNotRegistredProduct,
    ]

    ensures: ClassVar = [
        ProductExists,
    ]

    def do(self, name, price, minimum_stock, sold_by_weight):
        return True


def test_transaction_run_required_preconditions_before_main_operation():
    Application().at(
        CreateProduct, name="foo", price=100, minimum_stock=10, sold_by_weight=False
    ).expects(it.IsTrue)
