# Utiliser une image Python légère
FROM python:3.9-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt et installer les dépendances
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier tout le code source dans le répertoire /app
COPY app /app/app
WORKDIR /app/app

# Exposer le port
EXPOSE 80

# Démarrer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
