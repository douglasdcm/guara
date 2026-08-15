# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from constants import BASE_PATH

from guara.transaction import AbstractTransaction


class Divide(AbstractTransaction):
    """
    Divide two numbers

    Args:
        Just the numbers 1 and 2 are allowed for now.
        It is necessary to add more images in `images` folder if you want to
        divide other numbers

        a (int): The number to be divided
        b (int): The number that divides
    Returns:
        (Application) The application (self._driver)
    """

    def _get_button_path(self, button_name):
        return f"{BASE_PATH}{button_name}.png"

    def _click_buton(self, button, CONFIDENCE):
        from pyautogui import click, locateOnScreen

        button = locateOnScreen(button, confidence=CONFIDENCE)
        click(button)

    def do(self, a, b):
        BUTTON_1 = self._get_button_path(f"button_{a!s}")
        BUTTON_2 = self._get_button_path(f"button_{b!s}")
        # The tool confuses "+" and "÷", but this example does not worry about it
        BUTTON_DIVIDE = self._get_button_path("button_sum")
        BUTTON_EQUALS = self._get_button_path("button_equals")
        CONFIDENCE = 0.9

        self._click_buton(BUTTON_1, CONFIDENCE)
        self._click_buton(BUTTON_DIVIDE, CONFIDENCE)
        self._click_buton(BUTTON_2, CONFIDENCE)
        self._click_buton(BUTTON_EQUALS, CONFIDENCE)
        return self._driver
