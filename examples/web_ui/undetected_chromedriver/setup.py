# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from guara.transaction import AbstractTransaction


class OpenBrowserTransaction(AbstractTransaction):
    """Open browser using undetected-chromedriver"""

    def do(self):
        return self._driver  # Return the driver for Guará to manage


class CloseBrowserTransaction(AbstractTransaction):
    """Close the browser safely"""

    def do(self):
        self._driver.quit()
