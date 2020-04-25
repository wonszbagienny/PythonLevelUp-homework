from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}

def test_receive_patient():
    response = client.post("/patient", json={'name': 'Mateusz', 'surename': 'Kubiszewski'})
    assert response.json() == {"id": app.patients, "patient": {'name': 'Mateusz', 'surename': 'Kubiszewski'}}