# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import asyncio
from typing import Any, Type, Optional
import logging

logger = logging.getLogger(__name__)

class AbstractTransaction:
    def __init__(self, driver: Any):
        self._driver = driver

    async def do(self, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement do()")

class TransactionExecutor:
    def __init__(self, transaction: AbstractTransaction, kwargs: dict):
        self._transaction = transaction
        self._kwargs = kwargs
        self._result = None

    async def execute(self) -> Any:
        """Execute the transaction, handling both sync and async do methods."""
        logger.info(f"Transaction: {self._transaction.__class__.__name__}")
        for key, value in self._kwargs.items():
            logger.info(f" {key}: {value}")
        if asyncio.iscoroutinefunction(self._transaction.do):
            self._result = await self._transaction.do(**self._kwargs)
        else:
            self._result = self._transaction.do(**self._kwargs)
        return self._result

    def asserts(self, assertion: Any, expected: Any) -> "TransactionExecutor":
        """Run an assertion on the transaction result."""
        if hasattr(assertion, 'asserts'):  # Check if it's an IAssertion class
            assertion_instance = assertion()
            assertion_instance.asserts(self._result, expected)
        else:
            assertion(self._result, expected)
        return self

class Application:
    def __init__(self, driver: Any):
        self._driver = driver
        self._result = None

    async def at(self, transaction_cls: Type[AbstractTransaction], **kwargs) -> TransactionExecutor:
        """Set up and execute a transaction asynchronously."""
        transaction = transaction_cls(self._driver)
        executor = TransactionExecutor(transaction, kwargs)
        self._result = await executor.execute()
        return executor

    @property
    def result(self) -> Optional[Any]:
        return self._result