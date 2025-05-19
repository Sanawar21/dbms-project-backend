from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from api import router as api_router  # <-- Import API routes

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
app.include_router(api_router)  # <-- Register routes
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sample Course Data
courses = [
    {"id": 1, "name": "Database Management Systems", "code": "CS301"},
    {"id": 2, "name": "Data Structures & Algorithms", "code": "CS302"}
]

dbms_lab_questions = [
    {"id": 1, "text": "Which of the following is a primary key in a relational database?",
        "type": "mcq", "options": ["A unique identifier", "A foreign key", "A redundant key", "An index"]},
    {"id": 2, "text": "What is the function of a foreign key?", "type": "mcq", "options": [
        "To establish a relationship", "To store duplicate values", "To act as a primary key", "None of the above"]},
    {"id": 3, "text": "Write an SQL query to retrieve all records from a table named 'Students' where the age is greater than 18.", "type": "text"},
    {"id": 4, "text": "Explain the difference between OLAP and OLTP.", "type": "text"},
    {"id": 5, "text": "What is the purpose of normalization in databases?", "type": "text"}
]

labs = [
    {"id": 1, "number": 2, "course_id": 1, "questions": dbms_lab_questions},
    {"id": 2, "number": 3, "course_id": 1, "questions": dbms_lab_questions}
]

students_sub = [
    {"id": 1, "name": "Ali", "course_id": 1, "submissions": [
        {"lab_id": 1, "answers": {"Q1": "A", "Q2": "A", "Q3": "SELECT * FROM Students WHERE age > 18;",
                                  "Q4": "OLAP vs OLTP explanation", "Q5": "Normalization is..."}},
        {"lab_id": 2, "answers": {"Q1": "A", "Q2": "B",
                                  "Q3": "SQL query", "Q4": "Explanation", "Q5": "Purpose"}}
    ]},
    {"id": 2, "name": "Fatima", "course_id": 1, "submissions": [
        {"lab_id": 1, "answers": {"Q1": "A", "Q2": "A",
                                  "Q3": "Some SQL", "Q4": "Some answer", "Q5": "Purpose"}}
    ]}
]

students = [
    {"id": 1, "name": "Ali Khan", "course_id": 1},
    {"id": 2, "name": "Sara Ahmed", "course_id": 1},
    {"id": 3, "name": "Zainab Fatima", "course_id": 2}
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/student_portal", response_class=HTMLResponse)
async def std_portal(request: Request):
    return templates.TemplateResponse("std_portal.html", {"request": request})


@app.get("/teacher_portal", response_class=HTMLResponse)
async def t_course(request: Request):
    return templates.TemplateResponse("teacher_portal.html", {"request": request, "courses": courses})


@app.get("/course", response_class=HTMLResponse)
async def course(request: Request):
    return templates.TemplateResponse("teacher_course.html", {"request": request, "courses": courses})


@app.get("/course/{course_id}/labs", response_class=HTMLResponse)
async def course_labs(course_id: int, request: Request):
    selected_labs = [lab for lab in labs if lab['course_id'] == course_id]
    course = next((c for c in courses if c['id'] == course_id), None)
    return templates.TemplateResponse("course_labs.html", {"request": request, "course": course, "labs": selected_labs})


@app.get("/course/{course_id}/lab/{lab_id}", response_class=HTMLResponse)
async def lab_task(course_id: int, lab_id: int, request: Request):
    lab = next((lab for lab in labs if lab['id'] ==
               lab_id and lab['course_id'] == course_id), None)
    course = next((c for c in courses if c['id'] == course_id), None)
    if not lab or not course:
        return HTMLResponse(content="Lab or course not found", status_code=404)
    return templates.TemplateResponse("lab_task.html", {"request": request, "course": course, "lab": lab, "questions": lab['questions']})


@app.post("/submit_lab/{course_id}/{lab_id}")
async def submit_lab(course_id: int, lab_id: int, request: Request):
    form_data = await request.form()
    answers = dict(form_data)
    print("User Answers:", answers)
    return RedirectResponse(url="/", status_code=302)


@app.get("/t_opt", response_class=HTMLResponse)
async def t_opt(request: Request):
    return templates.TemplateResponse("t_opt.html", {"request": request})


@app.get("/t_lab", response_class=HTMLResponse)
async def t_lab(request: Request):
    labs_with_course = []
    for lab in labs:
        course = next(
            (c for c in courses if c['id'] == lab['course_id']), None)
        labs_with_course.append({"lab": lab, "course": course})
    return templates.TemplateResponse("t_lab.html", {"request": request, "labs": labs_with_course})


@app.get("/std_list", response_class=HTMLResponse)
async def std_list(request: Request):
    return templates.TemplateResponse("std_list.html", {"request": request, "students": students})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("t_dashboard.html", {"request": request, "courses": courses, "labs": labs, "students": students})


@app.get("/student_details", response_class=HTMLResponse)
async def all_student_details(request: Request):
    all_details = []
    for student in students_sub:
        course = next(
            (c for c in courses if c['id'] == student['course_id']), None)
        submissions = []
        for sub in student.get('submissions', []):
            lab = next((l for l in labs if l['id'] == sub['lab_id']), None)
            if lab:
                submissions.append({
                    "lab_number": lab['number'],
                    "lab_id": lab['id'],
                    "questions": lab['questions'],
                    "answers": sub['answers']
                })
        all_details.append(
            {"student": student, "course": course, "submissions": submissions})
    return templates.TemplateResponse("std_det.html", {"request": request, "all_details": all_details})
