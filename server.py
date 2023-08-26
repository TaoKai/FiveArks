from fastapi import FastAPI, Request, Form
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import threading, queue, uvicorn, json, time
import os, sys
#scp ChenLi.tar root@34.95.204.226:/root/workspace
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
    information_list = informations.split('|')
    recruit1 = information_list[4] if len(information_list) > 4 else ""
    recruit2 = information_list[5] if len(information_list) > 5 else ""
    recruit3 = information_list[6] if len(information_list) > 6 else ""
    
    dic = {
        "request": request,
        "recruit1": recruit1,
        "recruit2": recruit2,
        "recruit3": recruit3,
    }
    return templates.TemplateResponse("question2345.html", dic)

@app.post("/answer_q2345")
async def answer_q2345(request: Request, value: Annotated[str, Form()]):
    information_list = value.split('|')
    college1 = information_list[7] if len(information_list) > 7 else ""
    college2 = information_list[8] if len(information_list) > 8 else ""
    college3 = information_list[9] if len(information_list) > 9 else ""
    industry1 = information_list[10] if len(information_list) > 10 else ""
    industry2 = information_list[11] if len(information_list) > 11 else ""
    industry3 = information_list[12] if len(information_list) > 12 else ""

    dic = {
        "request": request,
        "college1": college1,
        "college2": college2,
        "college3": college3,
        "industry1": industry1,
        "industry2": industry2,
        "industry3": industry3,
    }
    return templates.TemplateResponse("temp.html", dic)

if __name__=="__main__":
    uvicorn.run(app, host='0.0.0.0', port=80, workers=1)
