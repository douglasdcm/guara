# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from repository import Repository
from domain import Student, Subject

# =========================
# Transactions
# =========================


class CreateStudent(AbstractTransaction):
    """Create a student."""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, repo: Repository, with_name):
        nui = len(repo.list_students()) + 1
        repo.add_student(nui, with_name)
        return True


class CreateCourse(AbstractTransaction):
    """Create a course."""

    def do(self, repo: Repository, with_name):
        nui = len(repo.list_courses()) + 1
        repo.add_course(nui, with_name)
        return True


class CreateSubject(AbstractTransaction):
    """Create a subject."""

    def do(self, repo: Repository, with_name, in_course_with_id):
        course = repo.get_course(in_course_with_id)
        nui = len(repo.list_subjects()) + 1
        subject = Subject(nui, with_name, course)
        repo.add_subject(nui, with_name, in_course_with_id)
        return subject.name


class EnrollStudentInCourse(AbstractTransaction):
    """Enroll student in course."""

    def do(self, repo: Repository, student_id, course_id):
        repo.update_student_course(student_id, course_id)
        return True


class IsNotStudentEnrolledInACourse(AbstractTransaction):
    def do(self, repo: Repository, student_id):
        try:
            IsStudentEnrolledInACourse().do(repo, student_id)
        except Exception:
            return
        raise Exception("Student enrolled to other course")


class IsStudentEnrolledInACourse(AbstractTransaction):
    def do(self, repo: Repository, student_id):
        student = repo.get_student(student_id)
        if not student.course:
            raise Exception("Student not enrolled to any course")


class IsStudentEnrolledInSubject(AbstractTransaction):
    def do(self, repo: Repository, student_id, subject_id):
        for raw in repo.list_enrollments_by_student(student_id, subject_id):
            if raw[1] == subject_id:
                return
        raise Exception("Student not enrolled to subject")


class IsNotStudentEnrolledInSubject(AbstractTransaction):
    def do(self, repo: Repository, student_id, subject_id):
        try:
            IsStudentEnrolledInSubject().do(repo, student_id, subject_id)
        except Exception:
            return
        raise Exception("Student already enrolled to subject")


class IsGradeInValidRange(AbstractTransaction):
    def do(self, grade):
        assert 0 <= grade <= 10, "Grade must be between 0 and 10"


class EnrollStudentInSubject(AbstractTransaction):
    """Enroll student in subject."""

    def do(self, repo: Repository, student_id, subject_id):
        repo.add_enrollment(subject_id, student_id)
        return True


class SetGrade(AbstractTransaction):
    """Set grade for student."""

    def do(self, repo: Repository, student_id, subject_id, with_grade):
        repo.add_grade(student_id, subject_id, with_grade)
        return True


class CalculateGPA(AbstractTransaction):
    """Calculate GPA."""

    def do(self, repo: Repository, student_id):
        student = Student(student_id)
        student = repo.get_student_grades(student_id)
        return student.gpa()


class ListSubjects(AbstractTransaction):
    """List subjects of a course."""

    def do(self, repo: Repository, course_id):
        return repo.list_subjects_by_course(course_id)


class HasCourse(AbstractTransaction):
    def do(self, repo: Repository, course_name: str = None, course_id=None):
        for cobj in repo.list_courses():
            if cobj.name == course_name:
                return
            if cobj.nui == course_id:
                return
        raise Exception(f"Course {course_name} does not exist")


class HasStudent(AbstractTransaction):
    def do(self, repo: Repository, student_id=None, student_name=None):
        for raw in repo.list_students():
            sobj = Student(raw[0], raw[1])
            if sobj.nui == student_id:
                return
            if sobj.name == student_name:
                return
        raise Exception(f"Student {student_id} {student_name} does not exist")


class IsNotStudentLocked(AbstractTransaction):
    def do(self, repo: Repository, student_id):
        student = repo.get_student(student_id)
        if student.status == "locked":
            raise Exception("Student locked")


class HasSubject(AbstractTransaction):
    def do(self, repo: Repository, subject_id=None, subject_name=None):
        for raw in repo.list_subjects():
            sobj = Subject(raw[0], raw[1])
            if sobj.nui == subject_id:
                return
            if sobj.name == subject_name:
                return
        raise Exception(f"Subject {subject_id} {subject_name} does not exist")


class HasNotCourse(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._repo = None

    def do(self, repo: Repository, course_name: str):
        try:
            HasCourse().do(repo, course_name=course_name)
        except Exception:
            return
        raise Exception("Course exists")


class HasNotSubject(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._repo = None

    def do(self, repo: Repository, subject_name: Subject):
        self._repo = repo
        for raw in repo.list_subjects():
            sobj = Subject(raw[0], raw[1])
            if subject_name == sobj.name:
                raise Exception(f"Subject {subject_name} exists")


class HasNotStudent(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._repo = None

    def do(self, repo: Repository, student_name: str):
        self._repo = repo
        for s in repo.list_students():
            s_obj = Student(s[0], s[1])
            if student_name == s_obj.name:
                raise Exception("Student exists")
