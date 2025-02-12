[WinAppDriver](https://github.com/microsoft/WinAppDriver) is a service to support Selenium-like UI Test Automation on Windows Applications. It is part of the Windows Application Driver project.

# WinAppDriver Integration Testing with Guara

This project demonstrates how to integrate **WinAppDriver** with **Guará's Page Transactions (PT) pattern** to automate interactions with the Windows Calculator application.

## Project Structure
```
project-root/ │── examples/ │ ├── windows_desktop/ │ ├── winappdriver/
├── setup.py # Contains setup transactions
├── calculator.py # Contains calculator transactions
├── test_calculator.py # The test script
```

## Code Breakdown

### **Imports**
- `pytest`: Provides test framework functionality.
- `platform`: Used to check the operating system.
- `guara.transaction.Application`: Manages transactions within the Guará framework.
- `guara.it`: Provides assertion utilities.

---

## **Test Class: `TestWindowsCalculatorWithWinAppDriver`**
This class automates interactions with the Windows Calculator application using **WinAppDriver**.

### **Class-Level Marking**
- The `@pytest.mark.skipif` decorator is used to **skip the test** if not running on Windows.

### **Setup Method `setup_method`**
1. Uses **lazy imports** to prevent unnecessary module loading.
2. Imports [`setup`] transactions from `examples.windows_desktop.winappdriver`.
3. Initializes a **Guará Application** instance using `WinAppDriver`.
4. Launches the Windows Calculator application using `setup.OpenAppTransaction`.

### **Teardown Method `teardown_method`**
- Closes the application after each test using `setup.CloseAppTransaction`.

---

## **Test Case: `test_addition`**
This test verifies that addition operations are successfully performed within the Windows Calculator application.
1. Uses a **lazy import** to retrieve the [`calculator`] transaction module.
2. Defines the test input numbers and expected result.
3. Performs the addition using `calculator.SumNumbers`.
4. **Assertions:**
   - Ensures the calculator correctly displays the result of the addition.

---

## **Summary**
- The test automates interactions with a **Windows application**.
- Uses **WinAppDriver** to control GUI elements.
- Implements the **Guará PT pattern** for structured automation.
- Uses **lazy imports** to optimize module loading and execution efficiency.