FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY app /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Install test dependencies
RUN pip install pytest pytest-cov
RUN pip install safetensors

# Copier et exécuter le script de reconstruction du modèle
COPY app/rebuild_model.py /app/rebuild_model.py
RUN python /app/rebuild_model.py

# Expose the port the app runs on
EXPOSE 80

# Copy the entrypoint script
COPY app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
