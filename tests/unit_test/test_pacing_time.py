# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from guara.transaction import AbstractTransaction


class ValidateLocal(AbstractTransaction):
    def do(self):
        pass

@mark.parametrize("value", ["invalid", -1, True])
def test_transactions_returns_none_when_invalid_retry(value):
    t = ValidateLocal()
    t.pacing_time = value
    assert t.pacing_time is None