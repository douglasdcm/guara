# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

TEXT_AREA = ".col-md-10"
TEXT_AREA_LABEL = "label:nth-child(1)"


class NavigateTo(AbstractTransaction):
    """
    Navigates to Home page

    Returns:
        str: The label of the page
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, ".navbar-brand > img").click()
        self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA).click()
        return self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA_LABEL).text


class ChangeToEnglish(AbstractTransaction):
    """
    Changes the content of the Home page to English

    Returns:
        str: The label of the page in English
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        EN_BUTTON = "en-usa"
        self._driver.find_element(By.ID, EN_BUTTON).click()
        self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA).click()
        return self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA_LABEL).text


class ChangeToPortuguese(AbstractTransaction):
    """
    Changes the content of the Home page to Portuguese

    Returns:
        str: The label of the page in Portuguese
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(By.ID, "pt-br").click()
        self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA).click()
        return self._driver.find_element(By.CSS_SELECTOR, TEXT_AREA_LABEL).text


class Search(AbstractTransaction):
    """
    Searches for a given text

    Args:
        text (str): the text to be searched for
        wait_for (str): the text to present after the search
    Returns:
        str: The result with the first similarity of the search
    """

    def __init__(self, driver):
        super().__init__(driver)

    def fill_text(self, text):
        self._driver.find_element(By.ID, "message_field").click()
        self._driver.find_element(By.ID, "message_field").send_keys(text)

    def select_search(self):
        raise NotImplementedError

    def wait_search(self, wait_for):
        ROW_1 = "row-1"
        self._driver.find_element(By.ID, "send_message").click()
        WebDriverWait(self._driver, 30).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, ROW_1),
                wait_for,
            )
        )
        return self._driver.find_element(By.ID, ROW_1).text

    def do(self, text, wait_for):
        self.fill_text(text)
        self.select_search()
        return self.wait_search(wait_for)


class DoRestrictedSearch(Search):
    """
    Searches for a given text in restricted mode

    Args:
        text (str): the text to be searched for
        wait_for (str): the text to present after the search
    Returns:
        str: The result with the first similarity of the search
    """

    def __init__(self, driver):
        super().__init__(driver)

    def select_search(self):
        BUTTON_NARROW_SEARCH = "narrow-search"
        self._driver.find_element(By.ID, "cond_and").click()
        self._driver.find_element(By.ID, BUTTON_NARROW_SEARCH).click()


class DoExpandedSearch(Search):
    """
    Searches for a given text in expanded mode

    Args:
        text (str): the text to be searched for
        wait_for (str): the text to present after the search
    Returns:
        str: The result with the first similarity of the search
    """

    def __init__(self, driver):
        super().__init__(driver)

    def select_search(self):
        BUTTON_WIDE_SEARCH = "wide-search"
        self._driver.find_element(By.ID, "cond_or").click()
        self._driver.find_element(By.ID, BUTTON_WIDE_SEARCH).click()
