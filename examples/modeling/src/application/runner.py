from guara.transaction import Application


class EducationApplication(Application):
    def __init__(self, driver=None):
        super().__init__(driver)

    def do(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    # GIVEN
    def a_course_with_subjects(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    def a_student_registered(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    def course_has_subjects(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    # WHEN
    def student_enrolls(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self


    def student_receives_grade(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    # THEN
    def academic_record_is_updated(self, transaction=None, **kwargs):
        if transaction:
            super().then(transaction, **kwargs)
        return self

    # ASSERT
    def academic_outcome_should_be(self, assertion, expected):
        super().asserts(assertion, expected)
        return self
