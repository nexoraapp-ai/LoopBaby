import streamlit as st
import os
import base64
import json
from datetime import date
import requests
import hashlib

# --- API SHEETDB ---
API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def login_user(email, password):
    res = requests.get(f"{API_URL}/search", params={
        "email": email,
        "password": hash_password(password)
    })
    data = res.json()
    return data[0] if data else None

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Login"

if "user" not in st.session_state:
    st.session_state.user = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# 🔒 BLOCCO ACCESSO
if not st.session_state.user and st.session_state.pagina not in ["Login", "Registrazione"]:
    st.session_state.pagina = "Login"

# --- IMMAGINI ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- CSS (TUO ORIGINALE) ---
st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
.stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
.main .block-container {{padding: 0 !important;}}

.header-custom {{
    background-image: url("data:image/png;base64,{logo_bg}");
    background-size: cover; height: 130px;
    display: flex; align-items: center; justify-content: center;
}}
.header-text {{ color: white; font-size: 32px; font-weight: 800; }}

div.stButton > button {{
    background-color: #f43f5e !important;
    color: white !important;
    border-radius: 18px !important;
    width: 100% !important;
}}

.card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; background: white; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if st.session_state.pagina == "Login":
    st.markdown("## Login 🔐")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            vai("Home")
            st.rerun()
        else:
            st.error("Credenziali errate")

    if st.button("Non hai un account? Registrati"):
        vai("Registrazione")
        st.rerun()

# ---------------- REGISTRAZIONE ----------------
elif st.session_state.pagina == "Registrazione":
    st.markdown('<h2 style="text-align:center;">Registrati ✨</h2>', unsafe_allow_html=True)

    with st.form("reg_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        nome = st.text_input("Nome genitore")
        bambino = st.text_input("Nome bambino")
        taglia = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm","86-92 cm"])
        locker = st.selectbox("Locker", ["Locker Esselunga","Locker InPost","Poste Italiane"])

        if st.form_submit_button("CREA ACCOUNT"):
            nuovo = {
                "email": email,
                "password": hash_password(password),
                "nome_genitore": nome,
                "nome_bambino": bambino,
                "taglia": taglia,
                "data_inizio": str(date.today()),
                "scadenza": "",
                "locker": locker
            }
            registra_user(nuovo)

            st.success("Account creato!")
            vai("Login")
            st.rerun()

# ---------------- HOME ----------------
elif st.session_state.pagina == "Home":
    user = st.session_state.user
    nome = user.get("nome_genitore","")

    st.markdown(f"<div class='card'><h2>Ciao {nome} 👋</h2></div>", unsafe_allow_html=True)

# ---------------- PROFILO ----------------
elif st.session_state.pagina == "Profilo":
    user = st.session_state.user

    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <b>Email:</b> {user.get("email","")}<br>
        <b>Nome:</b> {user.get("nome_genitore","")}<br>
        <b>Bambino:</b> {user.get("nome_bambino","")}<br>
        <b>Taglia:</b> {user.get("taglia","")}<br>
        <b>Locker:</b> {user.get("locker","")}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.user = None
        vai("Login")
        st.rerun()

# ---------------- NAV ----------------
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c = st.columns(3)

if st.session_state.user:
    if c[0].button("🏠"): vai("Home"); st.rerun()
    if c[1].button("👤"): vai("Profilo"); st.rerun()
    if c[2].button("🚪"): 
        st.session_state.user = None
        vai("Login")
        st.rerun()
