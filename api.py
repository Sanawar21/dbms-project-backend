# api.py
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from starlette.requests import Request

import os
import mysql.connector

# THIS IS THE DATABASE SCHEMA
# DROP DATABASE IF EXISTS dbms;
# CREATE DATABASE dbms;
# USE dbms;

# CREATE TABLE IF NOT EXISTS COURSES(
#     COURSE_CODE VARCHAR(10) PRIMARY KEY,
#     COURSE_TITLE VARCHAR(100) UNIQUE
# );

# CREATE TABLE IF NOT EXISTS LAB_TASK (
#     COURSE_CODE VARCHAR(10),
#     LAB_NO INT(5),
#     LAB_TITLE VARCHAR(100) UNIQUE,
#     PRIMARY KEY (COURSE_CODE, LAB_NO),
#     FOREIGN KEY (COURSE_CODE) REFERENCES COURSES(COURSE_CODE)
# );

# CREATE TABLE IF NOT EXISTS LAB_INFO (
#     LAB_TITLE VARCHAR(100),
#     DEADLINE DATE,
#     FOREIGN KEY (LAB_TITLE) REFERENCES LAB_TASK(LAB_TITLE),
#     PRIMARY KEY (LAB_TITLE)
# );


# CREATE TABLE IF NOT EXISTS STUDENT(
#     ROLL_NO INT(10),
#     BATCH INT(4),
#     STUDENT_NAME VARCHAR(200),
#     SEMESTER VARCHAR(10),
#     EMAIL VARCHAR(100) UNIQUE,
#     PASSWORD VARCHAR(100),
#     PRIMARY KEY (ROLL_NO),
#     CONSTRAINT chk_roll_no CHECK (ROLL_NO BETWEEN 10000 AND 99999)
# );

# CREATE TABLE IF NOT EXISTS STUDENT_COURSE(
#     ROLL_NO INT(10),
#     COURSE_CODE VARCHAR(10),
#     PRIMARY KEY (ROLL_NO, COURSE_CODE),
#     FOREIGN KEY (ROLL_NO) REFERENCES STUDENT(ROLL_NO),
#     FOREIGN KEY (COURSE_CODE) REFERENCES COURSES(COURSE_CODE)
# );


# CREATE TABLE IF NOT EXISTS TEACHER (
#     TEACHER_ID INT(10) PRIMARY KEY,
#     TEACHER_NAME VARCHAR(100),
#     EMAIL VARCHAR(100) UNIQUE,
#     PASSWORD VARCHAR(100)
# );

# CREATE TABLE IF NOT EXISTS TEACHER_COURSE (
#     TEACHER_ID INT(10),
#     COURSE_CODE VARCHAR(10),
#     PRIMARY KEY (TEACHER_ID, COURSE_CODE),
#     FOREIGN KEY (TEACHER_ID) REFERENCES TEACHER(TEACHER_ID),
#     FOREIGN KEY (COURSE_CODE) REFERENCES COURSES(COURSE_CODE)
# );
# CREATE TABLE IF NOT EXISTS QUESTION (
#     COURSE_CODE VARCHAR(10),
#     LAB_NO INT(5),
#     TASK_NO INT(5),
#     QUESTION_TEXT TEXT,
#     PRIMARY KEY (COURSE_CODE, LAB_NO, TASK_NO),
#     FOREIGN KEY (COURSE_CODE, LAB_NO) REFERENCES LAB_TASK(COURSE_CODE, LAB_NO) ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS ANSWER (
#     COURSE_CODE VARCHAR(10),
#     LAB_NO INT(5),
#     TASK_NO INT(5),
#     ROLL_NO INT(10),
#     ANSWER_TEXT TEXT,
#     IS_CORRECT BOOLEAN,
#     PRIMARY KEY (COURSE_CODE, LAB_NO, TASK_NO, ROLL_NO),
#     FOREIGN KEY (COURSE_CODE, LAB_NO, TASK_NO) REFERENCES QUESTION(COURSE_CODE, LAB_NO, TASK_NO) ON DELETE CASCADE,
#     FOREIGN KEY (ROLL_NO) REFERENCES STUDENT(ROLL_NO) ON DELETE CASCADE
# );

