# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class SubmitSeleniumStealth(AbstractTransaction):
    """Actions on the home page"""

    def do(self, text):
        self._driver.get("https://example.com")
        self._driver.find_element("tag name", "h1").click()
        return self._driver.page_source
