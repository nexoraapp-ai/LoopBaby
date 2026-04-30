import streamlit as st
import os
import base64
import json
from datetime import date
import requests

# =========================
# SHEETDB (TUO EXCEL)
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# LOGIN / REGISTER
# =========================

def registra_utente(email, password):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": "",
            "nome_bambino": "",
            "taglia": "50-56 cm",
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": ""
        }]
    }

    headers = {"Content-Type": "application/json"}
    r = requests.post(SHEETDB_URL, json=payload, headers=headers)

    print("REGISTER:", r.status_code, r.text)


def verifica_login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        data = r.json().get("data", [])

        for u in data:
            if u.get("email") == email and u.get("password") == password:
                return True
    except Exception as e:
        print("LOGIN ERROR:", e)

    return False


# =========================
# LOGIN SCREEN BLOCCANTE
# =========================
if "loggato" not in st.session_state:
    st.session_state.loggato = False

if not st.session_state.loggato:

    st.markdown("<h2 style='text-align:center;'>LoopBaby 🔐</h2>", unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            if email and password:
                registra_utente(email, password)
                st.success("Registrazione completata! Ora fai login.")
            else:
                st.error("Inserisci email e password")

    if mode == "Login":
        if st.button("Entra"):
            if verifica_login(email, password):
                st.session_state.loggato = True
                st.success("Accesso riuscito!")
                st.rerun()
            else:
                st.error("Email o password errati")

    st.stop()

# =========================
# APP LOOPBABY (DOPO LOGIN)
# =========================

st.set_page_config(page_title="LoopBaby", layout="centered")

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
# HOME
# =========================
if st.session_state.pagina == "Home":
    st.title("Home LoopBaby 👶")

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

    totale = 0
    for i in st.session_state.carrello:
        st.write(i["nome"], i["prezzo"])
        totale += i["prezzo"]

    st.write("Totale:", totale)

# =========================
# NAVBAR
# =========================
st.markdown("---")
c1, c2, c3 = st.columns(3)

if c1.button("Home"):
    vai("Home"); st.rerun()

if c2.button("Box"):
    vai("Box"); st.rerun()

if c3.button("Carrello"):
    vai("Carrello"); st.rerun()
