import streamlit as st
import os
import base64
import json
from datetime import date
import requests

# =========================
# SHEETDB USERS (EXCEL LOGIN)
# =========================
USERS_API = "https://sheetdb.io/api/v1/XXXXXXX"  # <-- METTI QUI IL TUO

def registra_utente(email, password):
    payload = {
        "data": {
            "email": email,
            "password": password
        }
    }
    headers = {"Content-Type": "application/json"}
    requests.post(USERS_API, json=payload, headers=headers)

def verifica_login(email, password):
    try:
        res = requests.get(USERS_API).json()

        # SheetDB può restituire data oppure lista diretta
        users = res.get("data", res)

        for u in users:
            if u["email"] == email and u["password"] == password:
                return True
    except:
        pass

    return False

# =========================
# LOGIN SCREEN (BLOCCANTE)
# =========================
if "loggato" not in st.session_state:
    st.session_state.loggato = False

if not st.session_state.loggato:

    st.markdown("<h2 style='text-align:center;'>LoopBaby Login 🔐</h2>", unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            registra_utente(email, password)
            st.success("Account creato! Ora fai login.")

    if mode == "Login":
        if st.button("Entra"):
            if verifica_login(email, password):
                st.session_state.loggato = True
                st.success("Login riuscito!")
                st.rerun()
            else:
                st.error("Email o password errati")

    st.stop()

# =========================
# DATABASE UTENTE APP
# =========================
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except:
            pass

    return {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

def salva_dati(dati):
    d = dati.copy()
    d["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d, f)

# =========================
# SETUP APP
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(p):
    st.session_state.pagina = p

def add_cart(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto!")

# =========================
# BASE64
# =========================
def b64(file):
    if os.path.exists(file):
        return base64.b64encode(open(file, "rb").read()).decode()
    return ""

img = b64("bimbo.jpg")
logo = b64("logo.png")

# =========================
# CSS (IDENTICO CONCEPT)
# =========================
st.markdown(f"""
<style>
.stApp {{
    background:#FDFBF7;
    max-width:450px;
    margin:auto;
    padding-bottom:120px;
}}
* {{
    font-family: Lexend;
}}
.header {{
    background:url(data:image/png;base64,{logo});
    height:130px;
    background-size:cover;
    border-radius:0 0 30px 30px;
    display:flex;
    align-items:center;
    justify-content:center;
}}
.title {{
    color:white;
    font-size:32px;
    font-weight:800;
}}
.card {{
    background:white;
    padding:20px;
    margin:15px;
    border-radius:20px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><div class="title">LOOPBABY</div></div>', unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    st.write("Benvenuto 👶")

    if st.button("Vai Box"):
        vai("Box")
        st.rerun()

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.title("Box")

    if st.button("Aggiungi Box"):
        add_cart("Box LUNA", 19.90)

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.title("Carrello")

    tot = 0
    for i in st.session_state.carrello:
        st.write(i["nome"], i["prezzo"])
        tot += i["prezzo"]

    st.write("Totale:", tot)

# =========================
# NAV
# =========================
st.markdown("---")

c1, c2, c3 = st.columns(3)

if c1.button("Home"):
    vai("Home"); st.rerun()

if c2.button("Box"):
    vai("Box"); st.rerun()

if c3.button("Carrello"):
    vai("Carrello"); st.rerun()
