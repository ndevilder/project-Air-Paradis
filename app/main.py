from fastapi import FastAPI

# Créer l'application FastAPI
app = FastAPI()

# Endpoint racine
@app.get("/")
def read_root():
    return {"message": "Bienvenue dans votre application FastAPI !"}

# Endpoint pour récupérer un message personnalisé
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Bonjour, {name} !"}

# Endpoint pour additionner deux nombres
@app.post("/add/")
def add_numbers(data: dict):
    try:
        num1 = data.get("num1", 0)
        num2 = data.get("num2", 0)
        return {"result": num1 + num2}
    except Exception as e:
        return {"error": str(e)}

# Endpoint pour vérifier que le serveur fonctionne
@app.get("/ping")
def ping():
    return {"status": "OK"}
