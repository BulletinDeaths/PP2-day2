import json, os

from .student import Student
from .teacher import Teacher
from .course import Course


class Repository:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.courses = []

        self._next_student_id = 1
        self._next_teacher_id = 1
        self._next_course_id = 1

        self.load_from_json()

    # --- Методы ДОБАВЛЕНИЯ ---
    def add_student(self, name, email):
        new_student = Student(self._next_student_id, name, email)
        self.students.append(new_student)
        self._next_student_id += 1

    def add_teacher(self, name, specialization):
        new_teacher = Teacher(self._next_teacher_id, name, specialization)
        self.teachers.append(new_teacher)
        self._next_teacher_id += 1

    def add_course(self, title, topic):
        new_course = Course(self._next_course_id, title, topic)
        self.courses.append(new_course)
        self._next_course_id += 1
        return new_course

    # --- Вспомогательные методы поиска ---
    def find_student_by_id(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def find_teacher_by_id(self, teacher_id):
        return next((t for t in self.teachers if t.id == teacher_id), None)

    def find_course_by_title(self, title):
        return next((c for c in self.courses if c.title == title), None)

    def find_course_by_id(self, course_id):
        return next((c for c in self.courses if c.id == course_id), None)

    # --- Методы УПРАВЛЕНИЯ СВЯЗЯМИ ---

    def assign_teacher_to_course(self, course_id, teacher_id):
        """
        Назначает преподавателя на курс.
        """
        course = self.find_course_by_id(course_id)
        teacher = self.find_teacher_by_id(teacher_id) if teacher_id else None

        if course:
            course.teacher_id = teacher.id if teacher else None
            return True
        return False

    def enroll_student_in_course(self, student_id, course_id):
        """
        Зачисляет студента на курс.
        """
        course = self.find_course_by_id(course_id)
        student_exists = self.find_student_by_id(student_id) is not None

        if course and student_exists and student_id not in course.students:
            course.students.append(student_id)
            return True
        return False

    def set_grade_and_complete_course(self, course_id):
        """
        Завершает курс. Предполагается, что оценки уже выставлены вручную.
        """
        course = self.find_course_by_id(course_id)

        if course and course.status == "активен":
            course.status = "завершён"
            return True
        return False

    # --- Методы сохранения и загрузки ---

    def save_to_json(self):
        """Сохраняет текущее состояние в JSON."""
        data = {
            "students": [{"id": s.id, "name": s.name, "email": s.email, "history": s.history} for s in self.students],
            "teachers": [{"id": t.id, "name": t.name, "specialization": t.specialization} for t in self.teachers],
            "courses": [{
                "id": c.id,
                "title": c.title,
                "topic": c.topic,
                "status": c.status,
                "students": c.students,
                "teacher_id": c.teacher_id,
            } for c in self.courses],
            "next_ids": {
                "student": self._next_student_id,
                "teacher": self._next_teacher_id,
                "course": self._next_course_id,
            }
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        """Загружает данные из JSON при старте приложения."""
        if not os.path.exists("data.json"):
            return  # Если файла нет, просто работаем с пустыми списками.

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

            for s_data in data.get("students", []):
                student = Student(s_data["id"], s_data["name"], s_data["email"])
                student.history = s_data.get("history", [])
                self.students.append(student)

            for t_data in data.get("teachers", []):
                teacher = Teacher(t_data["id"], t_data["name"], t_data["specialization"])
                self.teachers.append(teacher)

            for c_data in data.get("courses", []):
                course = Course(c_data["id"], c_data["title"], c_data["topic"])
                course.status = c_data.get("status", "активен")
                course.students = c_data.get("students", [])
                course.teacher_id = c_data.get("teacher_id")
                self.courses.append(course)

            next_ids = data.get("next_ids", {})
            self._next_student_id = next_ids.get("student", len(self.students) + 1)
            self._next_teacher_id = next_ids.get("teacher", len(self.teachers) + 1)
            self._next_course_id = next_ids.get("course", len(self.courses) + 1)