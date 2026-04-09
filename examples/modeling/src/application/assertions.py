from guara.assertion import IAssertion


class StudentGPAIs(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        return round(actual.get_gpa(), 2)


class StudentIsApproved(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        return actual.is_approved()


class StudentIsLocked(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        return actual.locked
