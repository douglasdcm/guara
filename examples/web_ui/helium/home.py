# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    """
    Submits the text

    Args:
        text (str): The text to be submited

    Returns:
        str: the label 'It works! {code}!'
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        # Lazy import as Helium is not compatible with Python 3.7
        from helium import find_all, write, click, S, Text

        TEXT = '//*[@id="input"]'
        BUTTON_TEST = "button"
        text_field = find_all(S(TEXT))[0]
        write(text, text_field)
        click(find_all(S(BUTTON_TEST))[0])
        return Text("It works!").value
