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

# Reconstituer le fichier avant le démarrage de l'app
RUN cat /app/saved_models/final_distilbert_model_parts/part_* > /app/saved_models/final_distilbert_model/model.safetensors

# Expose the port the app runs on
EXPOSE 80

# Copy the entrypoint script
COPY app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
