# models/course.py

class Course:
    def __init__(self, course_id: int, title: str, topic: str):
        self.id = course_id
        self.title = title
        self.topic = topic
        self.status = "активен" # или "завершён"
        self.students = [] # Список ID студентов (для связей)
        self.teacher_id = None # ID преподавателя (для связей)