from fastapi import FastAPI, HTTPException
from typing import Dict
from pydantic import BaseModel

app = FastAPI()
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
