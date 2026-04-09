class Subject:
    def __init__(self, niu, name):
        if len(name) > 10:
            raise ValueError("Subject name too long")
        self.niu = niu
        self.name = name
        self.active = True


class Course:
    def __init__(self, course_id, name):
        if len(name) > 10:
            raise ValueError("Course name too long")

        self.course_id = course_id
        self.name = name
        self.subjects = []
        self.canceled = False

    def add_subject(self, subject):
        self.subjects.append(subject)


class Student:
    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf
        self.course = None
        self.grades = {}  # {niu: [grades]}
        self.locked = False

    def enroll_course(self, course):
        if course.canceled:
            raise Exception("Cannot enroll in canceled course")
        self.course = course

    def add_grade(self, niu, grade):
        if self.locked:
            raise Exception("Student is locked")

        if grade < 0 or grade > 10:
            raise ValueError("Invalid grade")

        self.grades.setdefault(niu, []).append(grade)

    def get_gpa(self):
        best_grades = []

        for niu, grades in self.grades.items():
            best_grades.append(max(grades))

        if not best_grades:
            return 0

        return sum(best_grades) / len(best_grades)

    def is_approved(self):
        if not self.course:
            return False

        subjects_niu = {s.niu for s in self.course.subjects}

        # Must have all subjects
        if not subjects_niu.issubset(set(self.grades.keys())):
            return False

        # GPA rule
        return self.get_gpa() >= 7
