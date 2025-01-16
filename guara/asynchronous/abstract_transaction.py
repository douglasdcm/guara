"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser context using
Selenium.

Authors:
    douglasdcm
    Darkness4869
"""
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any, NoReturn, Union, Dict, Coroutine


class AbstractTransaction:
    """
    It will handle web transactions in an automated browser
    context using Selenium.
    """
    def __init__(self, driver: WebDriver):
        """
        Initializing the transaction which will allow it to interact
        with the web driver.

        Parameters:
            driver: WebDriver: It is the web driver that controls a browser by sending commands to a remote server.
        """
        self._driver: WebDriver = driver

    async def do(self, **kwargs: Dict[str, Any]) -> Coroutine[Union[Any, NoReturn]]:
        """
        It performs a specific transaction

        Parameters:
            kwargs: dict: It contains all the necessary data and parameters for the transaction.

        Returns:
            Any | NoReturn
        """
        raise NotImplementedError