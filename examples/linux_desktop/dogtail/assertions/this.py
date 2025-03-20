# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara import it


class Shows(it.IAssertion):
    """
    It checks if the value is shown in the calculator

    Args:
        actual (application): The calculator object
        expected (int): the value that should be present in the screen
    """

    def asserts(self, actual, expected):
        assert actual.child(str(expected)).showing
