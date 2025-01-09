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

    @property
    def result(self):
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs):
        """It executes the `do` method of each transaction"""

        LOGGER.info(f"Transaction '{get_transaction_info(transaction)}'")
        for k, v in kwargs.items():
            LOGGER.info(f" {k}: {v}")

        coroutine = transaction(self._driver).do(**kwargs)
        self._coroutines.append({self._TRANSACTION: coroutine})

        return self

    def asserts(self, it: IAssertion, expected):
        """The `asserts` method receives a reference to an `IAssertion` instance.
        It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
        It validates the result using the `asserts` method."""

        LOGGER.info(f"Assertion '{it.__name__}'")
        LOGGER.info(f" actual:   '{self._result}'")
        LOGGER.info(f" expected: '{expected}'")

        coroutine = it().asserts(self, expected)
        self._coroutines.append({self._ASSERTION: coroutine})

        return self

    async def perform(self) -> "Application":
        """Executes the coroutines in order and saves the result of the transaction
        in `result`"""

        for coroutine in self._coroutines:
            if coroutine.get(self._TRANSACTION):
                self._result = await coroutine.get(self._TRANSACTION)
                continue
            await coroutine.get(self._ASSERTION)
        self._coroutines.clear()
        return self
