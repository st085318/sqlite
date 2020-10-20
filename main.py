import sqlite3
from structures import Student, Subject, Grade, Grade_data


def create_database():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        country TEXT,
        birthday INTEGER,
        gang INTEGER);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        teacher TEXT);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS grades(
        grade_id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        data INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects (subjects_id),
        FOREIGN KEY (student_id) REFERENCES students (student_id));
    """)
    conn.commit()
    conn.close()


def insert_data_from_table_to_db(path_to_table):
    table_of_grades = open(path_to_table, 'r', encoding='utf8')
    for i in range(10):
        grade_with_data = table_of_grades.readline()
        list_input_data = grade_with_data.split(";")
        grade_info = Grade_data(int(list_input_data[0].replace('\ufeff', '')), list_input_data[1], int(list_input_data[2]), list_input_data[3],
                           list_input_data[4], int(list_input_data[5]))
        student = Student(grade_info.student_name, grade_info.student_surname, grade_info.students_gang)
        student_id = student.get_or_create_student_id()
        subject = Subject(grade_info.subject)
        subject_id = subject.get_or_create_subject_id()
        grade = Grade(student_id, subject_id, grade_info.grade, grade_info.data)
        #print(str(student_id) + " " + str(subject_id) + " " +str(grade_id))


if __name__ == '__main__':
    create_database()
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    insert_data_from_table_to_db("as.csv")
    cur.execute("SELECT * FROM grades")
    print(cur.fetchall())


