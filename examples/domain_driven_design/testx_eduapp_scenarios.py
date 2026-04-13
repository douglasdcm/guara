# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import pytest
from guara.transaction import Application
from types import SimpleNamespace
from repository import Repository

from scenarios import scenarios_student, scenarios_course, scenarios_subject


@pytest.fixture
def eduapp():
    yield Application()


@pytest.fixture
def repo():
    yield Repository(":memory:")


@pytest.fixture
def args():
    yield SimpleNamespace()


def test_create_student(eduapp, repo, args):
    args.name = "John"
    assert scenarios_student.create_student(eduapp, repo, args)


def test_set_grades_and_calculte_gpa(eduapp, repo, args):
    args.student = "John"
    args.grade = 7
    args.subject = "SU1"
    args.course = "CS1"

    args.name = args.course
    scenarios_course.create_course(eduapp, repo, args)
    course_id = len(repo.list_courses())
    args.course = course_id

    args.name = args.subject
    scenarios_subject.create_subject(eduapp, repo, args)
    subject_id = len(repo.list_subjects())
    args.subject = subject_id

    args.name = args.student
    scenarios_student.create_student(eduapp, repo, args)
    student_id = len(repo.list_students())
    args.student = student_id

    scenarios_student.enroll_course(eduapp, repo, args)
    scenarios_student.enroll_subject(eduapp, repo, args)
    scenarios_student.set_grade(eduapp, repo, args)
    assert scenarios_student.calculate_gpa(eduapp, repo, args)
