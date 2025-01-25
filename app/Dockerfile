# Utiliser une image Python légère
FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y git

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 80 pour l'application
EXPOSE 80

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
