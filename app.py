import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="PredictiveStock IA Pro", page_icon="📈", layout="wide")

# Masquer la sidebar par défaut pour un look épuré (votre style d'origine)
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL (À REMPLIR PLUS TARD)
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  # Mettez votre Client ID ici plus tard
PAYPAL_PLAN_ID = "DEMO"    # Mettez votre Plan ID ici plus tard

# -------------------------
# GESTION DE L'ACCÈS (SESSION STATE)
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("📈 PredictiveStock IA — Version Pro")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 50 $/mois")
        st.write("Optimisez vos stocks, évitez les ruptures et anticipez la demande du marché (montres, vêtements, sneakers, etc.).")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        st.write("Connectez-vous pour activer vos accès.")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access50":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects ou abonnement PayPal inactif.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLET
else:
    st.write("✨ **Bienvenue dans votre espace Premium.** Votre analyseur prédictif est prêt.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_input, col_metriques = st.columns(2)
        
        with col_input:
            produit = st.text_input("Nom ou type du produit à analyser", 
                                    placeholder="Ex: Rolex Submariner 126610LN, Sneakers Jordan 4 Black Cat...")
            tendances = st.text_area("Signaux & tendances du marché", 
                                     placeholder="Ex: Rupture globale sur le site officiel, +40% de hype sur TikTok, prix en hausse sur le marché secondaire...")
            
        with col_metriques:
            stock_actuel = st.number_input("Quantité actuelle en stock", min_value=0, value=2, step=1)
            ventes_dernier_mois = st.number_input("Unités vendues le mois dernier", min_value=0, value=5, step=1)

        generer = st.button("🚀 Lancer l'Analyse Prédictive Pro", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets du serveur.")
        elif not produit:
            st.error("⚠️ Veuillez indiquer le nom du produit à analyser.")
        else:
            with st.spinner("L'IA de Groq analyse l'état du marché et de vos stocks..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un expert mondial en Business Intelligence et gestion de stock pour détaillants haut de gamme.
                    Tu dois obligatoirement formater ta réponse sous forme de tableau Markdown avec exactement 3 colonnes :
                    1. **Indicateur Stratégique** (ex: Demande estimée, Niveau de risque, Recommandation d'achat)
                    2. **Analyse & Données** (Ton évaluation claire)
                    3. **Plan d'Action Immédiat** (Ce que le gérant doit faire)
                    Ne fais aucune intro ou conclusion."""

                    prompt_utilisateur = f"""
                    Produit à analyser : '{produit}'
                    Stock actuel : {stock_actuel} unités
                    Ventes mois dernier : {ventes_dernier_mois} unités
                    Signaux du marché : {tendances}
                    """

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.4
                    )
                    
                    # Correspond exactement à votre structure corrigée
                    script_genere = reponse.choices[0].message.content
                    st.success("✨ L'analyse de vos stocks est prête !")
                    st.markdown(script_genere)
                    st.text_area("Copier le rapport brut :", value=script_genere, height=200)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
