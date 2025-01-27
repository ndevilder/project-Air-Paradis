from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "powered by" in response.text

def test_predict():
    response = client.post("/predict", data={"text": "Test de prédiction"})
    assert response.status_code == 200
    assert "positive" in response.text or "negative" in response.text
    