from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction


class Navigate(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, ".navbar-brand > img").click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text


class SubmitText(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        text_box = self._driver.find_element(by=By.ID, value="input")
        submit_button = self._driver.find_element(by=By.CSS_SELECTOR, value="button")
        text_box.send_keys(text)
        submit_button.click()
        message = self._driver.find_element(by=By.ID, value="result")
        return message.text
