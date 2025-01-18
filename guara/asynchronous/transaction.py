"""
The module that has all of the transactions.
"""
from typing import Any, List, Dict, Coroutine, Union
from guara.asynchronous.it import IAssertion
from guara.utils import get_transaction_info
from logging import getLogger, Logger
from guara.asynchronous.abstract_transaction import AbstractTransaction, WebDriver

LOGGER: Logger = getLogger("guara")
class Application:
    """
    The runner of the automation.
    """
    def __init__(self, driver: Any):
        """
        Initializing the application with a driver.

        Parameters:
            driver: Any: This can be a web driver, the an object of the system being under test or any object where a transaction is needed.
        """
        self._driver: Any = driver
        """
        It is the driver that has a transaction.
        """
        self._result: Any = None
        """
        It is the result data of the transaction.
        """
        self._coroutines: List[Dict[str, Union[Coroutine[None, None, Any], Coroutine[None, None, None]]]] = []
        """
        The list of transactions that are performed.
        """
        self._TRANSACTION: str = "transaction"
        """
        Transaction header
        """
        self._ASSERTION: str = "assertion"
        """
        Assertion header
        """
        self._kwargs: Dict[str, Any] = None
        """
        It contains all the necessary data and parameters for the
        transaction.
        """
        self._transaction_name: str = None
        """
        The name of the transaction.
        """
        self._it: IAssertion = None
        """
        The interface of the Assertion
        """
        self._expected: Any = None
        """
        The expected data
        """
        self.__transaction: AbstractTransaction
        """
        The web transaction handler
        """

    @property
    def result(self) -> Any:
        """
        It is the result data of the transaction.
        """
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs: Dict[str, Any]) -> "Application":
        """
        Executing each transaction.

        Parameters:
            transaction: AbstractTransaction: The web transaction handler.
            kwargs: dict: It contains all the necessary data and parameters for the transaction.

        Returns:
            Application
        """
        self.__transaction = transaction(self._driver)
        self._kwargs = kwargs
        self._transaction_name = get_transaction_info(self.__transaction)
        coroutine: Coroutine[None, None, Any] = self.__transaction.do(**kwargs)
        self._coroutines.append({self._TRANSACTION: coroutine})
        return self

    def asserts(self, it: IAssertion, expected: Any) -> "Application":
        """
        Asserting the data that is performed by the transaction
        against its expected value.

        Parameters:
            it: IAssertion: The interface of the Assertion.
            expected: Any: The expected data.

        Returns:
            Application
        """
        self._it = it
        self._expected = expected
        coroutine: Coroutine[None, None, None] = self._it.validates(self, expected)
        self._coroutines.append({self._ASSERTION: coroutine})
        return self

    async def perform(self) -> "Application":
        """
        Executing all of the coroutines.

        Returns:
            Application
        """
        for index in range(0, len(self._coroutines), 1):
            await self.getAssertion(index) if not await self.getTransaction(index) == False else None
        self._coroutines.clear()
        return self

    async def getTransaction(self, index: int) -> Coroutine[None, None, bool]:
        """
        Retrieving the transaction from the coroutine.

        Parameters:
            index: int: The index of the current coroutine.

        Returns:
            boolean
        """
        transaction: Coroutine[None, None, Any] = self._coroutines[index].get(self._TRANSACTION)
        if transaction:
            LOGGER.info(f"Transaction: {self._transaction_name}")
            for key, value in self._kwargs.items():
                LOGGER.info(f"{key}: {value}")
            self._result = await transaction
            return True
        return False

    async def getAssertion(self, index: int) -> Coroutine[None, None, None]:
        """
        Retrieving the assertion from the coroutine.

        Parameters:
            index: int: The index of the current coroutine.

        Returns:
            None
        """
        LOGGER.info(f"Assertion: {self._it.__name__}")
        LOGGER.info(f"Actual: {self._result}")
        LOGGER.info(f"Expected: {self._expected}")
        return self._coroutines[index].get(self._ASSERTION)