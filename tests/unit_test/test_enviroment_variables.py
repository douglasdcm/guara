from guara.utils import get_retries_on_failure


def test_get_retries_on_failure_valid_int():
    # Note: Ensure your utility returns int or handle the string
    assert int(get_retries_on_failure(3)) == 3


def test_get_retries_on_failure_invalid_returns_default():
    # Should fall back to 0 or original value
    result = get_retries_on_failure("not-a-number")
    assert int(result) == 0 if isinstance(result, str) else result == 0
