from typing import Any, NoReturn
from selenium.webdriver.remote.webdriver import WebDriver
from guara.it import IAssertion


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
        self._result = transaction(self._driver).do(**kwargs)
        return self

    def asserts(self, it: IAssertion, expected):
        it().asserts(self._result, expected)
        return self
