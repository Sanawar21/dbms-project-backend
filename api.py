# api.py
from fastapi import Body
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from starlette.requests import Request

from google import genai
from google.genai import types

import os
import mysql.connector

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


@router.get("/api/teacher/course_labs/{course_code}")
async def get_teacher_course_labs(course_code: str):
    connection, cursor = get_db_connection_and_cursor()

    try:
        cursor.execute("""
            SELECT 
                l.*, 
                c.COURSE_TITLE
            FROM Lab_Task l
            JOIN Courses c ON l.COURSE_CODE = c.COURSE_CODE
            WHERE l.COURSE_CODE = %s
        """, (course_code,))

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


@router.get("/api/submissions/{course_code}/{lab_no}")
async def get_lab_submissions(course_code: str, lab_no: int):
    connection, cursor = get_db_connection_and_cursor()
    try:
        cursor.execute("""
            SELECT 
                s.ROLL_NO,
                s.STUDENT_NAME,
                s.EMAIL,
                sub.STATUS AS SUBMISSION_STATUS,
                lt.LAB_TITLE,
                q.TASK_NO,
                q.QUESTION_TEXT,
                a.ANSWER_TEXT,
                a.IS_CORRECT
            FROM STUDENT s
            JOIN SUBMISSION sub ON s.ROLL_NO = sub.ROLL_NO
            JOIN ANSWER a ON s.ROLL_NO = a.ROLL_NO 
                          AND a.COURSE_CODE = sub.COURSE_CODE 
                          AND a.LAB_NO = sub.LAB_NO
            JOIN QUESTION q ON q.COURSE_CODE = a.COURSE_CODE 
                           AND q.LAB_NO = a.LAB_NO 
                           AND q.TASK_NO = a.TASK_NO
            JOIN LAB_TASK lt ON lt.COURSE_CODE = sub.COURSE_CODE AND lt.LAB_NO = sub.LAB_NO
            WHERE sub.COURSE_CODE = %s AND sub.LAB_NO = %s
            ORDER BY s.ROLL_NO, q.TASK_NO
        """, (course_code, lab_no))

        rows = cursor.fetchall()
        grouped = {}

        for row in rows:
            roll_no = row["ROLL_NO"]
            if roll_no not in grouped:
                grouped[roll_no] = {
                    "ROLL_NO": roll_no,
                    "STUDENT_NAME": row["STUDENT_NAME"],
                    "EMAIL": row["EMAIL"],
                    "LAB_TITLE": row["LAB_TITLE"],
                    "SUBMISSION_STATUS": row["SUBMISSION_STATUS"],
                    "questions": []
                }

            grouped[roll_no]["questions"].append({
                "TASK_NO": row["TASK_NO"],
                "QUESTION_TEXT": row["QUESTION_TEXT"],
                "ANSWER_TEXT": row["ANSWER_TEXT"],
                "IS_CORRECT": row["IS_CORRECT"]
            })

        return {"success": True, "submissions": list(grouped.values())}

    finally:
        cursor.close()
        connection.close()


@router.post("/api/check_submission")
async def check_submission(data: dict = Body(...)):
    results = data.get("results", [])
    if not results:
        return {"success": False, "message": "No data provided."}

    connection, cursor = get_db_connection_and_cursor()
    try:
        updated = set()
        for entry in results:
            cursor.execute("""
                UPDATE ANSWER
                SET IS_CORRECT = %s
                WHERE ROLL_NO = %s AND COURSE_CODE = %s AND LAB_NO = %s AND TASK_NO = %s
            """, (
                entry["is_correct"],
                entry["roll_no"],
                entry["course_code"],
                entry["lab_no"],
                entry["task_no"]
            ))

            # Track which (ROLL_NO, COURSE_CODE, LAB_NO) to update in SUBMISSION table
            updated.add(
                (entry["roll_no"], entry["course_code"], entry["lab_no"]))

        # Update submission status for all students who were checked
        for roll_no, course_code, lab_no in updated:
            cursor.execute("""
                UPDATE SUBMISSION
                SET STATUS = 'Checked'
                WHERE ROLL_NO = %s AND COURSE_CODE = %s AND LAB_NO = %s
            """, (roll_no, course_code, lab_no))

        connection.commit()
        return {"success": True, "message": "Submissions checked successfully."}

    finally:
        cursor.close()
        connection.close()


