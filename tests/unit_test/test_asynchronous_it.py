import pytest

from guara.asynchronous.it import (
    Contains,
    DoesNotContain,
    IsEqualTo,
    IsNotEqualTo,
)


class Result:
    def __init__(self, result):
        self.result = result


@pytest.mark.asyncio
async def test_is_equal_to_passes_when_results_are_equal():
    actual = Result(10)

    await IsEqualTo().asserts(actual, 10)


@pytest.mark.asyncio
async def test_is_equal_to_fails_when_results_are_different():
    actual = Result(10)

    with pytest.raises(AssertionError):
        await IsEqualTo().asserts(actual, 20)


@pytest.mark.asyncio
async def test_is_not_equal_to_passes_when_results_are_different():
    actual = Result(10)

    await IsNotEqualTo().asserts(actual, 20)


@pytest.mark.asyncio
async def test_is_not_equal_to_fails_when_results_are_equal():
    actual = Result(10)

    with pytest.raises(AssertionError):
        await IsNotEqualTo().asserts(actual, 10)


@pytest.mark.asyncio
async def test_contains_passes_when_expected_is_in_result():
    actual = Result([1, 2, 3])

    await Contains().asserts(actual, 2)


@pytest.mark.asyncio
async def test_contains_fails_when_expected_is_not_in_result():
    actual = Result([1, 2, 3])

    with pytest.raises(AssertionError):
        await Contains().asserts(actual, 4)


@pytest.mark.asyncio
async def test_does_not_contain_passes_when_expected_is_not_in_result():
    actual = Result([1, 2, 3])

    await DoesNotContain().asserts(actual, 4)


@pytest.mark.asyncio
async def test_does_not_contain_fails_when_expected_is_in_result():
    actual = Result([1, 2, 3])

    with pytest.raises(AssertionError):
        await DoesNotContain().asserts(actual, 2)
