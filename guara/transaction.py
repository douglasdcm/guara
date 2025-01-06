import logging
from datetime import datetime
from typing import Any, NoReturn
from selenium.webdriver.remote.webdriver import WebDriver
from guara.it import IAssertion

LOGGER = logging.getLogger(__name__)


class AbstractTransaction:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    def do(self, **kwargs) -> Any | NoReturn:
        raise NotImplementedError


class Application:
    """This is the runner of the automation."""

    def __init__(self, driver):
        self._driver = driver
        self._result = None

    @property
    def result(self):
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs):
        """It executes the `do` method of each transaction"""

        LOGGER.info(f"{datetime.now()} Transaction '{transaction.__name__}'")
        for k, v in kwargs.items():
            LOGGER.info(f" {k}: {v}")

        self._result = transaction(self._driver).do(**kwargs)
        return self

    def asserts(self, it: IAssertion, expected):
        """The `asserts` method receives a reference to an `IAssertion` instance.
        It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
        It validates the result using the `asserts` method."""
        LOGGER.info(f"{datetime.now()} Assertion '{it.__name__}'")
        LOGGER.info(f" actual:   '{self._result}'")
        LOGGER.info(f" expected: '{expected}'")

        it().asserts(self._result, expected)
        return self
