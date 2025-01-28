#!/bin/sh

# Vérifier si on a demandé de lancer les tests ou le serveur
if [ "$1" = "test" ]; then
    pytest --cov=. --cov-report=xml --disable-warnings
else
    uvicorn main:app --host 0.0.0.0 --port 80
fi
