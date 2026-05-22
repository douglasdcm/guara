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
    [DEPRECATED] This method is not available starting from version `0.0.11`
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
            """Use your preferable async WebDriver.\n
            For example https://github.com/douglasdcm/caqui"""
        )


class CloseApp(AbstractTransaction):
    """
    [DEPRECATED] This method is not available starting from version `0.0.11`
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
            """Use your preferable async WebDriver.\n
            For example https://github.com/douglasdcm/caqui"""
        )
