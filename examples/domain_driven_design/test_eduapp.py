"""
Tests for CLI main function using Guará framework.
"""

import sys
import pytest
from guara.transaction import Application, AbstractTransaction
from guara import it

from examples.domain_driven_design.main import main  # <-- adjust to your actual file name


@pytest.fixture
def main_fixture():
    """Provide main CLI function."""
    return main

class RunCLI(AbstractTransaction):
    """Transaction to execute CLI with arguments."""

    def do(self, with_args, main_func):
        sys.argv = ["prog"] + with_args
        try:
            main_func()
            return True
        except Exception:
            return False


# =========================
# Tests
# =========================

def test_create_student(main_fixture):
    """Test create student action."""
    app = Application()

    (
        app
        .when(RunCLI, with_args=["--action", "create_student", "--name", "John"], main_func=main_fixture)
        .asserts(it.IsTrue)
    )


def test_create_course(main_fixture):
    """Test create course action."""
    app = Application()

    (
        app
        .when(RunCLI, with_args=["--action", "create_course", "--name", "Math"], main_func=main_fixture)
        .asserts(it.IsTrue)
    )


def test_create_subject(main_fixture):
    """Test create subject action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=["--action", "create_subject", "--name", "Alg", "--course", "C1"],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )


def test_enroll_course(main_fixture):
    """Test enroll course action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=["--action", "enroll_course", "--student", "S1", "--course", "C1"],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )


def test_enroll_subject(main_fixture):
    """Test enroll subject action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=["--action", "enroll_subject", "--student", "S1", "--subject", "SUB1"],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )


def test_set_grade(main_fixture):
    """Test set grade action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=[
                "--action", "set_grade",
                "--student", "S1",
                "--subject", "SUB1",
                "--grade", "8"
            ],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )


def test_gpa(main_fixture):
    """Test GPA action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=["--action", "gpa", "--student", "S1"],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )

@pytest.mark.skip
def test_list_subjects(main_fixture):
    """Test list subjects action."""
    app = Application()

    (
        app
        .when(
            RunCLI,
            with_args=["--action", "list_subjects", "--course", "C1"],
            main_func=main_fixture
        )
        .asserts(it.IsTrue)
    )