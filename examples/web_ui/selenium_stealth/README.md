# Selenium Stealth Integration Testing with Guara

This project demonstrates how to integrate [Selenium Stealth](https://pypi.org/project/selenium-stealth/) with **Guará's Page Transactions (PT) pattern** to automate interactions with a web page while avoiding bot detection mechanisms.

## Code Breakdown

### **Imports**
- `selenium.webdriver`: Manages browser automation.
- `selenium_stealth.stealth`: Helps bypass bot detection mechanisms.
- `guara.transaction.Application`: Manages transactions within the Guará framework.
- `guara.it`: Provides assertion utilities.

---

## **Test Class: `TestSeleniumStealthIntegration`**
This class automates interactions with a **local web page** using **Selenium Stealth** to evade detection.

### **Setup Method (`setup_method`)**
1. Configures **Chrome WebDriver** with options to **disable automation detection** and run in headless mode.
2. Applies **Selenium Stealth settings** to mimic a real user's environment by:
   - Setting browser languages.
   - Spoofing vendor and platform details.
   - Modifying WebGL renderer settings.
3. Initializes a **Guará Application** instance with the configured WebDriver.
4. Opens a web page (`https://example.com`) using `setup.OpenStealthBrowser`.

### **Teardown Method (`teardown_method`)**
- Closes the browser after each test using `setup.CloseStealthBrowser`.

---

## **Test Case: `test_local_page`**
This test verifies that text input is successfully processed on the web page.
1. Defines a list of sample texts.
2. Selects a **random text value** for submission.
3. Submits the text using `home.SubmitSeleniumStealth`.
4. **Assertions:**
   - Ensures the page contains "Example Domain" after text submission.
   - Ensures the result is **not equal** to an arbitrary incorrect value ("Any").

---

## **Summary**
- The test automates interactions with a **web page** while avoiding bot detection.
- Uses **Selenium Stealth** to make browser automation **less detectable**.
- Implements the **Guará PT pattern** for structured automation.
- Uses **randomized text selection** to enhance test variability.

