# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from selenium.webdriver.common.by import By


class NavigateTo(AbstractTransaction):
    """
    Navigates to Contact page

    Returns:
        str: Paragraph informing the contacts
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        BUTTON_CONTACT = "contact"
        self._driver.find_element(By.ID, BUTTON_CONTACT).click()
        self._driver.find_element(By.CSS_SELECTOR, ".container:nth-child(3)").click()
        return self._driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").text
