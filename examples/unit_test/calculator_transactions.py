from guara.transaction import AbstractTransaction


class Add(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, a, b):
        return self._driver.add(a, b)


class Subtract(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, a, b):
        return self._driver.subtract(a, b)
