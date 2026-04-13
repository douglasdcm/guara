# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from scenarios.utils import run_scenario
from guara.transaction import Application
from guara import it
from repository import Repository
from transactions import (
    CreateSubject,
    HasCourse,
    HasNotSubject,
    ListSubjects,
)


@run_scenario
def list_subjects(eduapp: Application, repo: Repository, args):

    result = (
        eduapp.when(ListSubjects, repo=repo, course_id=args.course).asserts(it.IsNotEmpty).result
    )
    print(result)


@run_scenario
def create_subject(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasCourse, repo=repo, course_id=args.course)
        .given(HasNotSubject, repo=repo, subject_name=args.name)
        .when(CreateSubject, repo=repo, with_name=args.name, in_course_with_id=args.course)
        .then(it.IsEqualTo, args.name)
    )
