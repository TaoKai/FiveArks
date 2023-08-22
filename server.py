from fastapi import FastAPI, Request, Form
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import threading, queue, uvicorn, json, time
import os, sys
import pymysql
#scp ChenLi.tar root@34.95.204.226:/root/workspace 35.202.98.116
base_path = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/htmls", StaticFiles(directory="htmls"), name="htmls")
templates = Jinja2Templates(directory="htmls")
@app.get("/")
async def get_sign_up_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "image":"/static/images/1.png"})

@app.post("/sign_up")
async def sign_up(request: Request, first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], email: Annotated[str, Form()], profession: Annotated[str, Form()]):
    dic = {
        "request": request,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "profession": profession,
    }
    return templates.TemplateResponse("question1.html", dic)

@app.post("/answer_q1")
async def answer_q1(request: Request, informations: Annotated[str, Form()]):
    return templates.TemplateResponse("temp.html", {"request": request, "informations_q1": informations})

if __name__=="__main__":
    uvicorn.run(app, host='0.0.0.0', port=80, workers=1)