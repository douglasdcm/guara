"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any, NoReturn, Union, Dict


class AbstractTransaction:
    """
    It will handle web transactions in an automated browser.
    """
    def __init__(self, driver: Any):
        """
        Initializing the transaction which will allow it to interact
        with the web driver.

        Args:
            driver: Any: It is the web driver that controls a browser by sending commands to a remote server.
        """
        self._driver: Any = driver

    @property
    def __name__(self) -> property:
        """
        The name of the transaction

        Returns:
            (str) The name of the transaction being implemented.
        """
        return self.__class__.__name__

    def do(self, **kwargs: Dict[str, Any]) -> Union[Any, NoReturn]:
        """
        It performs a specific transaction

        Args:
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Any | NoReturn)

        Raises:
            NotImplementedError: The method is not implemented in the subclass.
        """
        raise NotImplementedError