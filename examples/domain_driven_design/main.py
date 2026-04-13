# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
Education Platform CLI using Guará

Single-file implementation modeling use cases as transactions,
domain, and CLI interface.
"""

import argparse
from guara.transaction import Application
from scenarios import scenarios_student, scenarios_subject, scenarios_course
from repository import Repository

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
            scenarios_student.create_student(eduapp, repo, args)
        except Exception:
            pass

    elif args.action == "create_course":
        try:
            scenarios_course.create_course(eduapp, repo, args)
        except Exception:
            pass
    elif args.action == "create_subject":
        try:
            scenarios_subject.create_subject(eduapp, repo, args)
        except Exception:
            pass
    elif args.action == "enroll_course":
        try:
            scenarios_student.enroll_course(eduapp, repo, args)
        except Exception:
            pass

    elif args.action == "enroll_subject":
        try:
            scenarios_student.enroll_subject(eduapp, repo, args)
        except Exception:
            pass
    elif args.action == "set_grade":
        try:
            scenarios_student.set_grade(eduapp, repo, args)
        except Exception:
            pass
    elif args.action == "gpa":
        try:
            scenarios_student.calculate_gpa(eduapp, repo, args)
        except Exception:
            pass
    elif args.action == "list_subjects":
        try:
            scenarios_subject.list_subjects(eduapp, repo, args)
        except Exception:
            pass


if __name__ == "__main__":
    main()
