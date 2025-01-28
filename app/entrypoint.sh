#!/bin/sh

# Vérifier si on exécute les tests
if [ "$1" = "test" ]; then
    echo "🧪 Reconstruction du modèle pour les tests..."
    cat /app/saved_models/final_distilbert_model_parts/part_* > /app/saved_models/final_distilbert_model/model.safetensors

    echo "🧪 Exécution des tests..."
    pytest --cov=. --cov-report=xml --disable-warnings
    exit 0
fi

# Par défaut, reconstruire le modèle et démarrer le serveur
echo "🔧 Reconstruction du modèle avant le lancement..."
cat /app/saved_models/final_distilbert_model_parts/part_* > /app/saved_models/final_distilbert_model/model.safetensors

echo "🚀 Démarrage du serveur FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 80