@router.get("/api/student/all_labs/{roll_no}/{course_code}")
async def get_all_labs_of_student(roll_no: int, course_code: str):
    connection, cursor = get_db_connection_and_cursor()
    try:
        cursor.execute("""
            SELECT 
                s.ROLL_NO,
                s.STUDENT_NAME,
                s.EMAIL,
                sub.STATUS AS SUBMISSION_STATUS,
                lt.LAB_TITLE,
                lt.LAB_NO,
                q.TASK_NO,
                q.QUESTION_TEXT,
                a.ANSWER_TEXT,
                a.IS_CORRECT
            FROM STUDENT s
            LEFT JOIN LAB_TASK lt 
                ON lt.COURSE_CODE = %s
            LEFT JOIN SUBMISSION sub 
                ON s.ROLL_NO = sub.ROLL_NO 
                AND sub.COURSE_CODE = lt.COURSE_CODE 
                AND sub.LAB_NO = lt.LAB_NO
            LEFT JOIN QUESTION q 
                ON q.COURSE_CODE = lt.COURSE_CODE 
                AND q.LAB_NO = lt.LAB_NO
            LEFT JOIN ANSWER a 
                ON a.ROLL_NO = s.ROLL_NO 
                AND a.COURSE_CODE = q.COURSE_CODE 
                AND a.LAB_NO = q.LAB_NO 
                AND a.TASK_NO = q.TASK_NO
            WHERE s.ROLL_NO = %s AND lt.COURSE_CODE = %s
            ORDER BY lt.LAB_NO, q.TASK_NO
        """, (course_code, roll_no, course_code))

        rows = cursor.fetchall()

        result = {
            "ROLL_NO": roll_no,
            "STUDENT_NAME": None,
            "EMAIL": None,
            "labs": {}
        }

        for row in rows:
            if result["STUDENT_NAME"] is None:
                result["STUDENT_NAME"] = row["STUDENT_NAME"]
                result["EMAIL"] = row["EMAIL"]

            lab_key = (row["LAB_NO"], row["LAB_TITLE"])
            if lab_key not in result["labs"]:
                result["labs"][lab_key] = {
                    "LAB_NO": row["LAB_NO"],
                    "LAB_TITLE": row["LAB_TITLE"],
                    "SUBMISSION_STATUS": row["SUBMISSION_STATUS"],
                    "questions": []
                }

            result["labs"][lab_key]["questions"].append({
                "TASK_NO": row["TASK_NO"],
                "QUESTION_TEXT": row["QUESTION_TEXT"],
                "ANSWER_TEXT": row["ANSWER_TEXT"],
                "IS_CORRECT": row["IS_CORRECT"]
            })

        # Convert dict to list for JSON response
        result["labs"] = list(result["labs"].values())

        return {"success": True, "student_data": result}

    finally:
        cursor.close()
        connection.close()


@router.post("/api/teacher/ai_check")
async def submit_questions(data: dict = Body(...)):
    questions = data.get("questions", [])
    answers = data.get("answers", [])

    if not questions or not answers or len(questions) != len(answers):
        return {"success": False, "message": "Questions and answers must be non-empty and of equal length."}

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return {"success": False, "message": "Gemini API key not set."}

    client = genai.Client(api_key=gemini_key)
    model = "gemini-2.0-flash-lite"
    prompt_lines = [
        "You are an automated grader.",
        "Below is a list of questions and student answers.",
        "For each answer, return 1 if it is correct, otherwise return 0.",
        "Respond ONLY with a list of 0s and 1s in the same order.",
        "Format: [1, 0, 1, ...]",
        "",
        "Questions and Answers:"
    ]

    for i, (q, a) in enumerate(zip(questions, answers), 1):
        prompt_lines.append(f"{i}. Q: {q}\n   A: {a}")

    full_prompt = "\n".join(prompt_lines)

    try:
        response = client.models.generate_content(
            model=model,
            contents=full_prompt
        )
        text = response.text.strip()
        # Try to safely evaluate the list
        result = eval(text) if text.startswith("[") else []
        if not isinstance(result, list) or not all(i in (0, 1) for i in result):
            raise ValueError("Unexpected output format.")
    except Exception as e:
        print(f"Gemini error: {e}")
        return {"success": False, "message": "AI evaluation failed."}

    return {
        "success": True,
        "results": result
    }
