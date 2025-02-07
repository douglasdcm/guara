# Introduction
[Splinter](https://splinter.readthedocs.io/en/stable/) is a Python framework that provides a simple and consistent interface for web application automation.

# Splinter Integration Testing with Guara

This project demonstrates how to integrate [Splinter](https://splinter.readthedocs.io/en/stable/) with **Guará's Page Transactions (PT) pattern** to test a local HTML page.

## Code Breakdown

### **Imports**
- `pathlib`: Determines the file path of the test HTML file.
- `random`: Selects a random test input.
- `splinter.Browser`: Provides browser automation functionality.
- `guara.transaction.Application`: Manages transactions within the Guará framework.
- `guara.it`: Provides assertion utilities.
- `examples.web_ui.splinter.setup`: Contains transaction definitions for opening and closing the browser.
- `examples.web_ui.splinter.home`: Contains transactions for interacting with the home page.

---

## **Test Class: `TestSplinterIntegration`**
This class contains tests for verifying text submission functionality on a local web page.

### **Setup Method (`setup_method`)**
1. Determines the file path of the `sample.html` test page.
2. Initializes a headless Chrome browser using **Splinter**.
3. Creates a **Guará Application** instance using the browser.
4. Opens the local web page using the `setup.OpenSplinterApp` transaction.

### **Teardown Method (`teardown_method`)**
- Closes the application using `setup.CloseSplinterApp` to ensure proper cleanup after each test.

---

## **Test Case: `test_local_page`**
This test verifies the text input functionality on the web page.
1. Selects a random text from the list: `["cheese", "splinter", "test", "bla", "foo"]`.
2. Submits the selected text using `home.SubmitTextSplinter`.
3. **Assertions:**
   - Ensures the page displays `"It works! {text}!"`, confirming the correct input was processed.
   - Ensures the output is **not** `"Any"`, verifying the system does not accept incorrect text.

---

## **Summary**
- The test automates interactions with a local **HTML page**.
- Uses **Splinter** to control a **headless Chrome browser**.
- Implements the **Guará PT pattern** for structured UI automation.
- Tests whether submitting text produces the correct output.

