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
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#@app.get("/")
#async def get_sign_up_html(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request, "image":"/static/images/1.png"})

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup_form")
async def sign_up(request: Request, informations: Annotated[str, Form()]):
   infos = informations.split("|")
#    ["first_name","last_name","email","profession","recruit1","recruit2","recruit3"]
   dic = {
       "request": request, 
       "first_name": infos[0],
       "last_name": infos[1],
       "email": infos[2],
       "profession": infos[3],
       "recruit1": infos[4],
       "recruit2": infos[5],
       "recruit3": infos[6],
   }
   return templates.TemplateResponse("temp.html", dic)

@app.get("/signin", response_class=HTMLResponse)
async def signin(request: Request):
    return templates.TemplateResponse("temp.html", {"request": request})



#@app.post("/answer_q1")
#async def answer_q1(request: Request, informations: Annotated[str, Form()]):
#    information_list = informations.split('|')
#    recruit1 = information_list[4] if len(information_list) > 4 else ""
#    recruit2 = information_list[5] if len(information_list) > 5 else ""
#    recruit3 = information_list[6] if len(information_list) > 6 else ""
#   
#    dic = {
#        "request": request,
#        "recruit1": recruit1,
#        "recruit2": recruit2,
#        "recruit3": recruit3,
#    }
#    return templates.TemplateResponse("temp.html", dic)

if __name__=="__main__":
    uvicorn.run(app, host='0.0.0.0', port=80, workers=1)