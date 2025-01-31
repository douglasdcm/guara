from guara.transaction import AbstractTransaction


class SubmitSeleniumStealth(AbstractTransaction):
    """Actions on the home page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.browser = driver

    def do(self, text):
        self._driver.get("https://example.com")
        TEXT_FIELD_ID = "input"
        self._driver.find_element("tag name", "h1").click()
        text_field = self._driver.find_by_id(TEXT_FIELD_ID).first
        if not text_field:
            raise RuntimeError(f"Input field with ID '{TEXT_FIELD_ID}' not found")
        """Enter the text"""
        text_field.fill(text)
        text_field.send_keys(text)
        text_field.submit()
        return self._driver.page_source
