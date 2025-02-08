# Introduction
[Helium](https://github.com/mherrmann/helium) is lighter web automation with Python. It is a library for automating browsers such as Chrome and Firefox.

# Helium Integration Testing with Guara

This project demonstrates how to integrate [Helium](https://github.com/mherrmann/helium) with Guará for web UI testing using the Page Transactions (PT) pattern. The test suite automates interactions with a local HTML page and verifies expected behaviors.

## Project Overview

The test suite automates the following actions:
- Launches a local HTML page in a browser using Helium.
- Submits randomized text input.
- Validates expected and unexpected outcomes.
- Closes the browser session upon completion.

## Code Explanation

### **Test Setup**

- The `setup_method` initializes a Guara `Application` instance.
- It opens a local HTML file (`sample.html`) for testing.

### **Test Execution**

- The `test_local_page` method selects a random text string from a predefined list.
- It submits the text using `home.SubmitText` and asserts that the displayed result matches the expected output.
- Additional assertions verify that the result does not match an arbitrary incorrect value (`"Any"`).

### **Teardown**

- The `teardown_method` ensures that the application is closed properly after test execution.

## Notes

- The test follows the Page Transactions pattern to ensure modular and maintainable test automation.
- The approach eliminates direct element manipulation, relying instead on predefined transactions for stability and reusability.

