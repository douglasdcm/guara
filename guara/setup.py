# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
[DEPRECATED] This method is not available starting from version `0.0.11`.
Copy the code from
 https://github.com/douglasdcm/guara/blob/main/examples/web_ui/selenium/simple/local_page/setup.py"
"""

from guara.transaction import AbstractTransaction


class DeprecatedError(Exception):
    pass


class OpenApp(AbstractTransaction):
    """
    [DEPRECATED] This method is not available starting from version `0.0.11`
    """

    def do(self, **kwargs) -> str:
        raise DeprecatedError(
            "This method is deprecated. Copy the code from"
            " https://github.com/douglasdcm/guara"
            "/blob/main/examples/web_ui/selenium/simple/local_page/setup.py"
        )


class CloseApp(AbstractTransaction):
    """
    [DEPRECATED] This method is not available starting from version `0.0.11`
    """

    def do(self, **kwargs) -> None:
        OpenApp().do()
