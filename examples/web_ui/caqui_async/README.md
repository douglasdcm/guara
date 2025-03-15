# Introduction
[Caqui](https://github.com/douglasdcm/caqui) is an agnostic (Desktop, Mobile and Web) driver which performs sync and async operations on UIs.

The folder `asynchronous` contains the example of asynchronous execution using [Caqui](https://github.com/douglasdcm/caqui). The folder `synchronous` is the same synchronous test for performance comparison

# Asynchronous Testing with Caqui and Guara

This project showcases the implementation of asynchronous testing using [Caqui](https://github.com/douglasdcm/caqui) and Guará. The test suite automates the retrieval and verification of web page links using the Page Transactions (PT) pattern.

## Project Overview

The test suite leverages asynchronous transactions to:
- Open a local HTML file in a Chrome browser session.
- Retrieve all links from the page.
- Validate expected link outputs.
- Perform tests on multiple asynchronous pages.
- Close the browser session upon completion.

## Code Explanation

### **Test Setup**

- The `setup_test` fixture initializes a Chrome browser session using Caqui.
- It retries session creation up to five times if the connection fails.
- An `Application` instance is created using Guara's transaction mechanism.
- The test loads `sample.html` from the local filesystem and verifies the page title.

### **Test Execution**

- The `_run_it` method retrieves all links on the page and verifies their correctness.
- It iterates through the links, using the `GetNthLink` transaction to extract and validate individual links.
- The assertions ensure that the retrieved values match the expected format (`any1.com`, `any2.com`, etc.).

### **Test Cases**

- `test_async_page_1`, `test_async_page_2`, `test_async_page_3`, and `test_async_page_4` execute `_run_it` to validate link retrieval in different test cases.
- The tests run asynchronously using `pytest-asyncio`.

## Notes

- The test class is marked as `@mark.skip` to indicate that the driver should be started manually before execution.
- Logging is integrated for debugging session creation and transaction execution.
- The code follows the Page Transactions pattern, ensuring modular and scalable test flows.

