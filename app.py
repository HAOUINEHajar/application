import streamlit as st
import hashlib
import pandas as pd
import matplotlib.pyplot as plt

# --- Fonction d'authentification ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = {
    "admin": hash_password("1234"),
    "khalid": hash_password("pass2025"),
}

def check_login(username, password):
    return username in users and users[username] == hash_password(password)

# --- Authentification ---
st.set_page_config(page_title="App sécurisée", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    st.title("🔐 Connexion")
    with st.form("login"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.form_submit_button("Se connecter"):
            if check_login(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Identifiants incorrects.")
else:
    # --- Menu latéral après connexion ---
    st.sidebar.success(f"Connecté en tant que : {st.session_state.username}")
    page = st.sidebar.radio("Menu", ["🏠 Accueil", "📊 Dashboard", "📈 Visualisation", "⚙️ Paramètres", "🔓 Se déconnecter"])

    if page == "🔓 Se déconnecter":
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    elif page == "🏠 Accueil":
        st.title("🏠 Page d'accueil")
        st.write("Bienvenue sur l'application sécurisée Streamlit.")

    elif page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.write("Voici les indicateurs de performance... (exemple)")

    elif page == "📈 Visualisation":
        st.title("📈 Visualisation de données")
        uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            x = st.selectbox("Colonne X", df.columns)
            y = st.selectbox("Colonne Y", df.columns)

            fig, ax = plt.subplots()
            ax.scatter(df[x], df[y])
            st.pyplot(fig)

    elif page == "⚙️ Paramètres":
        st.title("⚙️ Paramètres")
        st.write("Paramètres de l'application (à développer).")
