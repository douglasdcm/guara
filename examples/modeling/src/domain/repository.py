class Repository:
    def __init__(self):
        self.students = []
        self.courses = []

    def save_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def save_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def list_students(self):
        return self.students

    def list_courses(self):
        return self.courses
