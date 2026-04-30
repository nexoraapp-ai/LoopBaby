import streamlit as st
import os
import base64
import json
from datetime import date
import requests

# -------------------------
# DATABASE UTENTI (EXCEL SHEETDB)
# -------------------------
USERS_API = "https://sheetdb.io/api/v1/XXXXXXX"  # <-- METTI QUI

def registra_utente(email, password):
    payload = {"data": [{"email": email, "password": password}]}
    requests.post(USERS_API, json=payload)

def verifica_login(email, password):
    try:
        res = requests.get(USERS_API).json()
        for u in res:
            if u["email"] == email and u["password"] == password:
                return True
    except:
        pass
    return False

# -------------------------
# LOGIN / REGISTER SCREEN
# -------------------------
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
                st.error("Credenziali errate")

    st.stop()

# -------------------------
# DATABASE FILE UTENTE LOOPBABY
# -------------------------
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

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)

# -------------------------
# CONFIGURAZIONE
# -------------------------
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(nome_pag):
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# -------------------------
# BASE64 IMMAGINI
# -------------------------
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")

# -------------------------
# CSS (IDENTICO AL TUO)
# -------------------------
st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
.stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
.main .block-container {{padding: 0 !important;}}
* {{ font-family: 'Lexend', sans-serif !important; }}

.header-custom {{
    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
    background-size: cover; background-position: center; height: 130px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 35px; border-radius: 0 0 30px 30px;
}}

.header-text {{
    color: white; font-size: 32px; font-weight: 800;
}}

.card {{
    border-radius: 25px; padding: 20px; margin: 10px 20px;
    border: 1px solid #EAE2D6; text-align: center;
    background-color: #FFFFFF;
}}

.box-luna {{ background-color: #f1f5f9 !important; }}
.box-sole {{ background-color: #FFD600 !important; }}
.box-nuvola {{ background-color: #94A3B8 !important; color: white !important; }}
.box-premium {{ background: linear-gradient(135deg, #4F46E5, #312E81) !important; color: white !important; }}

.prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# -------------------------
# HOME (ESEMPLIFICATA MA IDENTICA LOGICA)
# -------------------------
if st.session_state.pagina == "Home":

    st.write("Benvenuto 👶")

    if st.button("Vai a Box"):
        vai("Box")
        st.rerun()

# -------------------------
# BOX PAGE
# -------------------------
elif st.session_state.pagina == "Box":

    st.title("Scegli Box")

    if st.button("Aggiungi Box"):
        aggiungi_al_carrello("Box LUNA", 19.90)

# -------------------------
# CARRELLO
# -------------------------
elif st.session_state.pagina == "Carrello":

    st.title("Carrello")

    totale = 0
    for item in st.session_state.carrello:
        st.write(item["nome"], item["prezzo"])
        totale += item["prezzo"]

    st.write("Totale:", totale)

# -------------------------
# NAVBAR
# -------------------------
st.markdown("<hr>", unsafe_allow_html=True)

col = st.columns(3)

if col[0].button("Home"):
    vai("Home")
    st.rerun()

if col[1].button("Box"):
    vai("Box")
    st.rerun()

if col[2].button("Carrello"):
    vai("Carrello")
    st.rerun()
