# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import os

from pytest import mark

from guara.constants import convert_variable_to_integer


@mark.parametrize(
    "value,expected", [("not-a-number", 0), ("-1", 0), ("0", 0), ("1", 1)]
)
def test_get_variable_returns_correct_values(value, expected):
    os.environ["FOO"] = value
    assert convert_variable_to_integer("FOO") == expected
