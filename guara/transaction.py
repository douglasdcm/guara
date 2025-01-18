"""
The module that has all of the transactions.
"""
from typing import Any, Dict
from guara.it import IAssertion
from guara.utils import get_transaction_info
from logging import getLogger, Logger
from guara.abstract_transaction import AbstractTransaction


LOGGER: Logger = getLogger("guara")
class Application:
    """
    This is the runner of the automation.
    """
    def __init__(self, driver: Any = None):
        """
        Initializing the application with a driver.

        Args:
            driver: (Any): This can be a web driver, the an object of the system being under test or any object where a transaction is needed.
        """
        self._driver: Any = driver
        """
        It is the driver that has a transaction.
        """
        self._result: Any = None
        """
        It is the result data of the transaction.
        """
        self._transaction: AbstractTransaction
        """
        The web transaction handler.
        """
        self._assertion: IAssertion
        """
        The assertion logic to be used for validation.
        """

    @property
    def result(self) -> Any:
        """
        It is the result data of the transaction.
        """
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Performing a transaction.

        Args:
            transaction: (AbstractTransaction): The web transaction handler.
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Application)
        """
        self._transaction = transaction(self._driver)
        transaction_info: str = get_transaction_info(self._transaction)
        LOGGER.info(f"Transaction: {transaction_info}")
        for key, value in kwargs.items():
            LOGGER.info(f" {key}: {value}")
        self._result = self._transaction.do(**kwargs)
        return self

    def asserts(self, assertion: IAssertion, expected: Any) -> "Application":
        """
        Asserting and validating the data by implementing the
        Strategy Pattern from the Gang of Four.
        
        Args:
            assertion: (IAssertion): The assertion logic to be used for validation.
            expected: (Any): The expected data.

        Returns:
            (Application)
        """
        self._assertion = assertion()
        self._assertion.validates(self._result, expected)
        return self
