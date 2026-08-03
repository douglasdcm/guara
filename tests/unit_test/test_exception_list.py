# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging
from unittest.mock import patch

from pytest import raises
from guara.transaction import Application, AbstractTransaction


class Error1(Exception):
    pass


class Error2(Exception):
    pass


class Error3(Exception):
    pass


class FlakyTransaction(AbstractTransaction):
    return_on_dry_run = Error1()

    def do(self, error_number):
        if error_number == 1:
            raise Error1()
        raise Error2()


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 3)
def test_application_retry_when_exception_in_list(caplog):
    caplog.set_level(logging.INFO)
    app = Application(retry_on_exceptions=(Error1))
    with raises(Error1):
        assert app.at(FlakyTransaction, error_number=1) is None
        assert "attempt 4 / 4" in caplog.text


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 3)
def test_application_not_retry_when_exception_not_in_list(caplog):
    caplog.set_level(logging.INFO)
    app = Application(retry_on_exceptions=(Error2, Error3))
    with raises(Error1):
        app.at(FlakyTransaction, error_number=1)
        assert "attempt" not in caplog.text
