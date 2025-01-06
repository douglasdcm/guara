from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction


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
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text


class ChangeToEnglish(AbstractTransaction):
    """
    Changes the content of the Home page to English

    Returns:
        str: The label of the page in English
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, "button:nth-child(2) > img").click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text


class ChangeToPortuguese(AbstractTransaction):
    """
    Changes the content of the Home page to Portuguese

    Returns:
        str: The label of the page in Portuguese
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(
            By.CSS_SELECTOR, ".btn:nth-child(3) > button:nth-child(1) > img"
        ).click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text


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
        self._driver.find_element(By.ID, "send_message").click()
        WebDriverWait(self._driver, 30).until(
            expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".row:nth-child(1) > .col-md-2 > p"),
                wait_for,
            )
        )
        return self._driver.find_element(
            By.CSS_SELECTOR, ".row:nth-child(1) > .col-md-2 > p"
        ).text

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
        self._driver.find_element(By.ID, "cond_and").click()


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
        self._driver.find_element(By.ID, "cond_or").click()
