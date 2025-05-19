import mysql.connector
import os
from dotenv import load_dotenv
from faker import Faker
import random

# Initialize Faker
fake = Faker()

load_dotenv()


def with_connection(func):
    def wrapper(*args, **kwargs):
        # Database connection
        conn = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME")
        )
        cursor = conn.cursor()
        return func(conn, cursor, *args, **kwargs)
    return wrapper


@with_connection
def execute_sql_file(conn, cursor, file_path):
    """Execute SQL commands from a file."""
    with open(file_path, 'r') as file:
        sql_commands = file.read()
    for command in sql_commands.split(';'):
        if command.strip():
            cursor.execute(command)
    conn.commit()


@with_connection
def populate_teachers(conn, cursor):
    """Populate the TEACHER and TEACHER_COURSE tables."""
    teachers = [
        (1, "Dr. Alice", "dralice@gmail.com", "password"),
        (2, "Dr. Bob", "drbob@gmail.com", "password"),
    ]
    teacher_courses = [
        (1, "CS101"),
        (1, "CS102"),
        (2, "CS103"),
        (2, "CS104"),
    ]
    cursor.executemany(
        "INSERT INTO TEACHER (TEACHER_ID, TEACHER_NAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s)",
        teachers
    )
    cursor.executemany(
        "INSERT INTO TEACHER_COURSE (TEACHER_ID, COURSE_CODE) VALUES (%s, %s)",
        teacher_courses
    )
    conn.commit()
    print("Successfully inserted teachers and their courses.")


@with_connection
def populate_students(conn, cursor):
    """Populate the STUDENT and STUDENT_COURSE tables."""
    students = []
    student_courses = []
    roll_nos = set()
    for _ in range(30):
        batch = random.randint(2021, 2024)
        roll_no = int(f"{batch-2000}{random.randint(100, 999)}")
        while roll_no in roll_nos:
            roll_no = int(f"{batch-2000}{random.randint(100, 999)}")
        student_name = fake.name()
        semester = f"{['Spring', 'Fall'][random.randint(0, 1)]}"
        roll_nos.add(roll_no)
        students.append((roll_no, batch, student_name, semester,
                        f"{student_name.replace(' ', '').lower()}@gmail.com", "password"))

        # Enroll students in courses
        if batch == 2021:
            student_courses.append((roll_no, "CS101"))
        elif batch == 2022:
            student_courses.append((roll_no, "CS102"))
        elif batch == 2023:
            student_courses.append((roll_no, "CS103"))
        elif batch == 2024:
            student_courses.append((roll_no, "CS104"))

        # Enroll in one additional random course
        additional_course = random.choice(["CS101", "CS102", "CS103", "CS104"])
        while additional_course == student_courses[-1][1]:
            additional_course = random.choice(
                ["CS101", "CS102", "CS103", "CS104"])
        student_courses.append((roll_no, additional_course))

    cursor.executemany(
        "INSERT INTO STUDENT (ROLL_NO, BATCH, STUDENT_NAME, SEMESTER, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s, %s, %s)",
        students
    )
    cursor.executemany(
        "INSERT INTO STUDENT_COURSE (ROLL_NO, COURSE_CODE) VALUES (%s, %s)",
        student_courses
    )
    conn.commit()
    print("Successfully inserted students and their courses.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    # Step 1: Execute the SQL file to create tables
    execute_sql_file("tables.sql")
    execute_sql_file("CS101.sql")
    execute_sql_file("CS102.sql")
    execute_sql_file("CS103.sql")
    execute_sql_file("CS104.sql")

    os.chdir("..")

    # Step 3: Populate the TEACHER and TEACHER_COURSE tables
    populate_teachers()

    # Step 4: Populate the STUDENT and STUDENT_COURSE tables
    populate_students()
