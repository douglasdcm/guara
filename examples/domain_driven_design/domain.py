# =========================
# Domain Models
# =========================


class Student:
    """Represents a student."""

    def __init__(self, nui=None, name=None):
        self.nui = nui
        self.name = name
        self.course = None
        self.subjects = []
        self.locked = False

    def enroll_course(self, course):
        if self.course:
            return False
        self.course = course
        return True

    def enroll_subject(self, subject):
        if self.locked:
            return False
        if subject.course != self.course:
            return False
        if len(self.subjects) >= 3:
            return False
        self.subjects.append(subject)
        return True

    def add_grade(self, subject_nui, grade):
        self.subjects.append(float(grade))
        return True

    def gpa(self):
        if not self.subjects:
            return 0
        return sum(self.subjects) / len(self.subjects)


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
