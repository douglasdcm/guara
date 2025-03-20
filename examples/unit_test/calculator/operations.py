# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction


class Add(AbstractTransaction):
    def do(self, a, b):
        return self._driver.add(a, b)


class Subtract(AbstractTransaction):
    def do(self, a, b):
        return self._driver.subtract(a, b)
