# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class NavigateToGettingStarted(AbstractTransaction):
    """
    Navigates to Getting Started page

    Returns:
        str: the heading 'Installation'
    """

    def do(self, **kwargs):
        self._driver.get_by_role("link", name="Get started").click()
        return self._driver.get_by_role("heading", name="Installation").text_content()
