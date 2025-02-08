# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import raises
from guara import it


def test_assert_is_equal():
    assert it.IsEqualTo().asserts("any", "any") is None


def test_assert_is_equal_raises_exception():
    with raises(AssertionError):
        assert it.IsEqualTo().asserts("any", "other")


def test_assert_is_not_equal():
    assert it.IsNotEqualTo().asserts("any", "other") is None


def test_assert_is_not_equal_raises_exception():
    with raises(AssertionError):
        assert it.IsNotEqualTo().asserts("any", "any")


def test_assert_contains():
    assert it.Contains().asserts("any other", "any") is None
    assert it.Contains().asserts(["any"], "any") is None


def test_assert_contains_raises_exception():
    with raises(AssertionError):
        assert it.Contains().asserts("any", "other")


def test_assert_does_not_contain():
    assert it.DoesNotContain().asserts("any other", "foo") is None


def test_assert_does_not_contains_raises_exception():
    with raises(AssertionError):
        assert it.DoesNotContain().asserts("any other", "any")


def test_assert_has_key_value():
    actual = {"any-key": "any-value", "other-key": "other-value"}
    expected = {"any-key": "any-value"}
    assert it.HasKeyValue().asserts(actual, expected) is None


def test_assert_has_key_value_raises_exception():
    actual = {"any-key": "any-value", "other-key": "other-value"}
    expected = {"no-key": "no-value"}
    with raises(AssertionError):
        assert it.HasKeyValue().asserts(actual, expected) is None


def test_assert_matches_regex():
    actual = "An explanation of your regex will be automatically generated as you type"
    expected = "An explanation of your regex will (.*)"
    assert it.MatchesRegex().asserts(actual, expected) is None


def test_assert_matches_regex_raises_exception():
    actual = "An explanation of your regex will be automatically generated as you type"
    expected = "do not match anything"
    with raises(AssertionError):
        assert it.MatchesRegex().asserts(actual, expected) is None


def test_assert_is_subset_list():
    actual = [
        "An",
        "explanation",
        "of",
        "your",
        "regex",
        "will",
        "be",
        "automatically",
        "generated",
        "as",
        "you",
        "type",
    ]
    expected = [
        "your",
        "regex",
        "will",
        "be",
        "automatically",
    ]
    assert it.HasSubset().asserts(actual, expected) is None


def test_assert_is_subset_list_raises_exception():
    actual = [
        "An",
        "explanation",
        "of",
        "your",
        "regex",
        "will",
        "be",
        "automatically",
        "generated",
        "as",
        "you",
        "type",
    ]
    expected = [
        "your",
        "regex",
        "INVALID",
        "DATA",
        "will",
        "be",
        "automatically",
    ]
    with raises(AssertionError):
        assert it.HasSubset().asserts(actual, expected) is None


def test_assert_is_sorted_list():
    actual = [
        "An",
        "explanation",
        "of",
        "your",
        "regex",
        "will",
        "be",
        "automatically",
        "generated",
        "as",
        "you",
        "type",
    ]
    expected = [
        "An",
        "explanation",
        "of",
        "your",
        "regex",
        "will",
        "be",
        "automatically",
        "generated",
        "as",
        "you",
        "type",
    ]
    assert it.IsSortedAs().asserts(actual, expected) is None


def test_assert_is_sorted_list_raises_exception():
    actual = [
        "An",
        "explanation",
        "of",
        "your",
        "regex",
        "will",
        "be",
        "automatically",
        "generated",
        "as",
        "you",
        "type",
    ]
    expected = [
        "type",
        "you",
        "as",
        "generated",
        "automatically",
        "be",
        "will",
        "regex",
        "your",
        "of",
        "explanation",
        "An",
    ]
    with raises(AssertionError):
        assert it.IsSortedAs().asserts(actual, expected) is None
