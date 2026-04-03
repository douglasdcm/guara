import os
from unittest.mock import patch
from guara.utils import is_dry_run, get_retries_on_failure

def test_is_dry_run_enabled():
    with patch.dict(os.environ, {"DRY_RUN": "true"}):
        assert is_dry_run() is True

def test_is_dry_run_disabled_by_default():
    with patch.dict(os.environ, {}, clear=True):
        assert is_dry_run() is False

def test_get_retries_on_failure_valid_int():
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "3"}):
        # Note: Ensure your utility returns int or handle the string
        assert int(get_retries_on_failure()) == 3

def test_get_retries_on_failure_invalid_returns_default():
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "not-a-number"}):
        # Should fall back to 0 or original value
        result = get_retries_on_failure()
        assert int(result) == 0 if isinstance(result, str) else result == 0