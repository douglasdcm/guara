from guara.transaction import AbstractTransaction


class SubmitSeleniumStealth(AbstractTransaction):
    """Actions on the home page"""

    def do(self, text):
        self._driver.get("https://example.com")
        TEXT = '//*[@id="input"]'
        self._driver.find_element("tag name", "h1").click()
        text_field = self._driver.find_element_by_xpath(TEXT)
        text_field.send_keys(text)
        text_field.submit()
        return self._driver.page_source
