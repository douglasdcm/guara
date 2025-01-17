import pyautogui
from constants import BASE_PATH
from guara.transaction import AbstractTransaction


class Add(AbstractTransaction):
    """
    Sums two numbers

    Args:
        Just the numbers 1 and 2 are allowed for now.
        It is necessary to add more images in `images` folder if you want to
        sum other numbers

        a (int): The 1st number to be added
        b (int): The second number to be added
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, a, b):
        BUTTON_1 = f"{BASE_PATH}button_{str(a)}.png"
        BUTTON_2 = f"{BASE_PATH}button_{str(b)}.png"
        BUTTON_SUM = f"{BASE_PATH}button_sum.png"
        BUTTON_EQUALS = f"{BASE_PATH}button_equals.png"
        CONFIDENCE = 0.9

        button_1 = pyautogui.locateOnScreen(BUTTON_1, confidence=CONFIDENCE)
        pyautogui.click(button_1)

        # The tool confuses "+" and "÷", but this example does not worry about it
        button_sum = pyautogui.locateOnScreen(BUTTON_SUM, confidence=CONFIDENCE)
        pyautogui.click(button_sum)

        button_2 = pyautogui.locateOnScreen(BUTTON_2, confidence=CONFIDENCE)
        pyautogui.click(button_2)

        button_equals = pyautogui.locateOnScreen(BUTTON_EQUALS, confidence=CONFIDENCE)
        pyautogui.click(button_equals)
