# Introduction
[PyAutoWin](https://pywinauto.readthedocs.io/en/latest/) is a set of python modules to automate the Microsoft Windows GUI. At its simplest it allows you to send mouse and keyboard actions to windows dialogs and controls.

# PyAutoWin Integration Testing with Guara

This project demonstrates how to integrate **PyAutoWin** with **Guará's Page Transactions (PT) pattern** to automate interactions with a local Windows application.

## Code Breakdown

### **Imports**
- `pytest`: Provides test framework functionality.
- `guara.transaction.Application`: Manages transactions within the Guará framework.
- `guara.it`: Provides assertion utilities.

---

## **Test Class: `TestPyAutoWinIntegration`**
This class automates interactions with a local Windows application using **PyAutoWin**.

### **Class-Level Marking**
- The `@pytest.mark.skip` decorator is used to **skip the test** due to complex CI environment setup requirements.

### **Setup Method (`setup_method`)**
1. Uses **lazy imports** to prevent unnecessary module loading.
2. Imports `pyautowin`, a library for automating Windows GUI interactions.
3. Retrieves the **setup transactions** from `examples.windows_desktop.pyautowin.setup`.
4. Initializes a **Guará Application** instance using `pyautowin`.
5. Launches the Windows application using `setup.OpenApplication`, specifying the executable path (`app_path`).

### **Teardown Method (`teardown_method`)**
- Closes the application after each test using `setup.CloseApplication`.

---

## **Test Case: `test_submit_text`**
This test verifies that text input is successfully submitted within the Windows application.
1. Uses a **lazy import** to retrieve the `home` transaction module.
2. Defines the test input text: `"Hello, PyAutoWin!"`.
3. Submits the text using `home.SubmitTextPyAutoWin`.
4. **Assertions:**
   - Ensures the application correctly processes and returns the submitted text.

---

## **Summary**
- The test automates interactions with a **Windows application**.
- Uses **PyAutoWin** to control GUI elements.
- Implements the **Guará PT pattern** for structured automation.
- Uses **lazy imports** to optimize module loading and execution efficiency.

