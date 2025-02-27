from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_empty_text():
    response = client.post("/predict", data={"text": ""})
    assert response.status_code == 200
    assert "The submitted text is empty." in response.text

def test_predict_spaces_only():
    response = client.post("/predict", data={"text": "   "})
    assert response.status_code == 200
    assert "The submitted text is empty." in response.text
