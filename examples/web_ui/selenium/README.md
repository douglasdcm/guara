# Selenium Integration Testing with Guara

This project demonstrates how to integrate Selenium with Guara for web UI testing using the Page Transactions (PT) pattern. The test suite automates interactions with a local HTML page and a more complex validation workflow.

## Project Overview

The test suite automates the following actions:
- Launches a local HTML page in a headless Chrome browser.
- Switches between English and Portuguese content.
- Navigates through different sections of the page.
- Performs restricted and expanded searches.
- Verifies expected and unexpected results.

## Code Explanation

### **Test Setup**

- The `setup_method` initializes a Selenium WebDriver instance with headless Chrome.
- It opens the test page (`index.html` or `sample.html`) using the `setup.OpenApp` transaction.

### **Test Execution**

- The `test_vpm_transaction_chain` method:
  - Changes the page language to Portuguese and verifies the content.
  - Switches back to English and asserts the expected text.
  - Navigates to the "Info" and "Contact" pages, verifying content correctness.
  - Conducts restricted and expanded searches and validates similarity results.

- The `test_vpm_transaction_builder` method follows a similar flow but leverages chained transactions for improved readability and maintainability.

- The `test_local_page` method:
  - Selects a random text from a predefined list.
  - Submits the text and validates the displayed output.
  - Ensures incorrect text is not mistakenly accepted.

### **Teardown**

- The `teardown_method` ensures proper closure of the application after test execution.

## Notes

- The test follows the Page Transactions pattern for modular and maintainable test automation.
- The `@fixture` method `setup_application` provides an alternative approach for initializing the test environment.
- Assertions verify expected behavior, improving test reliability.

