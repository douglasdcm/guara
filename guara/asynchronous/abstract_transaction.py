"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser.
"""
from typing import Any, NoReturn, Union, Dict


class AbstractTransaction:
    """
    It will handle web transactions in an automated browser
    context using Selenium.
    """
    def __init__(self, driver: Any):
        """
        Initializing the transaction which will allow it to interact
        with the web driver.

        Args:
            driver: (Any): It is the web driver that controls a browser by sending commands to a remote server.
        """
        self._driver: Any = driver

    async def do(self, **kwargs: Dict[str, Any]) -> Union[Any, NoReturn]:
        """
        It performs a specific transaction

        Args:
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Any | NoReturn)
        """
        raise NotImplementedError