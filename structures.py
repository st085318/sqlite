from collections import namedtuple
import sqlite3

Grade_data = namedtuple('Grade_data', [
    'grade',
    'subject',
    'data',
    'student_name',
    'student_surname',
    'students_gang'
])


class Student:
    def __init__(self, first_name, second_name, gang, country=None, birthday=None):
        self.first_name = first_name
        self.second_name = second_name
        self.gang = gang
        self.country = country
        self.birthday = birthday
        self.student_id = self.get_or_create_student_id()

    def get_or_create_student_id(self):
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students where first_name = ? and second_name = ? and gang = ?",
                    [self.first_name, self.second_name, self.gang])
        student_id = cur.fetchall()
        if student_id == []:
            cur.execute("SELECT MAX(student_id) FROM students")
            max_student_id = cur.fetchall()[0][0]
            if max_student_id is None:
                cur.execute("""INSERT INTO students (student_id, first_name, second_name, gang)
                    VALUES
                    (1, ?, ?, ?);
                """, [self.first_name, self.second_name, self.gang])
                conn.commit()
                conn.close()
                return 1
            else:
                cur.execute("""INSERT INTO students (student_id, first_name, second_name, gang)
                                    VALUES
                                    (?, ?, ?, ?);
                                """, [max_student_id+1, self.first_name, self.second_name, self.gang])
            conn.commit()
            conn.close()
            return max_student_id+1
        else:
            conn.commit()
            conn.close()
            return student_id[0][0]


class Subject:
    def __init__(self, title, teacher=None):
        self.title = title
        self.teacher = teacher
        self.subject_id = self.get_or_create_subject_id()

    def get_or_create_subject_id(self):
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("SELECT subject_id FROM subjects where title = ?",
                    [self.title])
        subject_id = cur.fetchall()
        if not subject_id:
            cur.execute("SELECT MAX(subject_id) FROM subjects")
            max_subject_id = cur.fetchall()[0][0]
            if max_subject_id is None:
                cur.execute("""INSERT INTO subjects (subject_id, title, teacher)
                    VALUES
                    (?, ?, ?);
                """, [1, self.title, self.teacher])
                conn.commit()
                conn.close()
                return 1
            else:
                cur.execute("""INSERT INTO subjects (subject_id, title, teacher)
                                    VALUES
                                    (?, ?, ?);
                                """, [max_subject_id+1, self.title, self.teacher])
            conn.commit()
            conn.close()
            return max_subject_id+1
        else:
            try:
                return subject_id[0][0]
            except ValueError:
                return subject_id


class Grade:
    def __init__(self, student_id, subject_id, grade, data):
        self.student_id = student_id
        self.subject_id = subject_id
        self.grade = grade
        self.data = data
        self.grade_id = self.create_grade_id()

    def create_grade_id(self):
        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("SELECT MAX(grade_id) FROM grades")
        max_grade_id = cur.fetchall()[0][0]
        if max_grade_id is None:
            cur.execute("""INSERT INTO grades (grade_id, student_id, subject_id, grade, data)
                VALUES
                (1, ?, ?, ?, ?);
            """, [self.student_id, self.subject_id, self.grade, self.data])
            conn.commit()
            conn.close()
            return 1
        else:
            cur.execute("""INSERT INTO grades (grade_id, student_id, subject_id, grade, data)
                                VALUES
                                (?, ?, ?, ?, ?);
                            """, [max_grade_id+1, self.student_id, self.subject_id, self.grade, self.data])
        conn.commit()
        conn.close()
        return max_grade_id + 1
