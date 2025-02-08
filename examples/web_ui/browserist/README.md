# Introduction
[Browserist](https://github.com/jakob-bagterp/browserist) is a Python extension for the Selenium web driver that makes browser automation even easier 

# Browserist Integration Testing with Guara

This project demonstrates how to integrate [Browserist](https://github.com/jakob-bagterp/browserist) with Guará for web UI testing using the Page Transactions (PT) pattern. The test suite automates interactions with a local HTML page and verifies expected behaviors.

## Project Structure

```
examples/
├── web_ui/
│   ├── browserist/
│   │   ├── setup.py    # Handles browser setup and teardown
│   │   ├── home.py     # Defines interactions for the home page
tests/
│   ├── test_browserist_integration.py  # Main test suite
sample.html  # Local test page
```

## Test Details

The test suite uses Guara's `Application` and `Page Transactions` pattern to:
- Launch a local HTML file in a headless browser
- Submit random text inputs
- Validate expected outcomes

### Test Script Breakdown

- **Setup**: Opens a browser instance with `Browserist`, navigates to `sample.html`, and verifies the page title.
- **Test Execution**: Submits randomized text and checks if the response matches expectations.
- **Teardown**: Closes the browser session.



