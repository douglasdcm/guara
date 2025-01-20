from logging import error
from guara import it


class Shows(it.IAssertion):
    """
    It checks if the value is shown in the calculator

    Args:
        actual (application): The calculator object
        expected (int): the value that should be present in the screen
    """

    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        try:
            assert actual.child(str(expected)).showing
        except Exception:
            error(f"Expected value '{expected}' not found in the application.")
            raise
