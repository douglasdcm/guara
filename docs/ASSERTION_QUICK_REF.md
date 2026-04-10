# Assertions – Quick Reference

## Basic Assertions

| Assertion    | Description                                 |
| ------------ | ------------------------------------------- |
| IsEqualTo    | Checks if actual is equal to expected       |
| IsNotEqualTo | Checks if actual is different from expected |
| IsTrue       | Checks if actual evaluates to True          |
| IsFalse      | Checks if actual evaluates to False         |
| IsNone       | Checks if actual is None                    |
| IsNotNone    | Checks if actual is not None                |

---

## Collection Assertions

| Assertion      | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| IsEmpty        | Checks if a collection is empty                              |
| IsNotEmpty     | Checks if a collection is not empty                          |
| HasLength      | Checks if a collection has a specific length                 |
| Contains       | Checks if a value exists in a collection                     |
| DoesNotContain | Checks if a value does not exist in a collection             |
| ContainsAll    | Checks if all expected values exist in a collection          |
| ContainsAny    | Checks if at least one expected value exists in a collection |
| HasSubset      | Checks if expected values are a subset of actual             |

---

## Numeric Assertions

| Assertion     | Description                                       |
| ------------- | ------------------------------------------------- |
| IsGreaterThan | Checks if actual is greater than expected         |
| IsLessThan    | Checks if actual is less than expected            |
| IsBetween     | Checks if actual is within a range (inclusive)    |
| IsCloseTo     | Checks if actual is within a tolerance of a value |

---

## String Assertions

| Assertion    | Description                                   |
| ------------ | --------------------------------------------- |
| StartsWith   | Checks if actual starts with a prefix         |
| EndsWith     | Checks if actual ends with a suffix           |
| MatchesRegex | Checks if actual matches a regular expression |
| IsBlank      | Checks if string is empty or whitespace       |
| IsNotBlank   | Checks if string is not empty or whitespace   |

---

## State Assertions

| Assertion     | Description                                          |
| ------------- | ---------------------------------------------------- |
| HasChanged    | Checks if value changed from a previous value        |
| HasNotChanged | Checks if value did not change from a previous value |

---

## Advanced Assertions

| Assertion   | Description                                      |
| ----------- | ------------------------------------------------ |
| Satisfies   | Checks if actual satisfies a custom condition    |
| IsSortedAs  | Checks if actual matches expected order          |
| HasKeyValue | Checks if a dictionary contains a key-value pair |
