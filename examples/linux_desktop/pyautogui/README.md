# Introduction
[Pyautogui](https://pyautogui.readthedocs.io/en/latest/) lets your Python scripts control the mouse and keyboard to automate interactions with other applications. The API is designed to be simple. PyAutoGUI works on Windows, macOS, and Linux, and runs on Python 2 and 3.

## Test explanation
Before executing this example make sure your host matches the [requirements](https://pyautogui.readthedocs.io/en/latest/install.html) to install Pyautogui.

This example opens the Linux `GNOME Calculator`, sums 1 and 2. You will find the transactions to `Open` and `Close` the `GNOME Calculator` and the ones to click the buttons to `Sum` the numbers.
The outpout is:
```
test_integration_with_pyautogui.py::TestLinuxCalculatorWithPyautogui::test_calculator 
--------------------------------------------------------------- live log setup ---------------------------------------------------------------
2025-01-17 18:50:38.453 INFO Transaction 'setup.OpenApp'
--------------------------------------------------------------- live log call ----------------------------------------------------------------
2025-01-17 18:50:39.749 INFO Transaction 'calculator.Add'
2025-01-17 18:50:39.750 INFO  a: 1
2025-01-17 18:50:39.750 INFO  b: 2
PASSED                                                                                                                                 [100%]
------------------------------------------------------------- live log teardown --------------------------------------------------------------
2025-01-17 18:50:40.501 INFO Transaction 'setup.CloseApp'
```