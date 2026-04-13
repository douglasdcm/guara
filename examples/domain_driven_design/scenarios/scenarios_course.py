# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import Application
from guara import it
from repository import Repository
from scenarios.utils import run_scenario
from transactions import (
    CreateCourse,
    HasNotCourse,
)


@run_scenario
def create_course(eduapp: Application, repo: Repository, args):
    (
        eduapp.given(HasNotCourse, repo=repo, course_name=args.name)
        .when(CreateCourse, repo=repo, with_name=args.name)
        .then(it.IsTrue)
    )
