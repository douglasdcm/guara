import logging
from dogtail.procedural import run, focus, click
from dogtail.utils import screenshot
from guara.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Opens the App using dogtail for convenience

    Args:
        name: the name of the app, for example 'gnome-calculator'
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, name):
        try:
            run(name)
            focus.application(name)
        except Exception as e:
            logging.error(f"Failed to open {name}: {str(e)}")
            raise


class CloseApp(AbstractTransaction):
    """
    Closes the App using dogtail for convenience
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        screenshot()
        click("Close")
