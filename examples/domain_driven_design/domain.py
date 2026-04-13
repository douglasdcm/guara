# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara


# =========================
# Domain Models
# =========================


class Student:
    """Represents a student."""

    def __init__(self, nui=None, name=None):
        self.nui = nui
        self.name = name
        self.course = None
        self.subjects_grade = []
        self.status = None

    def add_grade(self, grade):
        self.subjects_grade.append(float(grade))

    def gpa(self):
        if not self.subjects_grade:
            return 0
        return sum(self.subjects_grade) / len(self.subjects_grade)


class Subject:
    """Represents a subject."""

    def __init__(self, nui=None, name=None, course=None):
        self.nui = nui
        self.name = name
        self.course = course
        self.students = {}

    def add_student(self, student):
        if len(self.students) >= 30:
            return False
        self.students[student.nui] = student
        return True


class Course:
    """Represents a course."""

    def __init__(self, nui=None, name=None):
        self.nui = nui
        self.name = name
        self.subjects = {}
        self.students = {}
        self.cancelled = False

    def __str__(self):
        return f"Course {self.nui} {self.name}"

    def add_subject(self, subject):
        self.subjects[subject.nui] = subject

    def add_student(self, student):
        if self.cancelled:
            return False
        self.students[student.nui] = student
        return True
