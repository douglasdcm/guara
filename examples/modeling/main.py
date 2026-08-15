import sys

from src.application.runner import EducationApplication
from src.application.transactions import (
    EnrollStudent,
    EnsureCourseExists,
    EnsureStudentExists,
)
from src.domain.entities import Course, Student
from src.domain.repository import Repository


def main(args):
    repo = Repository()
    course = Course(1, "CS1")
    student = Student("Marcos", "876")
    repo.save_course(course)
    repo.save_student(student)

    app = EducationApplication()
    (
        app.do(EnsureCourseExists, repo=repo, course=course)
        .do(EnsureStudentExists, repo=repo, student=student)
        .student_enrolls(EnrollStudent, repo=repo, student=student, course=course)
    )


if __name__ == "__main__":
    main(sys.argv[1:])
