# models/student.py

class Student:
    def __init__(self, student_id: int, name: str, email: str):
        self.id = student_id
        self.name = name
        self.email = email
        self.history = [] # История курсов и оценок (заполняется при завершении курса)