from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", data={"text": "This is a test text."})
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probabilities" in response.json()

def test_feedback():
    response = client.post("/feedback", data={"correct": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback received"}
