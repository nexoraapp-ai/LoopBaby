import streamlit as st
import requests
import hashlib
import os
import base64
import json
from datetime import date

# =========================
# 🔐 LOGIN SYSTEM
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db_loopbaby.json"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower() and u.get("password") == hash_password(password):
                return True
    except:
        pass
    return False

def registra(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower():
                return False

        requests.post(SHEETDB_URL, json={
            "data":[{"email":email,"password":hash_password(password)}]
        })
        return True
    except:
        return False

# =========================
# SESSION INIT
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "dati" not in st.session_state:
    st.session_state.dati = {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(p):
    st.session_state.pagina = p

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"{nome} aggiunto")

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            if registra(email, password):
                st.success("Account creato!")
            else:
                st.error("Email già registrata")

    if mode == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.auth = True
                st.session_state.dati["email"] = email
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

st.markdown("""
<style>
.stApp { background-color:#FDFBF7; max-width:450px; margin:auto; }
.card { border-radius:20px; padding:20px; margin:10px; background:white; box-shadow:0 5px 15px rgba(0,0,0,0.05);}
.prezzo-rosa { color:#ec4899; font-weight:800; }
</style>
""", unsafe_allow_html=True)

st.title("LOOPBABY 🌿")

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.dati["nome_genitore"].split()[0] if st.session_state.dati["nome_genitore"] else "👋"

    st.write(f"Ciao {nome}")

    st.markdown("<div class='card'>Armadio circolare per bambini</div>", unsafe_allow_html=True)

    if st.button("Vai ai Box"):
        vai("Box")

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.subheader("Scegli Box")

    taglia = st.session_state.dati["taglia"]

    st.info(f"Taglia: {taglia}")

    if st.button("Luna 🌙 - 19.90€"):
        aggiungi("Box Luna", 19.90)

    if st.button("Sole ☀️ - 19.90€"):
        aggiungi("Box Sole", 19.90)

    if st.button("Premium 💎 - 29.90€"):
        aggiungi("Box Premium", 29.90)

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":

    st.subheader("Vetrina")

    if st.button("Body Bio - 9.90€"):
        aggiungi("Body Bio", 9.90)

# =========================
# PROFILO
# =========================
elif st.session_state.pagina == "Profilo":

    st.subheader("Profilo")

    st.write(st.session_state.dati["email"])

    if st.button("Logout"):
        st.session_state.auth = False
        st.session_state.clear()
        st.rerun()

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.subheader("Carrello")

    totale = 0

    for i in st.session_state.carrello:
        st.write(f"{i['nome']} - {i['prezzo']}€")
        totale += i["prezzo"]

    st.markdown(f"### Totale: {totale:.2f}€")

    if st.button("Svuota"):
        st.session_state.carrello = []
        st.rerun()

# =========================
# NAVIGATION
# =========================
st.divider()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("Home"): vai("Home")
with c2:
    if st.button("Box"): vai("Box")
with c3:
    if st.button("Vetrina"): vai("Vetrina")
with c4:
    if st.button("Carrello"): vai("Carrello")
with c5:
    if st.button("Profilo"): vai("Profilo")
