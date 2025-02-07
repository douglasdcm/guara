# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class SubmitTextSplinter(AbstractTransaction):
    """
    Submits the text using Splinter

    Args:
        text (str): The text to be submitted

    Returns:
        str: the label 'It works! {code}!'
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.browser = driver

    def do(self, text):
        TEXT_FIELD_ID = "input"
        BUTTON_ID = "button"
        RESULT_ID = "result"

        text_field = self._driver.find_by_id(TEXT_FIELD_ID).first
        if not text_field:
            raise RuntimeError(f"Input field with ID '{TEXT_FIELD_ID}' not found")

        """Enter the text"""
        text_field.fill(text)

        """Locate the button by ID"""
        button = self._driver.find_by_id(BUTTON_ID).first
        if not button:
            raise RuntimeError(f"Button with ID '{BUTTON_ID}' not found")

        """Click the button"""
        button.click()

        """Locate the result field by ID"""
        result = self._driver.find_by_id(RESULT_ID).first
        if not result:
            raise RuntimeError(f"Result field with ID '{RESULT_ID}' not found")

        """Return the result text"""
        return result.text
