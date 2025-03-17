# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class NavigateToWritingTests(AbstractTransaction):
    """
    Navigates to Writing Tests page

    Returns:
        str: the heading 'Writing Tests'
    """

    def do(self, **kwargs):
        self._driver.get_by_role("link", name="Writing tests", exact=True).click()
        return self._driver.get_by_role(
            "heading",
            name="Writing",
        ).text_content()
