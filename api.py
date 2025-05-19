# api.py
from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from fastapi import Depends

import os
import mysql.connector


router = APIRouter()

# VALID_USERS = {
#     "ali@neduet.pk": {"name": "Ali", "email": "ali@neduet.pk", "role": "student"},
#     "fatima@neduet.pk": {"name": "Fatima", "email": "fatima@neduet.pk", "role": "teacher"}
# }


# @router.post("/api/authenticate")
# async def authenticate(request: Request, email: str = Form(...), password: str = Form(...)):
#     # Simulate checking password
#     if email in VALID_USERS and password == "pass123":  # static password for now
#         user = VALID_USERS[email]
#         request.session["user"] = user  # ✅ Set user in session
#         return JSONResponse(content={"success": True, "message": "Login successful"})

#     return JSONResponse(content={"success": False, "message": "Incorrect email or password"}, status_code=401)

@router.post("/api/authenticate")
async def authenticate(request: Request, email: str = Form(...), password: str = Form(...)):
    # Connect to the database
    connection = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME")
    )
    cursor = connection.cursor(dictionary=True)

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
