from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
import torch
from datetime import datetime, timedelta
from collections import deque
import yaml
import boto3

# Charger la configuration depuis config.yaml
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        if not config:
            raise ValueError("Le fichier config.yaml est vide ou invalide.")
except FileNotFoundError:
    raise FileNotFoundError("Le fichier de configuration 'config.yaml' est introuvable.")
except Exception as e:
    raise ValueError(f"Erreur lors du chargement de config.yaml : {e}")

# Initialiser FastAPI
app = FastAPI()

# Configurer les templates et les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Paramètres globaux pour le feedback négatif
NEGATIVE_FEEDBACK_LIMIT = config["negative_feedback_limit"]
NEGATIVE_FEEDBACK_WINDOW = timedelta(minutes=config["negative_feedback_window_minutes"])
negative_feedback_times = deque()

# Initialisation AWS CloudWatch
USE_AWS = config.get("use_aws", True)
if USE_AWS:
    cloudwatch_client = boto3.client("cloudwatch", region_name=config.get("aws_region", "eu-north-1"))

# Fonction pour publier une métrique dans CloudWatch
def publish_to_cloudwatch(metric_name, value, namespace):
    """
    Publie une métrique personnalisée dans Amazon CloudWatch.
    """
    try:
        response = cloudwatch_client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Timestamp": datetime.utcnow(),
                    "Value": value,
                    "Unit": "Count",
                }
            ],
        )
        print(f"Métrique {metric_name} publiée avec succès : {value}")
        print(f"Réponse CloudWatch : {response}")
        return response
    except Exception as e:
        print(f"Erreur lors de l'envoi de la métrique à CloudWatch : {e}")


# Fonction pour gérer les feedbacks négatifs
def handle_negative_feedback():
    """
    Gère les retours négatifs, publie les métriques et déclenche des alertes si nécessaire.
    """
    global negative_feedback_times

    now = datetime.utcnow()
    negative_feedback_times.append(now)

    # Nettoyer les anciens feedbacks
    while negative_feedback_times and now - negative_feedback_times[0] > NEGATIVE_FEEDBACK_WINDOW:
        negative_feedback_times.popleft()

    # Publier les métriques dans CloudWatch
    if USE_AWS:
        publish_to_cloudwatch(
            metric_name=config.get("cloudwatch_metric_name", "NegativeFeedbackCount"),
            value=len(negative_feedback_times),
            namespace=config.get("cloudwatch_namespace", "MyApp/Feedback"),
        )

    # Si le seuil est atteint, loguer ou effectuer d'autres actions
    if len(negative_feedback_times) >= NEGATIVE_FEEDBACK_LIMIT:
        print("Seuil de feedback négatif atteint.")
        negative_feedback_times.clear()

# Charger le modèle et le tokenizer
model_dir = config["model_dir"]

try:
    tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
    model = DistilBertForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    print("Modèle et tokenizer chargés avec succès.")
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle ou du tokenizer : {e}")

# Fonction de prédiction
def predict_text(text):
    """
    Effectue une prédiction sur un texte donné.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]
        prediction = torch.argmax(outputs.logits, dim=1).item()
        prediction_label = "positive" if prediction == 1 else "negative"
        return prediction_label, probabilities

# Route principale
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Page d'accueil de l'application.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Route pour effectuer une prédiction
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, text: str = Form(...)):
    """
    Effectue une prédiction sur le texte soumis par l'utilisateur.
    """
    try:
        # Vérifier si le texte est vide
        if not text.strip():
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error_message": "Le texte soumis est vide. Veuillez saisir un texte valide.",
                },
            )
        
        prediction, probabilities = predict_text(text)
        return templates.TemplateResponse(
            "prediction.html",
            {
                "request": request,
                "text": text,
                "prediction": prediction,
                "probabilities": probabilities.tolist(),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")


# Route pour gérer les feedbacks utilisateurs
@app.post("/feedback", response_class=HTMLResponse)
async def feedback(request: Request, correct: int = Form(...)):
    """
    Reçoit le feedback de l'utilisateur.
    """
    if correct == 0:
        handle_negative_feedback()
    return templates.TemplateResponse("feedback.html", {"request": request})
