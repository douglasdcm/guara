[undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) is a tool to evade bot detection mechanisms in Chrome.

# undetected-chromedriver Integration Testing with Guara

This project demonstrates how to integrate **undetected-chromedriver** with **Guará's Page Transactions (PT) pattern** to automate interactions with a web application.

## Project Structure

project-root/ │── examples/ │ ├── web/ │ │ ├── undetected_chromedriver/ │ │ │ ├── setup.py # Contains setup transactions │ │ │ ├── actions.py # Contains actions transactions │── test_undetected_chromedriver.py # The test script


## Code Breakdown

### **Imports**
- `pytest`: Provides test framework functionality.
- `guara.transaction.Application`: Manages transactions within the Guará framework.
- `guara.it`: Provides assertion utilities.

---

## **Test Class: `TestUndetectedChromeDriver`**
This class automates interactions with a web application using **undetected-chromedriver**.

### **Setup Method `setup_method`**
1. Imports `setup` transactions from `examples.web.undetected_chromedriver`.
2. Initializes a **Guará Application** instance using **undetected-chromedriver**.
3. Opens the browser using `setup.OpenBrowserTransaction`.

### **Teardown Method `teardown_method`**
- Closes the browser after each test using `setup.CloseBrowserTransaction`.

---

## **Test Case: `test_google_search`**
This test verifies that Google search operations are successfully performed using **undetected-chromedriver**.
1. Imports the `actions` transaction module from `examples.web.undetected_chromedriver`.
2. Defines the test input query.
3. Performs the Google search using `actions.SearchGoogle`.
4. **Assertions:**
   - Ensures the search results page is displayed.

---

## **Summary**
- The test automates interactions with a **web application**.
- Uses **undetected-chromedriver** to evade bot detection mechanisms.
- Implements the **Guará PT pattern** for structured automation.