# CREATE TABLE IF NOT EXISTS SUBMISSION (
#     SUBMISSION_ID INT AUTO_INCREMENT PRIMARY KEY,
#     COURSE_CODE VARCHAR(10),
#     ROLL_NO INT(10),
#     LAB_NO INT(5),
#     STATUS VARCHAR(100),
#     SUBMISSION_DATE DATE,
#     FOREIGN KEY (ROLL_NO) REFERENCES STUDENT(ROLL_NO),
#     FOREIGN KEY (COURSE_CODE, LAB_NO) REFERENCES LAB_TASK(COURSE_CODE, LAB_NO) ON DELETE CASCADE
# );

router = APIRouter()


def get_db_connection_and_cursor():
    """Create a new database connection."""
    conn = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME")
    )
    return conn, conn.cursor(dictionary=True)


@router.post("/api/authenticate")
async def authenticate(request: Request, email: str = Form(...), password: str = Form(...)):
    # Connect to the database
    connection, cursor = get_db_connection_and_cursor()
    try:
        # Search in Teacher table
        cursor.execute("SELECT * FROM Teacher WHERE email = %s", (email,))
        teacher = cursor.fetchone()

        if teacher and teacher["PASSWORD"] == password:
            teacher["type"] = "teacher"
            request.session["user"] = teacher
            return JSONResponse(content={"success": True, "message": "Login successful", "user": teacher})

        # Search in Student table
        cursor.execute("SELECT * FROM Student WHERE email = %s", (email,))
        student = cursor.fetchone()

        if student and student["PASSWORD"] == password:
            student["type"] = "student"
            request.session["user"] = student
            return JSONResponse(content={"success": True, "message": "Login successful", "user": student})

        # If no match found
        return JSONResponse(content={"success": False, "message": "Incorrect email or password"}, status_code=401)

    finally:
        cursor.close()
        connection.close()


@router.get("/api/student_courses/{roll_no}")
async def get_student_courses(roll_no: int):
    # Connect to the database
    connection, cursor = get_db_connection_and_cursor()

    try:
        # Fetch courses for the student
        cursor.execute("""
          SELECT * FROM Courses c
          WHERE c.COURSE_CODE IN (
            SELECT sc.COURSE_CODE
            FROM Student_Course sc
            WHERE sc.ROLL_NO = %s
          )
        """, (roll_no,))
        courses = cursor.fetchall()

        return JSONResponse(content={"success": True, "courses": courses})

    finally:
        cursor.close()
        connection.close()


@router.get("/api/course_name/{course_code}")
async def get_course_name(course_code: str):
    # Connect to the database
    connection, cursor = get_db_connection_and_cursor()

    try:
        # Fetch course name
        cursor.execute(
            "SELECT COURSE_TITLE FROM Courses WHERE COURSE_CODE = %s", (course_code,))
        course = cursor.fetchone()

        if course:
            return JSONResponse(content={"success": True, "course_name": course["COURSE_TITLE"]})
        else:
            return JSONResponse(content={"success": False, "message": "Course not found"}, status_code=404)

    finally:
        cursor.close()
        connection.close()


@router.get("/api/teacher_courses/{teacher_id}")
async def get_teacher_courses(teacher_id: int):
    # Connect to the database
    connection, cursor = get_db_connection_and_cursor()

    try:
        # Fetch courses for the teacher
        cursor.execute("""
          SELECT * FROM Courses c
          WHERE c.COURSE_CODE IN (
            SELECT tc.COURSE_CODE
            FROM Teacher_Course tc
            WHERE tc.TEACHER_ID = %s
          )
        """, (teacher_id,))
        courses = cursor.fetchall()

        return JSONResponse(content={"success": True, "courses": courses})

    finally:
        cursor.close()
        connection.close()


@router.get("/api/current_user")
async def get_current_user(request: Request):
    user = request.session.get("user")
    if user:
        return JSONResponse(content={"success": True, "user": user})
    return JSONResponse(content={"success": False, "message": "Not logged in"}, status_code=401)


@router.get("/api/course_labs/{course_code}")
async def get_course_labs(course_code: str, request: Request):
    connection, cursor = get_db_connection_and_cursor()
    roll_no = request.session.get("user")["ROLL_NO"]

    try:
        cursor.execute("""
            SELECT 
                l.*, 
                c.COURSE_TITLE,
                s.STATUS AS SUBMISSION_STATUS
            FROM Lab_Task l
            JOIN Courses c ON l.COURSE_CODE = c.COURSE_CODE
            LEFT JOIN Submission s 
                ON s.COURSE_CODE = l.COURSE_CODE 
               AND s.LAB_NO = l.LAB_NO 
               AND s.ROLL_NO = %s
            WHERE l.COURSE_CODE = %s
        """, (roll_no, course_code))

        labs = cursor.fetchall()
        return labs

    finally:
        cursor.close()
        connection.close()


