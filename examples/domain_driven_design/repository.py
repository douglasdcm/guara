"""
SQLite-backed Repository implementation.
"""

import sqlite3
from typing import List
from examples.domain_driven_design.domain import Course


class Repository:
    """Repository using SQLite for persistence."""

    def __init__(self, db_path="education.db"):
        """Initialize repository and create tables."""
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def __str__(self):
        """Return repository type."""
        return "sqlite"

    def _create_tables(self):
        """Create tables if they do not exist."""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                nui TEXT PRIMARY KEY,
                name TEXT,
                course_id TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                nui TEXT PRIMARY KEY,
                name TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                nui TEXT PRIMARY KEY,
                name TEXT,
                course_id TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                nui TEXT PRIMARY KEY,
                student_id TEXT,
                subject_id TEXT,
                grade TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                nui TEXT PRIMARY KEY,
                subject_id TEXT,
                student_id TEXT
            )
        """)

        self.conn.commit()

    # =========================
    # Students
    # =========================

    def add_student(self, nui, name, course_id=None):
        """Insert a student."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO students (nui, name, course_id) VALUES (?, ?, ?)", (nui, name, course_id)
        )
        self.conn.commit()

    def get_student(self, nui):
        """Get student by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM students WHERE nui = ?", (nui,))
        return cursor.fetchone()

    def list_students(self):
        """List all students."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM students")
        return cursor.fetchall()

    def update_student_name(self, nui, name):
        """Update student name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE students SET name = ? WHERE nui = ?",
            (name, nui)
        )
        self.conn.commit()

    def update_student_course(self, nui, course_id):
        """Update student course."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE students SET course_id = ? WHERE nui = ?",
            (course_id, nui)
        )
        self.conn.commit()

    # =========================
    # Courses
    # =========================

    def add_course(self, nui, name):
        """Insert a course."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO courses (nui, name) VALUES (?, ?)", (nui, name))
        self.conn.commit()

    def get_course(self, nui):
        """Get course by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name FROM courses WHERE nui = ?", (nui,))
        return cursor.fetchone()

    def list_courses(self) -> List[Course]:
        """List all courses."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name FROM courses")
        return cursor.fetchall()

    def update_course_name(self, nui, name):
        """Update course name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE courses SET name = ? WHERE nui = ?",
            (name, nui)
        )
        self.conn.commit()

    # =========================
    # Subjects
    # =========================

    def add_subject(self, nui, name, course_id):
        """Insert a subject."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO subjects (nui, name, course_id) VALUES (?, ?, ?)", (nui, name, course_id)
        )
        self.conn.commit()

    def get_subject(self, nui):
        """Get subject by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM subjects WHERE nui = ?", (nui,))
        return cursor.fetchone()

    def list_subjects(self):
        """List all subjects."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM subjects")
        return cursor.fetchall()

    def list_subjects_by_course(self, course_id):
        """List all subjects."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nui, name, course_id FROM subjects WHERE course_id = ?", (course_id,))
        return cursor.fetchall()

    def update_subject_name(self, nui, name):
        """Update subject name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE subjects SET name = ? WHERE nui = ?",
            (name, nui)
        )
        self.conn.commit()


    def update_subject_course(self, nui, course_id):
        """Update subject course."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE subjects SET course_id = ? WHERE nui = ?",
            (course_id, nui)
        )
        self.conn.commit()

    # =========================
    # Grades
    # =========================

    def add_grade(self, student_id, subject_id, grade):
        """Insert a new grade."""
        nui = f"{subject_id}-{student_id}-{grade}"
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO grades (nui, subject_id, student_id, grade) VALUES (?, ?, ?, ?)",
            (nui, subject_id, student_id, grade)
        )
        self.conn.commit()

    def get_grades_by_student(self, student_id):
        """Get course by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT student_id, grade FROM grades WHERE student_id = ?", (student_id,))
        return cursor.fetchall()


    def update_grade_value(self, nui, grade):
        """Update grade value."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE grades SET grade = ? WHERE nui = ?",
            (grade, nui)
        )
        self.conn.commit()

    def update_grade_student(self, nui, student_id):
        """Update student reference of a grade."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE grades SET student_id = ? WHERE nui = ?",
            (student_id, nui)
        )
        self.conn.commit()

    def update_grade_subject(self, nui, subject_id):
        """Update subject reference of a grade."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE grades SET subject_id = ? WHERE nui = ?",
            (subject_id, nui)
        )
        self.conn.commit()

    def update_grade(self, student_id=None, subject_id=None, grade=None):
        """Update multiple fields of a grade."""
        cursor = self.conn.cursor()

        fields = []
        values = []

        if student_id is not None:
            fields.append("student_id = ?")
            values.append(student_id)

        if subject_id is not None:
            fields.append("subject_id = ?")
            values.append(subject_id)

        if grade is not None:
            fields.append("grade = ?")
            values.append(grade)

        if not fields:
            return
        
        nui = 0
        values.append(nui)

        query = f"UPDATE grades SET {', '.join(fields)} WHERE nui = ?"
        cursor.execute(query, values)
        self.conn.commit()

    # =========================
    # Enrollments
    # =========================

    def add_enrollment(self, subject_id, student_id):
        """Insert a new enrollment."""
        nui = f"{subject_id}-{student_id}"
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO enrollments (nui, subject_id, student_id) VALUES (?, ?, ?)",
            (nui, subject_id, student_id)
        )
        self.conn.commit()

    def add_enrollments_bulk(self, enrollments):
        """Insert multiple enrollments."""
        cursor = self.conn.cursor()
        cursor.executemany(
            "INSERT INTO enrollments (nui, subject_id, student_id) VALUES (?, ?, ?)",
            enrollments
        )
        self.conn.commit()

    def get_enrollment(self, nui):
        """Get enrollment by NUI."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT nui, subject_id, student_id FROM enrollments WHERE nui = ?",
            (nui,)
        )
        return cursor.fetchone()

    def list_enrollments(self):
        """List all enrollments."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT nui, subject_id, student_id FROM enrollments"
        )
        return cursor.fetchall()

    def list_enrollments_by_student(self, student_id):
        """List enrollments by student."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT nui, subject_id, student_id FROM enrollments WHERE student_id = ?",
            (student_id,)
        )
        return cursor.fetchall()

    def list_enrollments_by_subject(self, subject_id):
        """List enrollments by subject."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT nui, subject_id, student_id FROM enrollments WHERE subject_id = ?",
            (subject_id,)
        )
        return cursor.fetchall()