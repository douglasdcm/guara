from datetime import datetime
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, url, window_width=1094, window_hight=765, implicitly_wait=10):
        self._driver.set_window_size(window_width, window_hight)
        self._driver.get(url)
        self._driver.implicitly_wait(implicitly_wait)
        return self._driver.title


class CloseApp(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, screenshot_filename=f"/tmp/test{datetime.now()}.png"):
        self._driver.get_screenshot_as_file(screenshot_filename)
        self._driver.quit()
