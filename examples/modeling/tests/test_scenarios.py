from src.application.runner import EducationApplication
from src.application.transactions import (
    CreateCourse,
    CreateStudent,
    EnrollStudent,
    AddGrade,
)
from src.application.assertions import StudentGPAIs, StudentIsApproved, StudentIsLocked
from src.domain.repository import Repository
from src.domain.entities import Student, Course

repo = Repository()


def test_student_gpa_calculation():
    student = Student("Douglas", "4321")
    course = Course(1, "CS1")
    app = EducationApplication()
    (
        app.a_course_with_subjects(CreateCourse, repo=repo, course_id=1, name="CS")
        .a_student_registered(CreateStudent, repo=repo, name="John", cpf="123")
        .student_enrolls(EnrollStudent, repo=repo, student=student, course=course)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S1", grade=8)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S1", grade=9)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S2", grade=7)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S3", grade=6)
        .academic_outcome_should_be(StudentGPAIs, round((9 + 7 + 6) / 3, 2))
    )


def test_student_is_approved():
    student = Student("Douglas", "4321")
    course = Course(1, "CS1")
    app = EducationApplication()
    (
        app.a_course_with_subjects(CreateCourse, repo=repo, course_id=1, name="ENG")
        .a_student_registered(CreateStudent, repo=repo, name="Ana", cpf="456")
        .student_enrolls(EnrollStudent, repo=repo, student=student, course=course)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S1", grade=8)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S2", grade=7)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S3", grade=9)
        .academic_record_is_updated()
        .academic_outcome_should_be(StudentIsApproved, True)
    )


def test_student_not_approved_missing_subject():
    student = Student("Douglas", "4321")
    course = Course(1, "CS1")
    app = EducationApplication()

    (
        app.a_course_with_subjects(CreateCourse, repo=repo, course_id=1, name="MED")
        .a_student_registered(CreateStudent, repo=repo, name="Bob", cpf="789")
        .student_enrolls(EnrollStudent, repo=repo, student=student, course=course)
        .student_receives_grade(AddGrade, repo=repo, student=student, niu="S1", grade=8)
        .academic_record_is_updated()
        .academic_outcome_should_be(StudentIsApproved, False)
    )


def test_locked_student():
    app = EducationApplication()

    (
        app.a_student_registered(CreateStudent, repo=repo, name="Mike", cpf="000")
        .academic_record_is_updated()
        .academic_outcome_should_be(StudentIsLocked, False)
    )
