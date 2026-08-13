# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from typing import ClassVar

from pytest import raises

from guara import it
from guara.policy import ApplicationPolicy, TransactionPolicy
from guara.transaction import AbstractTransaction, Application


class Error(Exception):
    pass


class Repository:
    loggedin = True
    manager = True
    product = False


class IsUserLoggedIn(AbstractTransaction):
    def do(self, r: Repository):
        if not r.loggedin:
            raise Error("not logged in")


class IsManager(AbstractTransaction):
    def do(self, r: Repository):
        if not r.manager:
            Error("not manager")


class AreValidValuesToRegistreProduct(AbstractTransaction):
    def do(self, minimum_stock, r):
        assert minimum_stock is not None


class HasNotRegistredProduct(AbstractTransaction):
    def do(self, r: Repository):
        if r.product:
            raise Error("product already exist")


class ProductExists(AbstractTransaction):
    def do(self, name, r: Repository):
        assert name is not None
        if not r.product:
            raise Error("product not exist")


class CreateProduct(AbstractTransaction):
    def do(self, name, price, minimum_stock, sold_by_weight, r: Repository):
        r.product = True
        return r.product


def test_transaction_run_requires_as_contract_in_main_operation():
    t = CreateProduct
    t.requires = [
        IsUserLoggedIn,
        IsManager,
        AreValidValuesToRegistreProduct,
        HasNotRegistredProduct,
    ]
    t.ensures = []
    Application().at(
        t, name="foo", price=100, minimum_stock=10, sold_by_weight=False, r=Repository()
    ).expects(it.IsTrue)


class IsUserLoggedInRaisesError(AbstractTransaction):
    def do(self):
        raise Error


def test_transaction_raises_error_when_run_requires():
    t = CreateProduct
    t.requires = [
        IsUserLoggedInRaisesError,
    ]
    t.ensures = []
    with raises(Error):
        Application().at(
            t,
            name="foo",
            price=100,
            minimum_stock=10,
            sold_by_weight=False,
            r=Repository(),
        ).expects(it.IsTrue)


def test_transaction_run_ensures_as_contract_in_main_operation():
    t = CreateProduct
    t.requires = []
    t.ensures = [
        ProductExists,
    ]

    Application().at(
        t, name="foo", price=100, minimum_stock=10, sold_by_weight=False, r=Repository()
    ).expects(it.IsTrue)


class ProductExistsRaisesError(AbstractTransaction):
    def do(self, name, r: Repository):
        raise Error


def test_transaction_raises_error_when_run_ensures():
    t = CreateProduct
    t.requires = []
    t.ensures = [
        ProductExistsRaisesError,
    ]

    with raises(Error):
        Application().at(
            t,
            name="foo",
            price=100,
            minimum_stock=10,
            sold_by_weight=False,
            r=Repository(),
        ).expects(it.IsTrue)


class CreateProductWithInnerContract(AbstractTransaction):
    requires: ClassVar = [IsManager]
    ensures: ClassVar = [ProductExists]

    def do(self, name, price, minimum_stock, sold_by_weight, r: Repository):
        r.product = True
        return True


def test_transaction_works_with_inner_requires_and_ensures():
    Application().at(
        CreateProductWithInnerContract,
        name="foo",
        price=100,
        minimum_stock=10,
        sold_by_weight=False,
        r=Repository(),
    ).expects(it.IsTrue)


class MyTransaction(AbstractTransaction):
    requires: ClassVar = [IsUserLoggedInRaisesError]
    ensures: ClassVar = [ProductExistsRaisesError]
    execution_policy: ClassVar = TransactionPolicy(return_on_dry_run="anything")

    def do(self):
        raise PermissionError()


def test_application_do_not_run_ensures_and_requires_when_disabled():
    app = Application(execution_policy=ApplicationPolicy(disable=True))
    (
        app.given(MyTransaction)
        .at(MyTransaction)
        .when(MyTransaction)
        .and_(MyTransaction)
        .so(MyTransaction)
        .execute(MyTransaction)
        .asserts(it.IsEqualTo, "anything")
        .expects(it.IsEqualTo, "anything")
        .then(it.IsEqualTo, "anything")
        .undo()
    )


def test_application_do_not_run_ensures_and_requires_when_dry_run():
    app = Application(execution_policy=ApplicationPolicy(dry_run=True))
    (
        app.given(MyTransaction)
        .at(MyTransaction)
        .when(MyTransaction)
        .and_(MyTransaction)
        .so(MyTransaction)
        .execute(MyTransaction)
        .asserts(it.IsEqualTo, "anything")
        .expects(it.IsEqualTo, "anything")
        .then(it.IsEqualTo, "anything")
        .undo()
    )
