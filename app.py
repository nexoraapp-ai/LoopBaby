import streamlit as st
import os
import base64
import json
from datetime import date
import requests
import hashlib

# --- CONFIG API ---
API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# --- FUNZIONI UTENTE ---
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

if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(nome_pag):
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# --- BLOCCO ACCESSO ---
if not st.session_state.user and st.session_state.pagina not in ["Login", "Registrazione"]:
    st.session_state.pagina = "Login"

# --- HEADER ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_bg = get_base64("logo.png")

st.markdown(f"""
<style>
.stApp {{ background-color: #FDFBF7; max-width:450px; margin:auto; }}
.header {{background-image:url("data:image/png;base64,{logo_bg}"); height:120px;
display:flex; align-items:center; justify-content:center; color:white; font-size:28px; font-weight:800;}}
button {{background:#f43f5e; color:white; border:none; border-radius:12px; width:100%; padding:10px;}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">LOOPBABY</div>', unsafe_allow_html=True)

# --- LOGIN ---
if st.session_state.pagina == "Login":
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
        user = login_user(email, password)

        if user:
            st.session_state.user = user
            vai("Home")
            st.success("Login riuscito")
            st.rerun()
        else:
            st.error("Credenziali errate")

    if st.button("Registrati"):
        vai("Registrazione")
        st.rerun()

# --- REGISTRAZIONE ---
elif st.session_state.pagina == "Registrazione":
    st.title("Registrazione")

    with st.form("reg"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        nome = st.text_input("Nome genitore")
        bambino = st.text_input("Nome bambino")
        taglia = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm","86-92 cm"])
        locker = st.selectbox("Locker", ["InPost","Esselunga","Poste"])

        if st.form_submit_button("Crea account"):
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

# --- HOME ---
elif st.session_state.pagina == "Home":
    user = st.session_state.user
    st.title(f"Ciao {user['nome_genitore']} 👋")

    st.write("Benvenuto in LoopBaby")

    if st.button("Vai alle Box"):
        vai("Box")
        st.rerun()

# --- BOX ---
elif st.session_state.pagina == "Box":
    st.title("Scegli Box")

    if st.button("Box Luna - 19.90€"):
        aggiungi_al_carrello("Box Luna", 19.90)

    if st.button("Box Premium - 29.90€"):
        aggiungi_al_carrello("Box Premium", 29.90)

    if st.button("Vai al carrello"):
        vai("Carrello")
        st.rerun()

# --- CARRELLO ---
elif st.session_state.pagina == "Carrello":
    st.title("Carrello")

    totale = 0
    for item in st.session_state.carrello:
        st.write(f"{item['nome']} - {item['prezzo']}€")
        totale += item["prezzo"]

    st.write(f"Totale: {totale}€")

    if st.button("Paga"):
        st.success("Pagamento simulato")
        st.session_state.carrello = []

# --- PROFILO ---
elif st.session_state.pagina == "Profilo":
    user = st.session_state.user

    st.title("Profilo")

    st.write(user["email"])
    st.write(user["nome_genitore"])
    st.write(user["nome_bambino"])
    st.write(user["taglia"])
    st.write(user["locker"])

    if st.button("Logout"):
        st.session_state.user = None
        vai("Login")
        st.rerun()

# --- NAVBAR ---
st.markdown("---")
c = st.columns(4)

if st.session_state.user:
    if c[0].button("Home"): vai("Home"); st.rerun()
    if c[1].button("Box"): vai("Box"); st.rerun()
    if c[2].button("Carrello"): vai("Carrello"); st.rerun()
    if c[3].button("Profilo"): vai("Profilo"); st.rerun()
