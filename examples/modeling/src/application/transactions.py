from guara.transaction import AbstractTransaction
from src.domain.entities import Course, Student, Subject


class CreateCourse(AbstractTransaction):
    def do(self, repo, course_id, name):
        course = Course(course_id, name)
        repo.save_course(course)
        return course


class CreateStudent(AbstractTransaction):
    def do(self, repo, name, cpf):
        student = Student(name, cpf)
        repo.save_student(student)
        return student


class EnrollStudent(AbstractTransaction):
    def do(self, repo, student, course):
        student.enroll_course(course)
        repo.save_student(student)


class AddSubjectToCourse(AbstractTransaction):
    def do(self, repo, course, niu, name):
        subject = Subject(niu, name)
        course.add_subject(subject)
        repo.save_course(course)


class AddGrade(AbstractTransaction):
    def do(self, repo, student, niu, grade):
        student.add_grade(niu, grade)
        repo.save_student(student)
        return student

class EnsureStudentExists(AbstractTransaction):
    def do(self, repo, student):
        if student not in repo.students:
            raise Exception("Student does not exist")

        return student

class EnsureCourseExists(AbstractTransaction):
    def do(self, repo, course):
        if course not in repo.courses:
            raise Exception("Course does not exist")

        return course
    
class EnsureSubjectExists(AbstractTransaction):
    def do(self, course, niu):
        subject = next((s for s in course.subjects if s.niu == niu), None)

        if not subject:
            raise Exception(f"Subject {niu} does not exist in course")

        return subject
    

class EnsureStudentEnrolledInCourse(AbstractTransaction):
    def do(self, student, course):
        if student.course != course:
            raise Exception("Student is not enrolled in this course")

        return True
    
class EnsureCourseHasSubjects(AbstractTransaction):
    def do(self, course):
        if not course.subjects:
            raise Exception("Course has no subjects")

        return course.subjects
    
class EnsureStudentSubscribedInSubject(AbstractTransaction):
    def do(self, student, course, niu):
        if student.course != course:
            raise Exception("Student not enrolled in course")

        subject = next((s for s in course.subjects if s.niu == niu), None)

        if not subject:
            raise Exception("Subject does not belong to student's course")

        return subject
    
class EnsureStudentCanReceiveGrade(AbstractTransaction):
    def do(self, repo, student, course, niu):
        if student not in repo.students:
            raise Exception("Student does not exist")

        if course not in repo.courses:
            raise Exception("Course does not exist")

        if student.course != course:
            raise Exception("Student not enrolled in course")

        subject = next((s for s in course.subjects if s.niu == niu), None)

        if not subject:
            raise Exception("Subject not found")

        if not subject.active:
            raise Exception("Subject is not active")

        if student.locked:
            raise Exception("Student is locked")

        return True