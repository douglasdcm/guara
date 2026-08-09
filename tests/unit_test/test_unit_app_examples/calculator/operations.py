# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from guara.transaction import AbstractTransaction


class Add(AbstractTransaction):
    def do(self, a, b):
        return self._driver.add(a, b)


class Subtract(AbstractTransaction):
    def do(self, a, b):
        return self._driver.subtract(a, b)
