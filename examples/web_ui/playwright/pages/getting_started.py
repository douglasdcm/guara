from playwright.sync_api import Page
from guara.transaction import AbstractTransaction


class NavigateToWritingTests(AbstractTransaction):
    """
    Navigates to Writing Tests page

    Returns:
        str: the heading 'Writing Tests'
    """

    def __init__(self, driver):
        super().__init__(driver)
        self._driver: Page

    def do(self, **kwargs):
        self._driver.get_by_role("link", name="Writing tests", exact=True).click()
        return self._driver.get_by_role(
            "heading",
            name="Writing",
        ).text_content()
