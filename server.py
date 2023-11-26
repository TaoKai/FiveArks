from fastapi import FastAPI, Request, Form, Depends, Response, HTTPException
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import threading, queue, uvicorn, json, time
import os, sys
import mysql.connector

base_path = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="chenli123456")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/htmls", StaticFiles(directory="htmls"), name="htmls")
templates = Jinja2Templates(directory="htmls")
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TaoKai123456",
    database="fivearks"
)

@app.get("/")
async def index(request: Request):
    email = "not login"
    user = request.session.get("user")
    if user:
        email = user
        return templates.TemplateResponse("user.html", {"request": request, "user": email})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "user": email})

#@app.get("/")
#async def get_sign_up_html(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request, "image":"/static/images/1.png"})

@app.post("/login")
async def signin(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(email, "login")
    query = "SELECT password from users where email=%s"
    cursor = cnx.cursor()
    cursor.execute(query, (email,))
    res = cursor.fetchone()[0]
    if password==res:
        request.session["user"] = email
        return templates.TemplateResponse("user.html", {"request": request, "user": email})
    else: 
        return templates.TemplateResponse("signin.html", {"request": request, "hint":"incorrect username or password"})

@app.get("/signin")
async def signinhref(request: Request):
    hint = ""
    return templates.TemplateResponse("signin.html", {"request": request, "hint":hint})

@app.get("/signup")
async def signuphref(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "err_msg": ""})

@app.post("/signup_form")
async def sign_up(request: Request, informations: Annotated[str, Form()]):
    infos = informations.strip().split("|")
    for i, info in enumerate(infos):
        if info.strip()=="":
            infos[i] = "NULL"
    dic = {
        "request": request, 
        "first_name": infos[0],
        "last_name": infos[1],
        "email": infos[2],
        "password": infos[3],
        "profession": infos[4],
        "recruit1": infos[5],
        "recruit2": infos[6],
        "recruit3": infos[7],
    }
    query = "SELECT id from users where email=%s"
    cursor = cnx.cursor()
    cursor.execute(query, (dic["email"],))
    res = cursor.fetchone()
    if res is not None and len(res)>0:
        return templates.TemplateResponse("signup.html", {"request": request, "err_msg": "Your email has been registered."})
    else:
        query = "INSERT INTO users (first_name, last_name, email, password, profession, recruit1, recruit2, recruit3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (dic["first_name"], dic["last_name"], dic["email"], dic["password"], dic["profession"], dic["recruit1"], dic["recruit2"], dic["recruit3"])
        cursor.execute(query, values)
        cnx.commit()
        return templates.TemplateResponse("signupdone.html", dic)

@app.get("/signin", response_class=HTMLResponse)
async def signin(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})

@app.get("/get_user_profile", response_class=HTMLResponse)
async def get_user_profile(request: Request):
    email = request.session.get("user")
    if email:
        query = "SELECT * from users where email=%s"
        cursor = cnx.cursor()
        cursor.execute(query, (email,))
        _, first_name, last_name, _, _,  profession, recruit1, recruit2, recruit3= cursor.fetchone()
        dic = {
            "request": request, 
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "profession": profession,
            "recruit1": recruit1,
            "recruit2": recruit2,
            "recruit3": recruit3,
        }
        return templates.TemplateResponse("user_profile.html", dic)
    else:
        return "Session is off, cannot get user informations."

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    del request.session["user"]
    return RedirectResponse("/")

if __name__=="__main__":
    uvicorn.run(app, host='0.0.0.0', port=80, workers=1)