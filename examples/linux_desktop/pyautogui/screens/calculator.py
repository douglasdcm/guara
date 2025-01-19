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

    def _get_button_path(self, button_name):
        return f"{BASE_PATH}{button_name}.png"

    def _click_buton(self, button, CONFIDENCE):
        button = pyautogui.locateOnScreen(button, confidence=CONFIDENCE)
        if not button:
            raise ValueError(f"Button image {button} not found.")
        pyautogui.click(button)

    def do(self, a, b):
        BUTTON_1 = self._get_button_path(f"button_{str(a)}")
        BUTTON_2 = self._get_button_path(f"button_{str(b)}")
        BUTTON_SUM = self._get_button_path("button_sum")
        BUTTON_EQUALS = self._get_button_path("button_equals")
        CONFIDENCE = 0.9

        self._click_buton(BUTTON_1, CONFIDENCE)
        # The tool confuses "+" and "÷", but this example does not worry about it
        self._click_buton(BUTTON_SUM, CONFIDENCE)
        self._click_buton(BUTTON_2, CONFIDENCE)
        self._click_buton(BUTTON_EQUALS, CONFIDENCE)
