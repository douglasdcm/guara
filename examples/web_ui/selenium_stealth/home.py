from guara.transaction import AbstractTransaction


class SubmitSeleniumStealth(AbstractTransaction):
    """Actions on the home page"""

    def do(self, text):
        self._driver.get("https://example.com")
        self._driver.find_element("tag name", "h1").click()
        return self._driver.page_source
