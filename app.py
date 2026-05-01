import streamlit as st
import requests
import hashlib
import os
import base64
import json
from datetime import date

# =========================
# CONFIG
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db_loopbaby.json"

# =========================
# UTILS
# =========================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def carica_dati_base():
    return {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

# =========================
# AUTH
# =========================
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
# UI BASE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

st.title("LOOPBABY 🌿")

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":
    nome = st.session_state.dati["nome_genitore"].split()[0] if st.session_state.dati["nome_genitore"] else "👋"

    st.write(f"Ciao {nome}")

    st.markdown("### Benvenuto in LoopBaby")
    st.write("Armadio circolare per bambini")

    if st.button("Vai ai Box"):
        vai("Box")

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.subheader("Scegli la tua Box")

    taglia = st.session_state.dati["taglia"]

    st.info(f"Taglia attuale: {taglia}")

    if st.button("Box Luna 🌙 - 19.90€"):
        aggiungi("Box Luna", 19.90)

    if st.button("Box Sole ☀️ - 19.90€"):
        aggiungi("Box Sole", 19.90)

    if st.button("Box Premium 💎 - 29.90€"):
        aggiungi("Box Premium", 29.90)

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
# NAV BAR SEMPLICE
# =========================
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Home"):
        vai("Home")

with col2:
    if st.button("Box"):
        vai("Box")

with col3:
    if st.button("Carrello"):
        vai("Carrello")