@router.get("/api/lab_tasks/{course_code}/{lab_no}")
async def get_lab_tasks(course_code: str, lab_no: int, request: Request):
    connection, cursor = get_db_connection_and_cursor()
    roll_no = request.session.get("user")["ROLL_NO"]

    try:
        # Get questions with submission and answer status
        cursor.execute("""
            SELECT 
                q.TASK_NO, 
                q.QUESTION_TEXT, 
                c.COURSE_TITLE, 
                l.LAB_TITLE,
                s.STATUS AS SUBMISSION_STATUS,
                a.ANSWER_TEXT,
                a.IS_CORRECT
            FROM QUESTION q
            JOIN COURSES c ON q.COURSE_CODE = c.COURSE_CODE
            JOIN LAB_TASK l ON q.COURSE_CODE = l.COURSE_CODE AND q.LAB_NO = l.LAB_NO
            LEFT JOIN SUBMISSION s ON s.COURSE_CODE = q.COURSE_CODE AND s.LAB_NO = q.LAB_NO AND s.ROLL_NO = %s
            LEFT JOIN ANSWER a ON a.COURSE_CODE = q.COURSE_CODE AND a.LAB_NO = q.LAB_NO AND a.TASK_NO = q.TASK_NO AND a.ROLL_NO = %s
            WHERE q.COURSE_CODE = %s AND q.LAB_NO = %s
            ORDER BY q.TASK_NO ASC
        """, (roll_no, roll_no, course_code, lab_no))

        tasks = cursor.fetchall()
        return JSONResponse(content={"success": True, "questions": tasks})

    finally:
        cursor.close()
        connection.close()


@router.post("/api/submit_lab")
async def submit_lab(
    request: Request,
    course_code: str = Form(...),
    lab_no: int = Form(...)
):
    connection, cursor = get_db_connection_and_cursor()

    try:
        roll_no = request.session.get("user")["ROLL_NO"]
        if not roll_no:
            return JSONResponse(content={"success": False, "message": "User not logged in"}, status_code=401)

        form_data = await request.form()
        # Extract answers in order: answer_1, answer_2, ...
        answers = []
        for key in sorted(form_data.keys(), key=lambda k: int(k.split('_')[1]) if k.startswith('answer_') and k.split('_')[1].isdigit() else 0):
            if key.startswith('answer_'):
                answers.append(form_data[key])
        # Now 'answers' is a list of answer strings in order

        cursor.execute("""
            INSERT INTO SUBMISSION (COURSE_CODE, ROLL_NO, LAB_NO, STATUS, SUBMISSION_DATE)
            VALUES (%s, %s, %s, 'Submitted', NOW())
        """, (course_code, roll_no, lab_no))

        for task_no, answer in enumerate(answers, start=1):
            cursor.execute("""
                INSERT INTO ANSWER (COURSE_CODE, LAB_NO, TASK_NO, ROLL_NO, ANSWER_TEXT)
                VALUES (%s, %s, %s, %s, %s)
            """, (course_code, lab_no, task_no, roll_no, answer))

        connection.commit()

        return JSONResponse(content={"success": True, "redirect": f"/course/{course_code}"})

    finally:
        cursor.close()
        connection.close()


@router.get("/api/teacher/students/{course_code}")
async def get_students_by_course(course_code: str):
    connection, cursor = get_db_connection_and_cursor()
    # Get all students in the course, and for each student, get all labs and their submission status

    try:
        cursor.execute("""
            SELECT 
                s.ROLL_NO, 
                s.STUDENT_NAME, 
                s.EMAIL, 
                l.LAB_NO, 
                l.LAB_TITLE,
                sub.status AS SUBMISSION_STATUS
            FROM STUDENT s
            JOIN STUDENT_COURSE sc ON s.ROLL_NO = sc.ROLL_NO
            CROSS JOIN LAB_TASK l ON l.COURSE_CODE = sc.COURSE_CODE
            LEFT JOIN SUBMISSION sub 
                ON sub.ROLL_NO = s.ROLL_NO 
                AND sub.COURSE_CODE = l.COURSE_CODE 
                AND sub.LAB_NO = l.LAB_NO
            WHERE sc.COURSE_CODE = %s
            ORDER BY s.ROLL_NO, l.LAB_NO
        """, (course_code,))

        students = cursor.fetchall()

        return JSONResponse(content={"success": True, "students": students})

    finally:
        cursor.close()
        connection.close()
