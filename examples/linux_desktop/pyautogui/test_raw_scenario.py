import pytest


@pytest.mark.skip("Skipped due to the complexity to integrate it in pipeline")
def test_pyauto_gui():
    # I opted for lazy imports just to not break the pipeline.
    # Do not do it.
    import pyautogui

    """This is the same scenario of the test organized with Guara, but disorganized"""
    BASE_PATH = "./examples/linux_desktop/pyautogui/images/"
    BUTTON_1 = f"{BASE_PATH}button_1.png"
    BUTTON_2 = f"{BASE_PATH}button_2.png"
    BUTTON_SUM = f"{BASE_PATH}button_sum.png"
    BUTTON_EQUALS = f"{BASE_PATH}button_equals.png"
    DISPLAYS_3 = f"{BASE_PATH}displays_3.png"

    button_1 = pyautogui.locateOnScreen(BUTTON_1, confidence=0.9)
    pyautogui.click(button_1)

    # The tool confuses "+" and "÷", but this example does not worry about it
    button_sum = pyautogui.locateOnScreen(BUTTON_SUM, confidence=0.8)
    pyautogui.click(button_sum)

    button_2 = pyautogui.locateOnScreen(BUTTON_2, confidence=0.9)
    pyautogui.click(button_2)

    button_equals = pyautogui.locateOnScreen(BUTTON_EQUALS, confidence=0.9)
    pyautogui.click(button_equals)

    button_display = pyautogui.locateOnScreen(DISPLAYS_3, confidence=0.99)
    assert button_display is not None
