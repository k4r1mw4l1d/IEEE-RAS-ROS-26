class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, stud):
        self.students.append(stud)

    def count_students(self):
        print("Number Of Students is: " + str(len(self.students)))


c = Classroom()   
c.add_student("Karim")
c.add_student("Mahmoud")
c.add_student("Khairy")
c.count_students()
