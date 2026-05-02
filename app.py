import streamlit as st
import requests
import bcrypt
import base64
import os
import json
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db_loopbaby.json"

# =========================
# PASSWORD
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

# =========================
# LOCKER MAP
# =========================
LOCKERS = {
    "Calolziocorte": ["Locker Centro", "Poste Italiane Calolziocorte", "InPost Point Supermarket"],
    "Milano": ["Milano Centrale Locker", "Poste Milano Duomo", "InPost Milano City"],
}

# =========================
# DB
# =========================
def email_esiste(email):
    try:
        r = requests.get(SHEETDB_URL)
        return any(u.get("email","").lower() == email.lower() for u in r.json())
    except:
        return False

def registra_user(data):
    requests.post(SHEETDB_URL, json={"data":[data]})

def login_user(email, password):
    r = requests.get(SHEETDB_URL)
    for u in r.json():
        if u["email"].lower() == email.lower():
            if check_password(password, u["password"]):
                st.session_state.user = u
                return True
    return False

def carica(email):
    r = requests.get(SHEETDB_URL)
    for u in r.json():
        if u["email"].lower() == email.lower():
            return u
    return None

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "carrello" not in st.session_state:
    st.session_state.carrello = []

# =========================
# UI HELP
# =========================
def go(p):
    st.session_state.page = p

def add_cart(n,p):
    st.session_state.carrello.append({"n":n,"p":p})
    st.toast("Aggiunto!")

# =========================
# HEADER
# =========================
st.markdown("""
<style>
body {background:#F5F1E8;}
.stApp {background:#F5F1E8;}
.header {
    text-align:center;
    font-size:30px;
    font-weight:900;
    padding:10px;
}
.card {
    background:white;
    padding:20px;
    border-radius:20px;
    margin:10px 0;
}
button {
    border-radius:15px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">LOOPBABY</div>', unsafe_allow_html=True)

# =========================
# LOGIN / REGISTRAZIONE
# =========================
if not st.session_state.auth:

    mode = st.radio("Accesso", ["Login","Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    nome = cognome = bambino = ""
    nascita = date(2024,1,1)
    taglia = "50-56 cm"
    città = "Calolziocorte"
    locker = ""

    if mode == "Registrati":

        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")

        if nascita.year >= 2024:
            taglia = "50-56 cm"
        elif nascita.year >= 2023:
            taglia = "62-68 cm"
        else:
            taglia = "74-80 cm"

        città = st.selectbox("Città", list(LOCKERS.keys()))
        locker = st.selectbox("Locker", LOCKERS[città])

        if st.button("Registrati"):
            if email_esiste(email):
                st.error("Email già esistente")
            else:
                data = {
                    "nome":nome,
                    "cognome":cognome,
                    "email":email,
                    "password":hash_password(password),
                    "bambino":bambino,
                    "nascita":str(nascita),
                    "taglia":taglia,
                    "citta":città,
                    "locker":locker
                }
                registra_user(data)
                st.success("Account creato")
                st.rerun()

    else:
        if st.button("Login"):
            if login_user(email,password):
                st.session_state.auth = True
                st.session_state.user = carica(email)
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user
nome = user.get("nome","")
baby = user.get("bambino","")

# =========================
# MENU HAMBURGER
# =========================
menu = st.selectbox("☰ Menu",[
    "Home","Box","Vetrina","Profilo","Come funziona","Contatti"
])

st.session_state.page = menu

# =========================
# HOME
# =========================
if menu == "Home":

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;">
        <div style="width:60%;">
        <h2>Ciao {nome} 👋</h2>

        <p>👶 Capi selezionati</p>
        <p>🔄 Cresce con il bambino</p>
        <p>💰 Risparmio reale</p>
        <p>🏠 Locker vicino a te</p>
        <p>♻️ Zero sprechi</p>

        <div class="card">
        <b>✨ Promo Mamme Fondatrici</b><br>
        Dona 10 capi → ricevi gift card Box (entro 3 mesi)
        </div>
        </div>

        <div style="width:35%;">
        <img src="https://via.placeholder.com/150" style="border-radius:20px;width:100%;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Dona 10 capi"):
        st.info("Entro 24h riceverai etichetta per locker scelto")

# =========================
# BOX
# =========================
elif menu == "Box":

    st.title("BOX")

    tipo = st.radio("Scegli:", ["Standard 14,90€","Premium 24,90€"])

    if "Standard" in tipo:
        scelta = st.radio("Tipi",["🌙 Luna","☀️ Sole","☁️ Nuvola"])

        st.write("Ogni box è per taglia:", user["taglia"])

        if st.button("Aggiungi"):
            add_cart(scelta,14.90)

    else:
        st.write("Premium selezionata")
        if st.button("Aggiungi Premium"):
            add_cart("Premium",24.90)

# =========================
# VETRINA
# =========================
elif menu == "Vetrina":

    st.title("Vetrina")

    st.write("Quello che scegli resta tuo")

    if st.button("Body 9.90€"):
        add_cart("Body",9.90)

# =========================
# PROFILO
# =========================
elif menu == "Profilo":

    st.title("Profilo")

    st.write(user)

# =========================
# COME FUNZIONA
# =========================
elif menu == "Come funziona":

    st.title("Come funziona")

    st.write("""
    1. Scegli box  
    2. Ricevi locker  
    3. Usa 3 mesi  
    4. Cambia taglia  
    5. Restituisci 10 capi  
    """)

# =========================
# CONTATTI
# =========================
elif menu == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📞 3921404637")

# =========================
# CARRELLO
# =========================
st.sidebar.title("Carrello")
for i in st.session_state.carrello:
    st.sidebar.write(i)

if st.sidebar.button("Paga"):
    st.success("Pagamento simulato")
    st.session_state.carrello = []
