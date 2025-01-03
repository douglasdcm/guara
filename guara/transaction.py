import logging
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
    def __init__(self, driver):
        self._driver = driver

    @property
    def result(self):
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs):
        LOGGER.info(f"Transaction '{transaction.__name__}'")
        for k, v in kwargs.items():
            LOGGER.info(f" {k}: {v}")

        self._result = transaction(self._driver).do(**kwargs)
        return self

    def asserts(self, it: IAssertion, expected):
        LOGGER.info(f"Assertion '{it.__name__}'")
        LOGGER.info(f" actual:   '{self._result}'")
        LOGGER.info(f" expected: '{expected}'")
        LOGGER.info("---")

        it().asserts(self._result, expected)
        return self
