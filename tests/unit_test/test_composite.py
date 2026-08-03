# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara import it
from guara.abstract_transaction import AbstractTransaction
from guara.application import Application


class DoThat(AbstractTransaction):
    def do(self, **kwargs):
        return f"do that {kwargs.get('param')}"


class DoIt(AbstractTransaction):
    def do(self, **kwargs):
        return f"do it {kwargs.get('param')}"


class DoAll(AbstractTransaction):
    def do(self, **kwargs):
        results = []
        to_dos = [DoIt, DoThat]
        for to_do in to_dos:
            result = to_do().do(**kwargs)
            results.append(result)
        return results


def test_composite_class():
    Application().when(DoAll, param="foo").then(it.ContainsAll, ["do that foo", "do it foo"])
