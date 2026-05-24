import streamlit as st
import pandas as pd
from groq import Groq

# Configuration de la page premium
st.set_page_config(page_title="PredictiveStock AI + Groq", page_icon="📈", layout="wide")

# Initialisation du client Groq (Remplacez par votre clé ou utilisez les variables d'environnement)
# Idéalement, utilisez st.secrets["GROQ_API_KEY"] en production
GROQ_API_KEY = "VOTRE_CLE_API_GROQ" 

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    client = None

st.title("📈 PredictiveStock AI — Propulsé par Groq")
st.subheader("Analyse prédictive et conseils d'achat générés par IA")

# 1. Base de données fictive de la boutique de luxe
data = {
    'Modele': ['Rolex Submariner', 'Audemars Piguet Royal Oak', 'Patek Philippe Nautilus'],
    'Stock_Actuel': [2, 0, 1],
    'Ventes_Mois_Dernier': [5, 2, 1],
    'Tendances_Reseaux_Sociaux': [
        "Hausse de 30% des recherches sur Chrono24, forte traction sur TikTok auprès des 25-35 ans.",
        "Rupture mondiale confirmée, prix du marché gris en hausse de 12% cette semaine.",
        "Volume de recherche stable, mais intérêt accru de la part des clients VIP locaux."
    ]
}
df = pd.DataFrame(data)

st.markdown("### 📊 État actuel des stocks et du marché")
st.dataframe(df)

# 2. Fonction pour appeler Groq et obtenir une analyse intelligente
def generer_conseil_ia(modele, stock, ventes, tendances):
    if not client or GROQ_API_KEY == "VOTRE_CLE_API_GROQ":
        return "⚠️ Veuillez configurer votre clé API Groq pour activer les conseils IA."
    
    # Prompt ultra-précis pour forcer l'IA à agir comme un consultant expert en retail de luxe
    prompt = f"""
    Tu es un consultant expert en gestion des stocks pour des boutiques de montres de luxe. 
    Analyse la situation suivante et donne une recommandation d'achat TRÈS courte (maximum 3 phrases), incisive et orientée business.
    
    - Modèle de montre : {modele}
    - Stock actuel en boutique : {stock} unités
    - Ventes le mois dernier : {ventes} unités
    - Tendances actuelles du marché : {tendances}
    
    Dis clairement si le gérant doit recommander du stock, combien d'unités, et pourquoi par rapport à la tendance. Sois direct.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tu es un expert business en horlogerie de luxe. Tu parles de manière professionnelle, concise et directe."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192", # Modèle ultra-rapide et économique de Groq
            temperature=0.2, # Basse température pour éviter que l'IA n'invente des faits
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de l'appel à Groq : {str(e)}"

# 3. Interface de génération des conseils IA
st.markdown("---")
st.markdown("### 🤖 Consultant IA Premium (Valeur ajoutée à 500$/mois)")

selected_watch = st.selectbox("Sélectionnez une montre pour obtenir l'analyse stratégique de l'IA :", df['Modele'].unique())

if st.button("Générer l'analyse Groq"):
    # Récupération des données de la montre sélectionnée
    row = df[df['Modele'] == selected_watch].iloc[0]
    
    with st.spinner("Groq analyse le marché en temps réel..."):
        conseil = generer_conseil_ia(
            row['Modele'], 
            row['Stock_Actuel'], 
            row['Ventes_Mois_Dernier'], 
            row['Tendances_Reseaux_Sociaux']
        )
        
    # Affichage du résultat dans un encadré premium
    st.info(f"**Recommandation de l'IA pour le modèle {selected_watch} :**\n\n{conseil}")
