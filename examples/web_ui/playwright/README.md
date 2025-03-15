# Playwright Integration Testing with Guara

This project demonstrates how to integrate [Playwright](https://playwright.dev/python/) with Guará for web UI testing using the Page Transactions (PT) pattern. The test suite automates interactions with the Playwright documentation site and verifies expected behaviors.

## Project Overview

The test suite automates the following actions:
- Launches the Playwright documentation site.
- Navigates through different sections of the site.
- Validates expected and unexpected outcomes using assertions.

## Code Explanation

### **Test Setup**

- The `setup_method` fixture initializes a Playwright `Page` instance wrapped in a Guara `Application`.
- It opens the Playwright documentation homepage and verifies that the page contains the word "Playwright".

### **Test Execution**

- The `test_local_page_playwright` method:
  - Navigates to the "Getting Started" section and asserts that the page title is "Installation".
  - Navigates to the "Writing Tests" section and asserts that the page title is not "Writing Tests".

### **Notes**

- The test is marked with `@mark.skip` to indicate that Playwright must be installed and configured properly before execution.
- The test follows the Page Transactions pattern for modular and maintainable automation.
- Assertions ensure that navigation actions produce the expected results, making the test more robust.

