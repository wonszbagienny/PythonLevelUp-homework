from hashlib import sha256
from fastapi import FastAPI, HTTPException, Response, Cookie, Request, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from typing import Dict
from pydantic import BaseModel
import secrets

app = FastAPI()

###########################
# second part [homework 3]

app.secret_key = "very constant and random secret, best 64 characters"
app.num = 0
app.count = -1
app.tokens = []

template = Jinja2Templates(directory = "templates")

security = HTTPBasic()

@app.post("/login")
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    session_token = sha256(bytes(f"{credentials.usename}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    response.set_cookie(key = "session_token", value = session_token)
    app.tokens.append(session_token)
    response.status_code = 307
    response.headers['Location'] = "/welcome"
    RedirectResponse(url = '/welcome')
    return response

@app.get("/welcome")
def welcome(request: Request, session_token = Cookie(None)):
    if session_token not in app.tokens:
        raise HTTPException(status_code = 401, detail = "Access denied")
    return template.TemplateResponse("second.html", {"request": request, "user": "trudnY"})
    #return {"message": "finally someone let me out of my cage"}
        
    

###########################
# first part [homework 1]

app.no_of_patients = 0
app.patients = []

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def method_get():
    return {"method": "GET"}

@app.post("/method")
def method_post():
    return {"method": "POST"}

@app.put("/method")
def method_put():
    return {"method": "PUT"}

@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}

class GiveMeSomethingRq(BaseModel):
    name: str
    surname: str

class GiveMeSomethingResp(BaseModel):
    id: int = app.no_of_patients
    patient: Dict

@app.post("/patient", response_model=GiveMeSomethingResp)
def post_patient(rq: GiveMeSomethingRq):
    returnID = app.no_of_patients
    app.patients.append(rq.dict())
    app.no_of_patients += 1
    return GiveMeSomethingResp(id=returnID, patient=rq.dict())

@app.get("/number_of_patients")
def get_number():
    return str(app.no_of_patients)

@app.get("/patient/{pk}")
def get_patient(pk: int):
    if (len(app.patients) > pk and pk >= 0):
        return app.patients[pk]
    else:
        raise HTTPException(status_code = 204, detail = "patient_not_found")

