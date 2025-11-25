# test
import streamlit as st
import os
from google import genai 

# --- 1. LE SYSTEM PROMPT (Ton ADN) ---
SYSTEM_PROMPT = """
Tu es le Mentor Miroir. Ton rôle est d'être un coach de vie pragmatique et intuitif, basé sur l'expérience. Ton ton est profondément bienveillant mais ta franchise est radicale. Structure toujours ta réponse en 3 parties claires : Validation, Vérité Inconfortable, et Question-Action. Règle absolue : Ne jamais accepter les excuses qui reposent sur le confort ou la peur. Toujours ramener à la responsabilité personnelle. Ton analyse doit toujours se terminer par une question pragmatique qui force l'utilisateur à se confronter à la réalité.
"""

# Configuration de l'interface Streamlit
st.set_page_config(page_title="Le Mentor Miroir : La Vérité, Rien que la Vérité.", layout="wide")
st.title("💡 Le Mentor Miroir : La Vérité, Rien que la Vérité.")
st.caption("Raconte-moi ton blocage et je te dirai ce que tu te caches.")

# --- Vérification et Initialisation (Code Final Simplifié) ---
try:
    # Tente de lire directement le secret, comme un dictionnaire
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

except KeyError:
    st.error("FATAL : La clé 'GEMINI_API_KEY' n'est pas accessible. Réessayez de la supprimer et de la sauvegarder dans les Secrets de Streamlit (le format TOML).")
    st.stop()

# Le reste du code d'initialisation (client, model) reste le même...
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = 'gemini-2.5-pro' 
except Exception as e:
    st.error(f"Erreur d'initialisation de l'API : {e}")
    st.stop()

# --- Fonction d'Analyse Réelle ---
def mentor_analyse_real(user_input):
    full_prompt = f"{SYSTEM_PROMPT}\n\nL'utilisateur dit : {user_input}"
    try:
        response = client.models.generate_content(
            model=model,
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"Désolé, une erreur est survenue lors de l'analyse : {e}"


# Zone de saisie pour l'utilisateur
user_input = st.text_area("Racontez-moi votre situation (anonymement) :", height=200)

if st.button("Obtenir sa Vérité"):
    if not user_input:
        st.error("Veuillez décrire votre situation.")
    else:
        with st.spinner("Le Mentor Miroir est en pleine introspection pour vous..."):
            response_text = mentor_analyse_real(user_input)
            st.subheader("🔮 Votre Vérité Révélée")
            st.markdown(response_text)
            
            st.markdown("---")

            st.info("Cette analyse vous a secoué ? Si vous êtes prêt(e) à prendre une heure pour un échange humain et sans filtre, réservez une session (Lien vers ton service).")

