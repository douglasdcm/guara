from guara.utils import is_dry_run, get_retries_on_failure


def test_is_dry_run_enabled():
    assert is_dry_run(True) is True


def test_is_dry_run_disabled_by_default():
    assert is_dry_run(False) is False


def test_get_retries_on_failure_valid_int():
    # Note: Ensure your utility returns int or handle the string
    assert int(get_retries_on_failure(3)) == 3


def test_get_retries_on_failure_invalid_returns_default():
    # Should fall back to 0 or original value
    result = get_retries_on_failure("not-a-number")
    assert int(result) == 0 if isinstance(result, str) else result == 0
