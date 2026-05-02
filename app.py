import streamlit as st
import requests
import bcrypt
import base64
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# PASSWORD
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

# =========================
# LOCKER PER CITTÀ
# =========================
LOCKER = {
    "Calolziocorte": ["InPost Centro", "Esselunga", "Poste Italiane"],
    "Milano": ["Duomo Locker", "Stazione Centrale", "Porta Garibaldi"],
    "Lecco": ["Lecco Centro", "Bione Locker"]
}

# =========================
# DATI UTENTE
# =========================
def get_user(email):
    r = requests.get(SHEETDB_URL)
    for u in r.json():
        if u["email"].lower() == email.lower():
            return u
    return None

def create_user(data):
    requests.post(SHEETDB_URL, json={"data":[data]})

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# CSS (BEIGE + DESIGN)
# =========================
st.markdown("""
<style>
.stApp { background:#f5f1ea; }

.card{
    background:white;
    padding:18px;
    border-radius:20px;
    margin:10px 0;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
}

.big-title{
    font-size:28px;
    font-weight:800;
}

.menu{
    position:fixed;
    top:10px;
    right:15px;
    font-size:28px;
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU HAMBURGER
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Home", "Box", "Vetrina", "Profilo",
    "Come funziona", "Contatti", "Logout"
])

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.page == "login":

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":

        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")
        taglia = st.selectbox("Taglia", ["50-56", "62-68", "74-80"])
        città = st.selectbox("Città", list(LOCKER.keys()))
        locker = st.selectbox("Locker", LOCKER[città])

        if st.button("Crea account"):

            if get_user(email):
                st.error("Email già registrata")
            else:
                user = {
                    "email": email,
                    "password": hash_password(password),
                    "nome": nome,
                    "bambino": bambino,
                    "nascita": str(nascita),
                    "taglia": taglia,
                    "città": città,
                    "locker": locker
                }

                create_user(user)
                st.success("Account creato")
                st.session_state.user = user
                st.session_state.page = "home"
                st.rerun()

    else:
        if st.button("Entra"):
            u = get_user(email)
            if u and check_password(password, u["password"]):
                st.session_state.user = u
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()

# =========================
# UTENTE
# =========================
u = st.session_state.user
nome = u["nome"].split()[0]

# =========================
# HOME
# =========================
if menu == "Home":

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;">
        <div>
            <div class="big-title">Ciao {nome} 👋</div>

            <p>👶 Capi selezionati</p>
            <p>🔄 Cresce con il bambino</p>
            <p>💰 Risparmio reale</p>
            <p>🏠 Locker vicino a te</p>
            <p>♻️ Zero sprechi</p>

            <div class="card">
            <b>✨ Promo Mamme Fondatrici</b><br>
            Dona 10 capi → gift card box entro 3 mesi
            </div>
        </div>

        <img src="https://via.placeholder.com/180" style="border-radius:20px;">
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
elif menu == "Box":

    st.title("BOX")

    tipo = st.radio("Scegli", ["Standard 14,90€", "Premium 24,90€"])

    if tipo == "Standard 14,90€":

        scelta = st.selectbox("Box", ["Luna", "Sole", "Nuvola"])

        st.info("Box personalizzata per la tua taglia: " + u["taglia"])

    else:
        st.success("Premium selezionata")

# =========================
# VETRINA
# =========================
elif menu == "Vetrina":

    st.title("Vetrina 🛍️")

    st.write("Tutto ciò che scegli è tuo per sempre")

# =========================
# PROFILO
# =========================
elif menu == "Profilo":

    st.title("Profilo")

    st.write("Nome:", u["nome"])
    st.write("Bambino:", u["bambino"])
    st.write("Taglia:", u["taglia"])

    if st.button("Modifica"):
        st.info("Qui dopo facciamo edit completo")

# =========================
# COME FUNZIONA
# =========================
elif menu == "Come funziona":

    st.title("Come funziona")

    st.write("""
    LoopBaby è un sistema circolare:
    - ricevi box
    - usi vestiti
    - restituisci
    - ricevi nuova taglia
    """)

# =========================
# CONTATTI
# =========================
elif menu == "Contatti":

    st.title("Contatti")

    st.write("WhatsApp: 3921404637")
    st.write("Email: assistenza.loopbaby@gmail.com")

# =========================
# LOGOUT
# =========================
elif menu == "Logout":
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()
