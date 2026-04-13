# Modeling a CLI Education Platform with Guará

## Introduction

This article presents a complete example of how to build a CLI-based education platform using the Guará framework. The goal is to demonstrate how business requirements can be translated directly into executable use cases, and how those same use cases drive implementation and testing.

Instead of separating requirements, application logic, and tests, Guará allows you to express everything through a unified approach based on transactions and fluent scenarios. This results in a system where behavior is explicit, traceable, and aligned with business intent.

## Problem Overview

The system models a simple academic environment with the following core concepts:

* Students
* Courses
* Subjects
* Enrollments
* Grades and GPA

The platform supports operations such as:

* Creating students, courses, and subjects
* Enrolling students in courses and subjects
* Assigning grades
* Calculating GPA

All interactions are performed via CLI, but internally represented as Guará transactions.

## Use Cases as the Source of Truth

In Guará, behavior is expressed using a fluent syntax:

```python
eduapp.when(CreateStudent, with_name="John").asserts(it.IsNotNone)

eduapp.when(CreateCourse, with_name="Math").asserts(it.IsEqualTo, "Math")

eduapp.when(CreateSubject, with_name="Algebra", in_course_with_id="C1") \
      .asserts(it.IsEqualTo, "Algebra")

eduapp.when(EnrollStudentInCourse, student_id="S1", course_id="C1") \
      .asserts(it.IsTrue)

eduapp.when(SetGrade, student_id="S1", subject_id="SUB1", with_grade=8) \
      .asserts(it.IsTrue)
```

These use cases are not just tests. They define what the system must do. The implementation follows directly from them.

## Domain Model

The domain is intentionally simple and focuses on business rules.

```python
class Student:
    """Represents a student."""

    def __init__(self, nui=None, name=None):
        self.nui = nui
        self.name = name
        self.course = None
        self.subjects_grade = []
        self.status = None

    def add_grade(self, grade):
        self.subjects_grade.append(float(grade))

    def gpa(self):
        if not self.subjects_grade:
            return 0
        return sum(self.subjects_grade) / len(self.subjects_grade)
```

## Persistence Layer

The repository persists data using SQLite. It abstracts the storage from the rest of the system.

```python
class Repository:
    def __init__(self, db_path="education.db"):
        self.conn = sqlite3.connect(db_path)

    def add_student(self, nui, name, course_id=None):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO students (nui, name, course_id) VALUES (?, ?, ?)",
            (nui, name, course_id)
        )
        self.conn.commit()

    def get_student(self, nui):
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM students WHERE nui = ?", (nui,))
        return cursor.fetchone()
```

## Transactions

Each use case is implemented as a transaction. This is where business behavior lives.

```python
from guara import AbstractTransaction

class CreateStudent(AbstractTransaction):
    def do(self, repo: Repository, with_name):
        nui = len(repo.list_students()) + 1
        repo.add_student(nui, with_name)
        return True
```

```python
class EnrollStudentInCourse(AbstractTransaction):
    def do(self, repo: Repository, student_id, course_id):
        repo.update_student_course(student_id, course_id)
        return True
```

```python
class SetGrade(AbstractTransaction):
    def do(self, repo: Repository, student_id, subject_id, with_grade):
        repo.add_grade(student_id, subject_id, with_grade)
        return True
```

## Application Layer

Guará provides an Application object that orchestrates transactions.

```python
from guara import Application

eduapp = Application()
eduapp.execute(CreateStudent, repo=repo, with_name="John")
```

The Application instance manages execution, state, and undo operations when needed.

## CLI Integration

The CLI acts as an entrypoint that maps user commands to Guará use cases.

```python
def main():
    parser = argparse.ArgumentParser()

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
        eduapp.when(CreateStudent, repo=repo, with_name=args.name).expects(it.IsTrue)

    elif args.action == "enroll_course":
        try:
            (
                eduapp
                .given(HasCourse, repo=repo, course=args.course)
                .and_(HasStudent, repo=repo, student=args.student)
                .and_(IsNotStudentEnrolledInACourse, repo=repo, student_id=args.student)
                .when(EnrollStudentInCourse, repo=repo, student_id=args.student, course_id=args.course)
                .asserts(it.IsTrue)
            )
        except Exception as e:
            print(str(e))
            eduapp.undo()
```

This design keeps the CLI thin and delegates all logic to transactions.

## Testing with the Same Use Cases

Tests reuse the same transactions and scenarios.

```python
def test_create_student():
    app = Application()
    app.when(CreateStudent, repo=repo, with_name="John").asserts(it.IsNotNone)
```

```python
def test_enroll_course():
    app = Application()
    app.when(
        EnrollStudentInCourse,
        repo=repo,
        student_id="S1",
        course_id="C1"
    ).asserts(it.IsTrue)
```

There is no need for a separate testing DSL. The same language is used everywhere.

## Benefits of This Approach

This architecture provides several advantages:

* Single source of truth for system behavior
* High readability aligned with business language
* Reduced duplication between requirements and tests
* Faster feedback loop during development
* Easier onboarding for new developers and stakeholders

## Conclusion

This project shows how Guará enables a different way of building systems. By modeling behavior as executable use cases, the gap between requirements, implementation, and testing disappears.

The result is a system where:

* Use cases define the architecture
* Transactions implement behavior
* Assertions validate outcomes

This approach is particularly effective for business-driven applications where clarity and correctness are more important than technical complexity.

For more details, refer to the example:

 - [Domain Driven Design example](https://github.com/douglasdcm/guara/blob/main/examples/domain_driven_design/)
