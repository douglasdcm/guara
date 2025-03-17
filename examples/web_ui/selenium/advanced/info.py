# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from selenium.webdriver.common.by import By


class NavigateTo(AbstractTransaction):
    """
    Navigates to Info page

    Returns:
        str: Paragraph with information of app (About)
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        BUTTON_ABOUT = "about"
        self._driver.find_element(By.ID, BUTTON_ABOUT).click()
        self._driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").click()
        return self._driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").text
