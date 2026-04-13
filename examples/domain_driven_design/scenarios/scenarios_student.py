# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging

from scenarios.utils import run_scenario
from guara.transaction import Application
from guara import it
from repository import Repository
from transactions import (
    CreateStudent,
    HasCourse,
    EnrollStudentInCourse,
    EnrollStudentInSubject,
    HasStudent,
    HasSubject,
    HasNotStudent,
    IsGradeInValidRange,
    IsNotStudentEnrolledInSubject,
    IsNotStudentLocked,
    IsStudentEnrolledInACourse,
    IsStudentEnrolledInSubject,
    SetGrade,
    CalculateGPA,
    IsNotStudentEnrolledInACourse,
)

logging.getLogger(__name__)


@run_scenario
def create_student(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasNotStudent, repo=repo, student_name=args.name).when(
            CreateStudent, repo=repo, with_name=args.name
        )
    ).expects(it.IsTrue)


@run_scenario
def set_grade(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasStudent, repo=repo, student_id=args.student)
        .given(HasSubject, repo=repo, subject_id=args.subject)
        .and_(
            IsStudentEnrolledInSubject,
            repo=repo,
            student_id=args.student,
            subject_id=args.subject,
        )
        .and_(IsGradeInValidRange, grade=args.grade)
        .when(
            SetGrade,
            repo=repo,
            student_id=args.student,
            subject_id=args.subject,
            with_grade=args.grade,
        )
        .asserts(it.IsTrue)
    )


@run_scenario
def enroll_course(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasCourse, repo=repo, course_id=args.course)
        .and_(HasStudent, repo=repo, student_id=args.student)
        .and_(IsNotStudentEnrolledInACourse, repo=repo, student_id=args.student)
        .when(EnrollStudentInCourse, repo=repo, student_id=args.student, course_id=args.course)
        .asserts(it.IsTrue)
    )


@run_scenario
def enroll_subject(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasStudent, repo=repo, student_id=args.student)
        .and_(IsStudentEnrolledInACourse, repo=repo, student_id=args.student)
        .given(IsNotStudentLocked, repo=repo, student_id=args.student)
        .and_(HasSubject, repo=repo, subject_id=args.subject)
        .and_(
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


@run_scenario
def calculate_gpa(eduapp: Application, repo: Repository, args):
    result = eduapp.when(CalculateGPA, repo=repo, student_id=args.student).result
    logging.info(f"GPA: {result}")
