# Utiliser une image de base légère
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers nécessaires pour l'installation
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /app

# Exposer le port utilisé par l'application
EXPOSE 80

# Copy the entrypoint script
COPY app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
