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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/student_portal", response_class=HTMLResponse)
async def std_portal(request: Request):
    return templates.TemplateResponse("std_portal.html", {"request": request})


@app.get("/teacher_portal", response_class=HTMLResponse)
async def t_course(request: Request):
    return templates.TemplateResponse("teacher_portal.html", {"request": request})


@app.get("/course/{course_code}", response_class=HTMLResponse)
async def course_labs(course_code, request: Request):
    return templates.TemplateResponse("course_labs.html", {"request": request})


@app.get("/course/{course_code}/lab/{lab_id}", response_class=HTMLResponse)
async def lab_task(course_code, lab_id, request: Request):
    return templates.TemplateResponse("lab_task.html", {"request": request})


@app.get("/course", response_class=HTMLResponse)
async def course(request: Request):
    return templates.TemplateResponse("teacher_course.html", {"request": request})


@app.get("/teacher/{course_code}", response_class=HTMLResponse)
async def teacher_options(request: Request):
    return templates.TemplateResponse("t_opt.html", {"request": request})


@app.get("/teacher/{course_code}/students")
async def teacher_students(course_code, request: Request):
    return templates.TemplateResponse("std_list.html", {"request": request})


@app.get("/teacher/{course_code}/labs")
async def teacher_labs(course_code, request: Request):
    return templates.TemplateResponse("t_lab.html", {"request": request})


@app.get("/teacher/checking/{course_code}/{lab_no}")
async def teacher_checking(course_code, lab_no, request: Request):
    return templates.TemplateResponse("lab_checking.html", {"request": request})


@app.get("/teacher/checking/student/{course_code}/{student_id}")
async def teacher_student(course_code, student_id, request: Request):
    return templates.TemplateResponse("t_std.html", {"request": request})


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
