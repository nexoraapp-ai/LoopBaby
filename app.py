import streamlit as st
import requests
import bcrypt
from datetime import date

# =========================
# 🔐 DATABASE
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"


# =========================
# 🔐 PASSWORD
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())


# =========================
# 📡 UTENTI
# =========================
def get_users():
    return requests.get(SHEETDB_URL).json()


def email_esiste(email):
    return any(u["email"].lower() == email.lower() for u in get_users())


def registra_utente(user):
    requests.post(SHEETDB_URL, json={"data":[user]})


def login(email, password):
    for u in get_users():
        if u["email"].lower() == email.lower():
            if check_password(password, u["password"]):
                st.session_state.user = u
                return True
    return False


# =========================
# ⚙️ INIT SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None


# =========================
# 🎨 HEADER (LOGO + DESIGN)
# =========================
st.markdown("""
<div style="text-align:center;">
    <img src="logo.png" width="140">
</div>
""", unsafe_allow_html=True)


# =========================
# 🔐 LOGIN / REGISTER
# =========================
if st.session_state.page == "login":

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # ---------------- REGISTER ----------------
    if mode == "Registrati":

        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")
        taglia = st.selectbox("Taglia", ["50-56", "62-68", "74-80", "86-92"])
        locker = st.text_input("Locker più vicino")

        if st.button("Crea account"):

            if not email or "@" not in email:
                st.error("Email non valida")

            elif email_esiste(email):
                st.error("Email già registrata")

            else:
                user = {
                    "email": email,
                    "password": hash_password(password),
                    "nome": nome,
                    "cognome": cognome,
                    "nome_bambino": bambino,
                    "nascita": nascita.isoformat(),
                    "taglia": taglia,
                    "locker": locker
                }

                registra_utente(user)

                st.success("Account creato!")
                st.session_state.user = user
                st.session_state.page = "home"
                st.rerun()

    # ---------------- LOGIN ----------------
    else:

        if st.button("Entra"):

            if login(email, password):
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Credenziali errate")


    st.stop()


# =========================
# ☰ MENU (SIDEBAR STILE FACEBOOK)
# =========================
menu = st.sidebar.radio("☰ Menu", [
    "Home",
    "Box",
    "Vetrina",
    "Chi Siamo",
    "Come funziona",
    "Profilo",
    "Contatti"
])

st.session_state.page = menu


# =========================
# 🏠 HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user
    nome = u["nome"]

    st.markdown(f"## Ciao {nome} 👋")

    st.image("bimbo.jpg", use_container_width=True)

    st.markdown("""
    ### 🌿 LoopBaby

    👶 Capi selezionati  
    🔄 Cresce con il tuo bambino  
    💰 Risparmi fino a 1000€/anno  
    📍 Locker vicino a casa  
    ♻️ Sostenibilità reale  
    """)

    st.markdown("""
    ### ✨ Promo Mamme Fondatrici
    Dona 10 capi → ricevi box omaggio
    """)


# =========================
# 📦 BOX
# =========================
elif st.session_state.page == "Box":

    st.title("Box 📦")

    st.markdown("### Standard - 14,90€")

    if st.button("Luna 🌙"):
        st.success("Aggiunta")

    if st.button("Sole ☀️"):
        st.success("Aggiunta")

    if st.button("Nuvola ☁️"):
        st.success("Aggiunta")


    st.markdown("### Premium - 24,90€")

    if st.button("Box Premium 💎"):
        st.success("Aggiunta")


# =========================
# 🛍️ VETRINA
# =========================
elif st.session_state.page == "Vetrina":

    st.title("Vetrina 🛍️")

    st.write("Prodotti disponibili per sempre")


# =========================
# ℹ️ COME FUNZIONA
# =========================
elif st.session_state.page == "Come funziona":

    st.title("Come funziona")

    st.write("""
    1. Scegli box  
    2. Ricevi a casa/locker  
    3. Usi fino a 3 mesi  
    4. Restituisci o cambi taglia  
    """)


# =========================
# 👤 PROFILO
# =========================
elif st.session_state.page == "Profilo":

    u = st.session_state.user

    st.title("Profilo")

    st.write(u)


# =========================
# 📞 CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📞 3921404637")


# =========================
# ℹ️ CHI SIAMO
# =========================
elif st.session_state.page == "Chi Siamo":

    st.title("Chi siamo ❤️")

    st.write("Siamo genitori come te...")
