from guara.transaction import AbstractTransaction
from examples.domain_driven_design.repository import Repository
from examples.domain_driven_design.domain import Student, Subject, Course

# =========================
# Transactions
# =========================


class CreateStudent(AbstractTransaction):
    """Create a student."""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, repo: Repository, with_name):
        nui = len(repo.list_students()) + 1
        student = Student(nui, with_name)
        repo.add_student(nui, with_name)
        return student


class CreateCourse(AbstractTransaction):
    """Create a course."""

    def do(self, repo: Repository, with_name):
        nui = len(repo.list_courses()) + 1
        course = Course(nui, with_name)
        repo.courses = course
        return course.name


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
        raw = repo.get_student(student_id)
        student = Student(nui=raw[0], name=raw[1])
        raw = repo.get_course(course_id)
        course = Course(nui=raw[0], name=raw[1])

        if student.enroll_course(course):
            repo.update_student_course(student_id, course_id)
            return True
        return False


class IsNotStudentEnrolledInACourse(AbstractTransaction):
    def do(self, repo: Repository, student_id):
        raw = repo.get_student(student_id)
        student = Student(nui=raw[0], name=[1])
        student.course = raw[2]
        if student.course:
            raise Exception(f"Student enrolled to course {student.course}")


class IsStudentEnrolledInACourse(AbstractTransaction):
    def do(self, repo: Repository, student_id):
        raw = repo.get_student(student_id)
        student = Student(nui=raw[0], name=[1])
        student.course = raw[2]
        if not student.course:
            raise Exception("Student not enrolled to any course")


class IsStudentEnrolledInSubject(AbstractTransaction):
    def do(self, repo: Repository, student_id, subject_id):
        for raw in repo.list_enrollments_by_student(student_id):
            if raw[1] == subject_id:
                return
        raise Exception("Student not enrolled to subject")


class IsNotStudentEnrolledInSubject(AbstractTransaction):
    def do(self, repo: Repository, student_id, subject_id):
        raw = repo.get_student(student_id)
        student = Student(nui=raw[0], name=[1])
        student.subjects.append(raw[2])
        if subject_id in student.subjects:
            raise Exception("Student already enrolled to subject")


class IsGradeInValidRange(AbstractTransaction):
    def do(self, grade):
        assert 0 <= grade <= 10, "Grade must be between 0 and 10"


class EnrollStudentInSubject(AbstractTransaction):
    """Enroll student in subject."""

    def do(self, repo: Repository, student_id, subject_id):
        raw = repo.get_student(student_id)
        student = Student(raw[0], raw[1])
        raw = repo.get_subject(subject_id)
        subject = Subject(raw[0], raw[1])
        if student.enroll_subject(subject):
            subject.add_student(student)
            repo.add_enrollment(subject_id, student_id)
            return True
        return False


class SetGrade(AbstractTransaction):
    """Set grade for student."""

    def do(self, repo: Repository, student_id, subject_id, with_grade):
        repo.add_grade(student_id, subject_id, with_grade)
        return True


class CalculateGPA(AbstractTransaction):
    """Calculate GPA."""

    def do(self, repo: Repository, student_id):
        student = Student(student_id)
        for raw in repo.get_grades_by_student(student_id):
            student.add_grade(raw[0], raw[1])
        return student.gpa()


class ListSubjects(AbstractTransaction):
    """List subjects of a course."""

    def do(self, repo: Repository, course_id):
        return repo.list_subjects_by_course(course_id)


class HasCourse(AbstractTransaction):
    def do(self, repo: Repository, course: Course):
        for raw in repo.list_courses():
            cobj = Course(raw[0], raw[1])
            if cobj.nui == course.nui:
                return
            if cobj.name == course.name:
                return
        raise Exception(f"Course {course.nui} {course.name} does not exist")


class HasStudent(AbstractTransaction):
    def do(self, repo: Repository, student_id=None, student_name=None):
        for raw in repo.list_students():
            sobj = Student(raw[0], raw[1])
            if sobj.nui == student_id:
                return
            if sobj.name == student_name:
                return
        raise Exception(f"Student {student_id} {student_name} does not exist")


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

    def do(self, repo: Repository, course: Course):
        self._repo = repo
        for raw in repo.list_courses():
            cobj = Course(raw[0], raw[1])
            if course.name == cobj.name:
                raise Exception("Course exists")


class HasNotSubject(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._repo = None

    def do(self, repo: Repository, subject: Subject):
        self._repo = repo
        for raw in repo.list_subjects():
            sobj = Subject(raw[0], raw[1])
            if subject.name == sobj.name:
                raise Exception("Subject exists")


class HosNotStudent(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._repo = None

    def do(self, repo: Repository, student: Student):
        self._repo = repo
        for s in repo.list_students():
            s_obj = Student(s[0], s[1])
            if student.name == s_obj.name:
                raise Exception("Student exists")
