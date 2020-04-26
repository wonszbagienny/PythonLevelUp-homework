from hashlib import sha256
from fastapi import FastAPI, HTTPException, Response, Cookie
from typing import Dict
from pydantic import BaseModel

app = FastAPI()

###########################
# second part [homework 3]

app.secret_key = "very constant and random secret, best 64 characters"
app.num = 0
app.count = -1
app.users = {"trudnY": "PaC13Nt"}
app.secret = "secret"
app.tokens = []

@app.post("/login")
def login(credentials, response: Response):
    if credentials.username in app.users and credentials.password == app.users[credentials.username]:
        session_token = sha256(bytes(f"{user}{password}{app.secret_key}")).hexdigest()
        response.set_cookie(key="session_token", value=session_token)
        app.tokens.append(session_token)
        #response.status_code = 307
        #response.headers['Location'] = "/welcome"
        return response = RedirectResponse(url='/welcome')
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/welcome")
def welcome():
    if s_token in app.tokens:
		return template.TemplateResponse("template1.html", {"request": request, "user": "trudnY" }
    else:
        raise HTTPException(status_code=401, detail="dostęp wzbroniony")
    return {"message": "finally someone let me out of my cage"}

@app.post("/login")

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
    surename: str

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

