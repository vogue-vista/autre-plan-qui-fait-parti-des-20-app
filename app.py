import streamlit as st
import pandas as pd
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="PredictiveStock AI", page_icon="📈", layout="wide")

# -----------------------------------------------------------------------------
# SÉCURITÉ & AUTHENTIFICATION (Simulée pour le Micro-SaaS)
# -----------------------------------------------------------------------------
# En production, remplacez ces valeurs ou connectez une base de données.
USER_DATABASE = {
    "admin": "premium2026",
    "client1": "rolex30",
    "test": "crypto"
}

def check_password():
    """Retourne True si l'utilisateur a entré le bon mot de passe."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Interface de connexion si non connecté
    st.title("🔐 Accès Restreint — PredictiveStock AI")
    st.write("Cette application nécessite un abonnement actif à **30 $/mois**.")
    
    # Intégration visuelle du bouton PayPal
    st.markdown("""
    <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:20px;">
        <h4>Pas encore abonné ?</h4>
        <p>Activez votre accès instantanément pour 30 $/mois :</p>
        <!-- Simulation de bouton PayPal -->
        <a href="https://paypal.com" target="_blank" style="background-color:#0070ba; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">
            🖲️ S'abonner avec PayPal (30$/mois)
        </a>
    </div>
    """, unsafe_url_allowed=True)

    # Formulaire de connexion
    with st.form("Login Form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        
        if submit:
            if username in USER_DATABASE and USER_DATABASE[username] == password:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects ou abonnement expiré.")
    return False

# Si l'utilisateur n'est pas connecté, on arrête l'exécution du script ici
if not check_password():
    st.stop()

# -----------------------------------------------------------------------------
# APPLICATION PRINCIPALE (Accessible uniquement après connexion)
# -----------------------------------------------------------------------------

# Initialisation du client Groq via les Secrets Streamlit
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    client = None
    st.sidebar.warning("⚠️ Clé API Groq manquante dans les Secrets Streamlit.")

# Barre latérale de déconnexion
st.sidebar.success("✅ Connecté avec succès")
if st.sidebar.button("Se déconnecter"):
    st.session_state["authenticated"] = False
    st.rerun()

st.title("📈 Votre Assistant d'Analyse Prédictive")
st.subheader(" Entrez vos propres produits pour analyser la demande")

# Formulaire dynamique pour que l'utilisateur entre N'IMPORTE QUEL type de produit
with st.expander("➕ Étape 1 : Configurer votre produit à analyser", expanded=True):
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        nom_produit = st.text_input("Nom de l'article (ex: Chaussures Nike Dunk, Sac Chanel, Carte Dracaufeu)", "Chaussures Nike Dunk")
        stock_actuel = st.number_input("Quantité actuellement en stock", min_value=0, value=5, step=1)
    with col_input2:
        ventes_dernier_mois = st.number_input("Ventes réalisées le mois dernier", min_value=0, value=12, step=1)
        tendances_observees = st.text_area("Tendances ou signaux observés (ex: Rupture sur le site officiel, influenceur en parle, etc.)", 
                                           "Grosse tendance sur TikTok cette semaine, le modèle est en rupture de stock chez la plupart des grossistes.")

# Création du tableau de bord dynamique à partir des entrées de l'utilisateur
st.markdown("### 📊 Données actuelles du produit")
donnees_utilisateur = pd.DataFrame({
    'Article': [nom_produit],
    'Stock Actuel': [stock_actuel],
    'Ventes (Mois Dernier)': [ventes_dernier_mois]
})
st.dataframe(donnees_utilisateur, use_container_width=True)

# Bouton d'analyse IA avec Groq
st.markdown("---")
st.markdown("### 🤖 Analyse Stratégique par l'IA (Groq)")

def generer_analyse_generique(produit, stock, ventes, tendances):
    if not client:
        return "⚠️ L'analyse ne peut pas être générée car la clé API Groq n'est pas configurée dans les paramètres de votre serveur."
    
    prompt = f"""
    Tu es un consultant expert en gestion des stocks et de la demande pour des commerces de détail et e-commerce.
    Analyse la situation de l'article suivant et donne une recommandation d'achat TRÈS courte (maximum 3 phrases), incisive et orientée profit.
    
    - Article : {produit}
    - Stock actuel en magasin : {stock} unités
    - Ventes le mois dernier : {ventes} unités
    - Signaux de tendance : {tendances}
    
    Indique clairement si le commerçant doit commander plus de stock, en quelle quantité estimée, et le risque s'il ne le fait pas.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tu es un expert business. Tu parles de manière professionnelle, concise et directe en français."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"

if st.button(f"🚀 Lancer l'analyse IA pour : {nom_produit}"):
    with st.spinner("Groq analyse les données entrées..."):
        resultat_ia = generer_analyse_generique(nom_produit, stock_actuel, ventes_dernier_mois, tendances_observees)
    st.info(resultat_ia)
