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
    grade_with_data = table_of_grades.readline()
    while grade_with_data != "":
        list_input_data = grade_with_data.split(";")
        grade_info = Grade_data(int(list_input_data[0].replace('\ufeff', '')), list_input_data[1], int(list_input_data[2]), list_input_data[3],
                           list_input_data[4], int(list_input_data[5]))
        student = Student(grade_info.student_name, grade_info.student_surname, grade_info.students_gang)
        student_id = student.get_or_create_student_id()
        subject = Subject(grade_info.subject)
        subject_id = subject.get_or_create_subject_id()
        grade = Grade(student_id, subject_id, grade_info.grade, grade_info.data)
        grade_with_data = table_of_grades.readline()
    table_of_grades.close()


def get_average_mark_in_subject(subject):
    subj = Subject(subject)
    subject_id = subj.subject_id
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    set_students_id = set()
    cur.execute("""SELECT * FROM grades WHERE subject_id=?""", (subject_id,))
    grades = cur.fetchall()
    amount = 0
    marks_sum = 0
    average_mark = {}
    for grade in grades:
        set_students_id.add(grade[1])
    for student_id in set_students_id:
        amount = 0
        marks_sum = 0
        for grade in grades:
            if grade[1] == student_id:
                amount += 1
                marks_sum += grade[4]
        if amount == 0:  # defence from zero division error
            amount = 1
        cur.execute("""SELECT first_name FROM students WHERE student_id = ?""", (student_id,))
        student_name = cur.fetchall()
        student_first_name = str(student_name[0][0])
        cur.execute("""SELECT second_name FROM students WHERE student_id = ?""", (student_id,))
        student_name = cur.fetchall()
        student_second_name = str(student_name[0][0])
        average_mark.update({student_first_name+" "+student_second_name: float(marks_sum) / float(amount)})
    return average_mark


def get_average_mark_in_group(gang):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    set_students_id = set()
    cur.execute("SELECT * FROM grades ")
    grades = cur.fetchall()
    cur.execute("SELECT subject_id FROM grades ")
    subject_ids = cur.fetchall()
    cur.execute("SELECT student_id FROM students WHERE gang = ?", (gang,))
    students_in_group = cur.fetchall()
    subject_and_marks = {}
    for grade in grades:
        if (grade[1],) in students_in_group:
            set_students_id.add(grade[1])
    for subject_id in subject_ids:
        average_mark = {}
        for student_id in set_students_id:
            amount = 0
            marks_sum = 0
            for grade in grades:
                if grade[1] == student_id and (grade[2],) == subject_id:
                    amount += 1
                    marks_sum += grade[4]
            if amount == 0:  # defence from zero division error
                amount = 1
            cur.execute("""SELECT first_name FROM students WHERE student_id = ?""", (student_id,))
            student_name = cur.fetchall()
            student_first_name = str(student_name[0][0])
            cur.execute("""SELECT second_name FROM students WHERE student_id = ?""", (student_id,))
            student_name = cur.fetchall()
            student_second_name = str(student_name[0][0])
            average_mark.update({student_first_name+" "+student_second_name: float(marks_sum) / float(amount)})
        for student_id in students_in_group[0]:
            if not student_id in set_students_id:
                cur.execute("""SELECT first_name FROM students WHERE student_id = ?""", (student_id,))
                student_name = cur.fetchall()
                student_first_name = str(student_name[0][0])
                cur.execute("""SELECT second_name FROM students WHERE student_id = ?""", (student_id,))
                student_name = cur.fetchall()
                student_second_name = str(student_name[0][0])
                average_mark.update({student_first_name + " " + student_second_name: 0.0})
        cur.execute("SELECT title FROM subjects WHERE subject_id = ?", subject_id)
        subject_title = cur.fetchall()[0][0]
        subject_and_marks.update({subject_title: average_mark})
    return subject_and_marks


def get_average_mark_in_group_in_subject(gang, subject):
    subjects_and_average_marks = get_average_mark_in_group(gang)
    return subjects_and_average_marks.get(subject)


def clean_grades():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM grades;")
    conn.commit()
    conn.close()


def clean_students():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM students;")
    conn.commit()
    conn.close()


def clean_subjects():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM subjects;")
    conn.commit()
    conn.close()


def clean_base_data():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM grades;")
    cur.execute("DELETE FROM students;")
    cur.execute("DELETE FROM subjects;")
    conn.commit()
    conn.close()


def help_text():
    print("what you want to do?")
    print("input 1 to add new data in base")
    print("input 2 to clean all data in base")
    print("input 3 to clean table with subjects")
    print("input 4 to clean table with students")
    print("input 5 to clean table with grades")
    print("input 6 to get average mark in subject")
    print("input 7 to get average mark in group")
    print("input 8 to get average mark in group in subject")
    print("input -1 to get help")
    print("input 0 to exit")


if __name__ == '__main__':
    create_database()
    help_text()
    mode = int(input())
    while mode != 0:
        try:
            if mode == 1:
                print("input path to table")
                insert_data_from_table_to_db(input())
                print("DONE!")
            elif mode == 2:
                clean_base_data()
                print("Database cleared")
            elif mode == 3:
                clean_subjects()
                print("Table cleared")
            elif mode == 4:
                clean_students()
                print("Table cleared")
            elif mode == 5:
                clean_grades()
                print("Table cleared")
            elif mode == 6:
                print("Enter a subject name")
                average_marks = get_average_mark_in_subject(input())
                if average_marks == {}:
                    print("There isn't this subject")
                for average_mark_in_subject in average_marks:
                    if average_marks.get(average_mark_in_subject) != 0.0:
                        print(str(average_mark_in_subject) + " " +
                              str(average_marks.get(average_mark_in_subject)))
                    else:
                        print(str(average_mark_in_subject) + " no marks")
            elif mode == 7:
                print("Enter a group number")
                average_marks = get_average_mark_in_group(int(input()))
                for subject in average_marks:
                    print(subject)
                    for average_mark_in_subject in average_marks.get(subject):
                        if average_marks.get(subject).get(average_mark_in_subject) != 0.0:
                            print(str(average_mark_in_subject) + " " +
                                  str(average_marks.get(subject).get(average_mark_in_subject)))
                        else:
                            print(str(average_mark_in_subject) + " no marks")
            elif mode == 8:
                print("Enter a group number and a subject name")
                average_marks = get_average_mark_in_group_in_subject(int(input()), input())
                if average_marks == None:
                    print("There isn't this subject")
                else:
                    for average_mark_in_subject in average_marks:
                        if average_marks.get(average_mark_in_subject) != 0.0:
                            print(str(average_mark_in_subject) + " " +
                                  str(average_marks.get(average_mark_in_subject)))
                        else:
                            print(str(average_mark_in_subject) + " no marks")
            elif mode == -1:
                help_text()
            elif mode == 0:
                break
            print("Choose a work mode")
            mode = int(input())
        except IndexError:
            print("There isn't this group")
            print("Choose a work mode")
            mode = int(input())
        except BaseException:
            print("Oops, error")
            print("Choose a work mode")
            mode = int(input())
    print("Goodbye")
