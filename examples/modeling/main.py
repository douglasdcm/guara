import sys

from src.domain.repository import Repository
from src.application.transactions import *
from src.application.runner import EducationApplication


def main(args):
    repo = Repository()  
    course = Course(1, "CS1")
    student = Student("Marcos", "876")

    app = EducationApplication()
    (
        app.do(EnsureCourseExists, repo=repo, course=course)
        .do(EnsureStudentExists)
        .student_enrolls(EnrollStudent, repo=repo, student=student, course=course)
    )


if __name__ == "__main__":
    main(sys.argv[1:])
