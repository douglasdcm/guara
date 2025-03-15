# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
The module that is reponsible for the opening and closing
transactions.
"""

from guara.asynchronous.transaction import AbstractTransaction
from typing import Dict, Any


class OpenApp(AbstractTransaction):
    """
    It is the transaction for opening application.

    Not Implemented as Selenium is not executed asynchronously.
    Use your preferable asynchronous Web Driver.

    Link:
        https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver: Any):
        """
        Initializing the transaction

        Args:
            driver: (Any): The web driver
        """
        super().__init__(driver)

    async def do(self, **kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError(
            """Selenium does not support asynchronous execution.\n
            Use your preferable async WebDriver.\n
            For example https://github.com/douglasdcm/caqui"""
        )


class CloseApp(AbstractTransaction):
    """
    It is the transaction for closing application.

    Not Implemented as Selenium is not executed asynchronously.
    Use your preferable asynchronous Web Driver.

    Link:
        https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver: Any):
        """
        Initializing the transaction

        Args:
            driver: (Any): The web driver
        """
        super().__init__(driver)

    async def do(self, **kwargs: Dict[str, Any]) -> Any:
        raise NotImplementedError(
            """Selenium does not support asynchronous execution.\n
            Use your preferable async WebDriver.\n
            For example https://github.com/douglasdcm/caqui"""
        )
