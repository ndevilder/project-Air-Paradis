from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import DistilBertTokenizer
from transformers import DistilBertForSequenceClassification
import torch
import os
from datetime import datetime, timedelta
from collections import deque
import yaml
import boto3

# Load configuration from config.yaml
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        if not config:
            raise ValueError("The config.yaml file is empty or invalid.")
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config.yaml' is not found.")
except Exception as e:
    raise ValueError(f"Error loading config.yaml: {e}")

# Initialize FastAPI
app = FastAPI()

# Configure templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Global parameters for negative feedback
NEGATIVE_FEEDBACK_LIMIT = config["negative_feedback_limit"]
NEGATIVE_FEEDBACK_WINDOW = timedelta(minutes=config["negative_feedback_window_minutes"])
negative_feedback_times = deque()

# Initialize AWS CloudWatch
USE_AWS = config.get("use_aws", True)
if USE_AWS:
    cloudwatch_client = boto3.client("cloudwatch", region_name="eu-north-1")

def publish_to_cloudwatch(metric_name, value, namespace="MyApp/Feedback"):
    """
    Publishes a custom metric to Amazon CloudWatch.
    """
    try:
        response = cloudwatch_client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Value": value,
                }
            ],
        )
        print(f"Metric {metric_name} published: {value}")
        return response
    except Exception as e:
        print(f"Error publishing to CloudWatch: {e}")

# Function to handle negative feedback
def handle_negative_feedback():
    """
    Handles negative feedback and publishes a metric to CloudWatch.
    """
    if USE_AWS:
        publish_to_cloudwatch(
            metric_name="NegativeFeedbackCount",
            value=1,  # Each negative feedback increments by 1
        )
    print("Negative feedback recorded and metric published.")

# Prediction function
def predict_text(text):
    """
    Makes a prediction on a given text.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]
        prediction = torch.argmax(outputs.logits, dim=1).item()
        prediction_label = "positive" if prediction == 1 else "negative"
        return prediction_label, probabilities

# Main route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page of the application.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Route to make a prediction
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, text: str = Form(...)):
    """
    Makes a prediction on the text submitted by the user.
    """
    try:
        # Check if the text is empty or consists only of spaces
        if not text or not text.strip() or len(text) == 0:
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error_message": "The submitted text is empty. Please enter valid text.",
                },
            )
        
        # Make the prediction
        prediction, probabilities = predict_text(text)
        return templates.TemplateResponse(
            "prediction.html",
            {
                "request": request,
                "length": len(text),
                "text": text,
                "prediction": prediction,
                "probabilities": probabilities.tolist(),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")

# Route to handle user feedback
@app.post("/feedback", response_class=HTMLResponse)
async def feedback(request: Request, correct: int = Form(...)):
    """
    Receives user feedback.
    """
    if correct == 0:
        handle_negative_feedback()
    return templates.TemplateResponse("feedback.html", {"request": request})
