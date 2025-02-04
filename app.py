import streamlit as st
import requests
from bs4 import BeautifulSoup  # Pour extraire les données HTML si nécessaire

# URL de ton API FastAPI
API_URL = "http://13.53.129.120/predict"

# Titre de l'application
st.title("Tweet sentiment prediction")

# Champ de saisie pour entrer un texte
user_input = st.text_area("Enter your text and click on the predict button", "")

# Bouton pour soumettre le texte
if st.button("🔍 Predict"):
    if user_input.strip() != "":
        # Envoyer la requête à l'API
        response = requests.post(API_URL, data={"text": user_input})

        if response.status_code == 200:
            # Parser la réponse HTML pour extraire la prédiction
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraire la prédiction (ici basée sur le format de ton HTML)
            prediction = soup.find("p", class_="prediction")  # Cherche le <p> contenant la prédiction
            prediction_text = prediction.get_text().replace("Prediction:", "").strip() if prediction else "Non trouvé"

            # Afficher le résultat proprement
            st.subheader("Prediction Result :")
            st.write(f" **Prediction: ** {prediction_text}")

            # Boutons de feedback
            st.write("📢 **please give us a feedback**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Correct"):
                    requests.post("http://13.53.129.120/feedback", data={"correct": "1"})
                    st.success("Merci pour votre feedback !")
            with col2:
                if st.button("❌ Incorrect"):
                    requests.post("http://13.53.129.120/feedback", data={"correct": "0"})
                    st.warning("Merci, votre retour a été pris en compte !")

        else:
            st.error("❌ Erreur : Impossible de contacter l'API.")
    else:
        st.warning("⚠️ The submitted text is empty. Please enter valid text..")
