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

# --- CONFIG ---
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

# --- BLOCCO LOGIN ---
if not st.session_state.user and st.session_state.pagina not in ["Login", "Registrazione"]:
    st.session_state.pagina = "Login"

# --- HEADER ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")

st.markdown(f"""
<style>
.stApp {{ background-color:#FDFBF7; max-width:450px; margin:auto; }}
.header {{background-image:url("data:image/png;base64,{logo_bg}"); height:130px;
display:flex; align-items:center; justify-content:center; color:white; font-size:30px; font-weight:800;}}
button {{background:#f43f5e; color:white; border:none; border-radius:15px; width:100%; padding:10px; margin-top:10px;}}
.card {{border-radius:20px; padding:15px; margin:10px; background:white; box-shadow:0 5px 15px rgba(0,0,0,0.05);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">LOOPBABY</div>', unsafe_allow_html=True)

# --- LOGIN ---
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

    if st.button("Registrati"):
        vai("Registrazione")
        st.rerun()

# --- REGISTRAZIONE ---
elif st.session_state.pagina == "Registrazione":
    st.markdown("## Registrati ✨")

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
    nome = user.get("nome_genitore","")

    st.markdown(f"<div class='card'><h2>Ciao {nome} 👋</h2><p>Benvenuto in LoopBaby</p></div>", unsafe_allow_html=True)

    if st.button("Vai alle Box"):
        vai("Box"); st.rerun()

# --- BOX ---
elif st.session_state.pagina == "Box":
    st.markdown("## Scegli la tua Box 📦")

    if st.button("Box Luna 🌙 - 19,90€"):
        aggiungi_al_carrello("Box Luna", 19.90)

    if st.button("Box Premium 💎 - 29,90€"):
        aggiungi_al_carrello("Box Premium", 29.90)

# --- CARRELLO ---
elif st.session_state.pagina == "Carrello":
    st.markdown("## Carrello 🛒")

    totale = sum(i["prezzo"] for i in st.session_state.carrello)

    for item in st.session_state.carrello:
        st.write(f"{item['nome']} - {item['prezzo']}€")

    st.write(f"Totale: {totale}€")

    if st.button("Paga"):
        st.success("Pagamento simulato")
        st.session_state.carrello = []

# --- PROFILO ---
elif st.session_state.pagina == "Profilo":
    user = st.session_state.user

    st.markdown("## Profilo 👤")

    st.write("Email:", user.get("email",""))
    st.write("Nome:", user.get("nome_genitore",""))
    st.write("Bambino:", user.get("nome_bambino",""))
    st.write("Taglia:", user.get("taglia",""))
    st.write("Locker:", user.get("locker",""))

    if st.button("Logout"):
        st.session_state.user = None
        vai("Login")
        st.rerun()

# --- NAV ---
st.markdown("---")
c = st.columns(4)

if st.session_state.user:
    if c[0].button("Home"): vai("Home"); st.rerun()
    if c[1].button("Box"): vai("Box"); st.rerun()
    if c[2].button("Carrello"): vai("Carrello"); st.rerun()
    if c[3].button("Profilo"): vai("Profilo"); st.rerun()
