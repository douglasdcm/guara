import logging
from typing import Any, NoReturn
from selenium.webdriver.remote.webdriver import WebDriver
from guara.asynchronous.it import IAssertion
from guara.utils import get_transaction_info

LOGGER = logging.getLogger(__name__)


class AbstractTransaction:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    async def do(self, **kwargs) -> Any | NoReturn:
        raise NotImplementedError


class Application:
    """
    This is the runner of the automation.
    """

    def __init__(self, driver):
        self._driver = driver
        self._result = None
        self._coroutines = []
        self._TRANSACTION = "transaction"
        self._ASSERTION = "assertion"
        self._kwargs = None
        self._transaction_name = None
        self._it = None
        self._expected = None

    @property
    def result(self):
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs):
        """It executes the `do` method of each transaction"""

        self._kwargs = kwargs
        self._transaction_name = get_transaction_info(transaction)
        coroutine = transaction(self._driver).do(**kwargs)
        self._coroutines.append({self._TRANSACTION: coroutine})

        return self

    def asserts(self, it: IAssertion, expected):
        """The `asserts` method receives a reference to an `IAssertion` instance.
        It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
        It validates the result using the `asserts` method."""

        self._it = it
        self._expected = expected
        coroutine = it().validates(self, expected)
        self._coroutines.append({self._ASSERTION: coroutine})

        return self

    async def perform(self) -> "Application":
        """Executes the coroutines in order and saves the result of the transaction
        in `result`"""
        for coroutine in self._coroutines:
            if coroutine.get(self._TRANSACTION):
                LOGGER.info(f"Transaction '{self._transaction_name}'")
                for k, v in self._kwargs.items():
                    LOGGER.info(f" {k}: {v}")
                self._result = await coroutine.get(self._TRANSACTION)
                continue

            LOGGER.info(f"Assertion '{self._it.__name__}'")
            LOGGER.info(f" actual:   '{self._result}'")
            LOGGER.info(f" expected: '{self._expected}'")
            await coroutine.get(self._ASSERTION)
        self._coroutines.clear()
        return self
