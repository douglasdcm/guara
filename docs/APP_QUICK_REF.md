# Application class – Quick Reference

## Attributes

| Name   | Description                                        |
| ------ | -------------------------------------------------- |
| result | Stores the result of the last executed transaction |

---

## Execution Methods

| Method  | Description                                     |
| ------- | ----------------------------------------------- |
| at      | Executes a transaction and stores its result    |
| given   | Alias of `at`, used for preconditions           |
| when    | Alias of `at`, used for main actions            |
| and_    | Alias of `at`, used to chain additional actions |
| execute | Alias of `at`, generic execution method         |

---

## Assertion Methods

| Method  | Description                                       |
| ------- | ------------------------------------------------- |
| asserts | Validates the result using an assertion           |
| expects | Alias of `asserts`                                |
| then    | Alias of `asserts`, used for readability in flows |

---

## Control Methods

| Method | Description                                    |
| ------ | ---------------------------------------------- |
| undo   | Reverts executed transactions in reverse order |
