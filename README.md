# 📢 Application d'Analyse de Sentiment

## 📝 Description
Cette application permet d'analyser le sentiment des tweets en utilisant un modèle **DistilBERT**. L'API est développée avec **FastAPI** et est déployée sur un serveur cloud. L'interface utilisateur est construite avec **Streamlit** pour envoyer des tweets à l'API et récupérer les prédictions de sentiment.

---

## 🚀 Fonctionnalités
- 📡 **API FastAPI** qui expose un endpoint `/predict` pour l'analyse de sentiment.
- 💡 **Interface utilisateur Streamlit** pour une utilisation intuitive.
- 🌐 **Interface Web pour tester directement l'API via [le serveur](http://13.53.129.120/)** 
- 📊 **Système de feedback** permettant d'améliorer les prédictions du modèle.
- 🛠️ **Déployé sur EC2 (AWS)** et **conteneurisé avec Docker**.

---

## 📌 Prérequis
Avant de commencer, assure-toi d'avoir installé :

- **Python 3.9+**
- **pip** (gestionnaire de paquets Python)

---

## ⚙️ Installation et Exécution

###  **Cloner le projet**
```sh
  cd ton-repo
  git clone https://github.com/ndevilder/project-Air-Paradis.git .
  cd project-Air-Paradis
```
### **Installer les dépendances**
```sh
  pip install -r requirements.txt
```
### **Lancer l'interface streamlit**
```sh 
      streamlit run app.py
```      
---
## 📂 Structure du projet
```sh 
project-Air-Paradis/
│── app/
│   ├── main.py                         # API FastAPI
│   ├── templates/                      # Fichiers HTML pour l'API
│   ├── static/                         # CSS pour l'interface
│   ├── saved_models/                   # Modèle entraîné
│   │   ├── final_distimbert_model/         
│   │   ├── final_distimbert_model_parts/  # fichier du model necessitant une partition pour etre uploadé sur github 
│   │── tests/                          # Tests unitaires avec pytest
│── notebooks/                          # notebooks utilisés lors de la conception, utiles pour le projet mais pas pour l api
│── Dockerfile                          # Fichier Docker pour la conteneurisation
│── requirements.txt                    # Liste des dépendances
│── app.py                              # Interface Streamlit
│── README.md                           # Documentation du projet
```
---
## 🛠️ Améliorations futures

- 📊 **Dashboard analytique**  
  - Visualisation des tendances des sentiments  
  - sauvegarde des tweet, de la prediction et du feedback pour un réentrainement futur  

- 🌎 **Détection de langue**  
  - Prise en charge multilingue avant l'analyse de sentiment  
  - Traduction automatique des tweets avant l'envoi au modèle  

- 🔗 **Amélioration de l'API**  
  - Optimisation des performances et réduction du temps de réponse  
  - Ajout de nouvelles fonctionnalités comme l'analyse de plusieurs tweets en batch  

- 🎨 **Amélioration de l'interface Streamlit**  
  - Personnalisation du design et meilleure UX  
---
## 📚 Ressources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- image docker hebergée sur docker hub ![Docker Pulls](https://img.shields.io/docker/pulls/dralakh/airparadis)
-  pipeline CI/CD via git hub actions ![CI/CD](https://github.com/ndevilder/project-Air-Paradis/actions/workflows/deploy.yml/badge.svg)

---

## 📝 Auteur
👤 **[Nicolas De vilder](https://github.com/ndevilder)** 
---