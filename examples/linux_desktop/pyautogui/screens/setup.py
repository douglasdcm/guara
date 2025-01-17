from dogtail.procedural import run, focus, click
from dogtail.utils import screenshot
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App using dogtail for convenience
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        app_name = "gnome-calculator"
        run(app_name)
        focus.application(app_name)


class CloseApp(AbstractTransaction):
    """
    Closes the App using dogtail for convenience
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        screenshot()
        click("Close")
