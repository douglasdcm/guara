"""
The module that is reponsible for the opening and closing
transactions.
"""
from guara.asynchronous.transaction import AbstractTransaction, WebDriver
from typing import Dict, Any


class OpenApp(AbstractTransaction):
    """
    It is the transaction for opening application.

    Not Implemented as Selenium is not executed asynchronously.
    Use your preferable asynchronous Web Driver.
    
    Link:
        https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver: WebDriver):
        """
        Initializing the transaction

        Parameters:
            driver: WebDriver: The web driver
        """
        super().__init__(driver)

    async def do(self, **kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError("Selenium does not support asynchronous execution.\nUse your preferable async WebDriver.\nFor example https://github.com/douglasdcm/caqui")

class CloseApp(AbstractTransaction):
    """
    It is the transaction for closing application.

    Not Implemented as Selenium is not executed asynchronously.
    Use your preferable asynchronous Web Driver.
    
    Link:
        https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver: WebDriver):
        """
        Initializing the transaction

        Parameters:
            driver: WebDriver: The web driver
        """
        super().__init__(driver)

    async def do(self, **kwargs: Dict[str, Any]) -> Any:
        """
        It performs a specific transaction

        Parameters:
            kwargs: dict: It contains all the necessary data and parameters for the transaction.

        Returns:
            Any
        """
        raise NotImplementedError("Selenium does not support asynchronous execution.\nUse your preferable async WebDriver.\nFor example https://github.com/douglasdcm/caqui")
