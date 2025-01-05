from guara.asynchronous.transaction import AbstractTransaction


class OpenApp(AbstractTransaction):
    """
    Not Implemented as Selenium not is executed asynchronously.
    Use your preferable asynchronous Web Driver.
    For example: https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver):
        super().__init__(driver)

    async def do(self, **kwargs):
        raise NotImplementedError(
            "Selenium does not support asynchronous execution."
            " Use your preferable async WebDriver. "
            " For example https://github.com/douglasdcm/caqui"
        )


class CloseApp(AbstractTransaction):
    """
    Not Implemented as Selenium is not executed asynchronously.
    Use your preferable asynchronous Web Driver.
    For example: https://github.com/douglasdcm/caqui
    """

    def __init__(self, driver):
        super().__init__(driver)

    async def do(self, **kwargs):
        raise NotImplementedError(
            "Selenium does not support asynchronous execution."
            " Use your preferable async WebDriver. "
            " For example https://github.com/douglasdcm/caqui"
        )
