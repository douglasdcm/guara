from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction


class Navgigate(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(5) img").click()
        self._driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").click()
        return self._driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").text
