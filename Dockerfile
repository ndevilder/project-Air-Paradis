# Utilisez une image Python légère
FROM python:3.9-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le code source de l'application
COPY . /app
WORKDIR /app/app

# Exposer le port 80
EXPOSE 80

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
