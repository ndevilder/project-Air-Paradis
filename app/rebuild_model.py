import os
from safetensors.torch import load_file, save_file

# Dossiers contenant les morceaux du modèle
MODEL_PARTS_DIR = "saved_models/final_distilbert_model_parts"
FINAL_MODEL_DIR = "saved_models/final_distilbert_model"
FINAL_MODEL_PATH = os.path.join(FINAL_MODEL_DIR, "model.safetensors")

def rebuild_model():
    """Reconstitue le modèle en fusionnant les fichiers part_*"""
    if not os.path.exists(FINAL_MODEL_DIR):
        os.makedirs(FINAL_MODEL_DIR)

    if os.path.exists(FINAL_MODEL_PATH):
        print("✅ Le modèle est déjà reconstruit.")
        return

    print("🔧 Reconstruction du modèle à partir des morceaux...")
    tensor_data = {}

    # Trier et fusionner les fichiers
    for part in sorted(os.listdir(MODEL_PARTS_DIR)):  # Trier pour assurer le bon ordre
        part_path = os.path.join(MODEL_PARTS_DIR, part)
        part_data = load_file(part_path)
        tensor_data.update(part_data)

    # Sauvegarder le modèle fusionné
    save_file(tensor_data, FINAL_MODEL_PATH)
    print(f"✅ Modèle reconstruit avec succès : {FINAL_MODEL_PATH}")

if __name__ == "__main__":
    rebuild_model()
