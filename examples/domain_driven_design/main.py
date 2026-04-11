"""
Education Platform CLI using Guará

Single-file implementation modeling use cases as transactions,
domain, and CLI interface.
"""

import argparse
from guara.transaction import Application
from guara import it
from examples.domain_driven_design.repository import Repository
from examples.domain_driven_design.transactions import (
    CreateCourse,
    CreateStudent,
    CreateSubject,
    HasCourse,
    HasNotCourse,
    EnrollStudentInCourse,
    EnrollStudentInSubject,
    HasNotSubject,
    HasStudent,
    HasSubject,
    HosNotStudent,
    IsGradeInValidRange,
    IsNotStudentEnrolledInSubject,
    IsStudentEnrolledInACourse,
    IsStudentEnrolledInSubject,
    SetGrade,
    ListSubjects,
    CalculateGPA,
    IsNotStudentEnrolledInACourse,
)
from examples.domain_driven_design.domain import Course, Subject, Student

# =========================
# CLI Use Cases
# =========================


class EducationApp:
    """Application state."""

    def __init__(self):
        self.students = {}
        self.courses = {}
        self.subjects = {}


def main():
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Education CLI")

    parser.add_argument("--action", required=True)
    parser.add_argument("--name")
    parser.add_argument("--student")
    parser.add_argument("--course")
    parser.add_argument("--subject")
    parser.add_argument("--grade", type=float)

    args = parser.parse_args()

    repo = Repository()
    eduapp = Application()

    if args.action == "create_student":
        try:
            (
                eduapp.given(HosNotStudent, repo=repo, student=Student(None, args.name)).when(
                    CreateStudent, repo=repo, with_name=args.name
                )
            )
        except Exception as e:
            print(str(e))
            eduapp.undo()

    elif args.action == "create_course":
        try:
            (
                eduapp.given(HasNotCourse, repo=repo, course=Course(name=args.name))
                .when(CreateCourse, repo=repo, with_name=args.name)
                .then(it.IsEqualTo, args.name)
            )
        except Exception as e:
            print(str(e))
            eduapp.undo()

    elif args.action == "create_subject":
        try:
            (
                eduapp.given(HasCourse, repo=repo, course=Course(nui=args.course))
                .given(HasNotSubject, repo=repo, subject=Subject(name=args.name))
                .when(CreateSubject, repo=repo, with_name=args.name, in_course_with_id=args.course)
                .then(it.IsEqualTo, args.name)
            )
        except Exception as e:
            print(e)
            eduapp.undo()

    elif args.action == "enroll_course":
        try:
            (
                eduapp.given(HasCourse, repo=repo, course=Course(nui=args.course))
                .given(HasStudent, repo=repo, student=Student(nui=args.student))
                .given(IsNotStudentEnrolledInACourse, repo=repo, student_id=args.student)
                .when(
                    EnrollStudentInCourse, repo=repo, student_id=args.student, course_id=args.course
                )
                .asserts(it.IsTrue)
            )
        except Exception as e:
            print(str(e))
            eduapp.undo()

    elif args.action == "enroll_subject":
        try:
            (
                eduapp.given(HasStudent, repo=repo, student_id=args.student)
                .given(IsStudentEnrolledInACourse, repo=repo, student_id=args.student)
                .given(HasSubject, repo=repo, subject_id=args.subject)
                .given(
                    IsNotStudentEnrolledInSubject,
                    repo=repo,
                    student_id=args.student,
                    subject_id=args.subject,
                )
                .when(
                    EnrollStudentInSubject,
                    repo=repo,
                    student_id=args.student,
                    subject_id=args.subject,
                )
                .asserts(it.IsTrue)
            )
        except Exception as e:
            print(e)
            eduapp.undo()

    elif args.action == "set_grade":
        try:
            (
                eduapp.given(HasStudent, repo=repo, student_id=args.student)
                .given(HasSubject, repo=repo, subject_id=args.subject)
                .given(
                    IsStudentEnrolledInSubject,
                    repo=repo,
                    student_id=args.student,
                    subject_id=args.subject,
                )
                .given(IsGradeInValidRange, grade=args.grade)
                .when(
                    SetGrade,
                    repo=repo,
                    student_id=args.student,
                    subject_id=args.subject,
                    with_grade=args.grade,
                )
                .asserts(it.IsTrue)
            )
        except Exception as e:
            print(e)
            eduapp.undo()

    elif args.action == "gpa":
        try:
            result = eduapp.when(CalculateGPA, repo=repo, student_id=args.student).result
            print(result)
        except Exception as e:
            print(e)
            eduapp.undo()

    elif args.action == "list_subjects":
        result = (
            eduapp.when(ListSubjects, repo=repo, course_id=args.course)
            .asserts(it.IsNotEmpty)
            .result
        )
        print(result)


if __name__ == "__main__":
    main()
