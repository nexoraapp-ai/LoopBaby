import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# 🔐 LOGIN / REGISTER (CODICE A)
# =========================

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

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
    requests.post(SHEETDB_URL, json=payload)

def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        utenti = r.json()

        for u in utenti:
            if u.get("email","").lower() == email.lower() and u.get("password") == password:
                st.session_state.user_data = u
                return True
    except:
        pass
    return False


# =========================
# 📦 APP STATE
# =========================

st.set_page_config(page_title="LoopBaby", layout="centered")

if "loggato" not in st.session_state:
    st.session_state.loggato = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

def vai(p):
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto!")


# =========================
# 🎨 LOGIN SCREEN (BLOCCANTE)
# =========================

if not st.session_state.loggato:

    st.title("LOOPBABY 🌸")

    scelta = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if scelta == "Registrati":
        if st.button("Crea account"):
            registra_utente(email, password)
            st.success("Account creato!")

    if scelta == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.loggato = True
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()


# =========================
# 🎨 IL TUO CODICE B (INTOCCATO)
# =========================

st.title("LOOPBABY")

# NAV
menu = [("🏠","Home"),("📦","Box"),("🛍️","Vetrina"),("👤","Profilo"),("🛒","Carrello")]
cols = st.columns(len(menu))

for i,(icon,p) in enumerate(menu):
    with cols[i]:
        if st.button(icon):
            vai(p)

st.divider()


# =========================
# 🏠 HOME
# =========================

if st.session_state.pagina == "Home":
    nome = st.session_state.user_data.get("email","Mamma")

    st.markdown(f"## Ciao {nome} 👋")
    st.write("Benvenuta in LoopBaby")


# =========================
# 📦 BOX
# =========================

elif st.session_state.pagina == "Box":
    st.subheader("Box")

    for x in ["LUNA 🌙","SOLE ☀️"]:
        st.markdown(f"**{x} - 19,90€**")
        if st.button(f"Scegli {x}"):
            aggiungi(x, 19.9)


# =========================
# 🛒 CARRELLO
# =========================

elif st.session_state.pagina == "Carrello":
    st.subheader("Carrello")

    totale = 0
    for i in st.session_state.carrello:
        st.write(i["nome"], i["prezzo"])
        totale += i["prezzo"]

    st.markdown(f"### Totale: {totale}€")

    if st.button("Paga (Stripe futuro)"):
        st.success("Qui mettiamo Stripe Checkout dopo")


# =========================
# 👤 PROFILO
# =========================

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data

    st.subheader("Profilo")
    st.write("Email:", u.get("email"))
    st.write("Taglia:", u.get("taglia"))

    if st.button("Logout"):
        st.session_state.loggato = False
        st.rerun()
