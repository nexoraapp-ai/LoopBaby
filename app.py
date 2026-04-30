import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# SHEETDB LOGIN
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def login_sheetdb(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        users = r.json()

        for u in users:
            if str(u.get("email","")).strip().lower() == email.strip().lower() and str(u.get("password","")) == password:
                return u
    except:
        pass
    return None


def register_sheetdb(email, password):
    payload = {
        "data":[{
            "email": email,
            "password": password,
            "nome_genitore":"",
            "nome_bambino":"",
            "telefono":"",
            "taglia":"50-56 cm",
            "nascita":"",
            "locker":""
        }]
    }
    requests.post(SHEETDB_URL, json=payload)


# =========================
# SETUP APP
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "loggato" not in st.session_state:
    st.session_state.loggato = False

if "dati" not in st.session_state:
    st.session_state.dati = {}

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []


def vai(p):
    st.session_state.pagina = p
    st.rerun()


def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto!")


# =========================
# LOGIN SCREEN (BLOCCO)
# =========================
if not st.session_state.loggato:

    st.markdown("## 🔐 LoopBaby Login")

    scelta = st.radio("Seleziona", ["Accedi", "Registrati"], horizontal=True)

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if scelta == "Registrati":
        if st.button("CREA ACCOUNT", key="reg"):
            register_sheetdb(email, password)
            st.success("Account creato!")

    if scelta == "Accedi":
        if st.button("ENTRA", key="login"):
            user = login_sheetdb(email, password)

            if user:
                st.session_state.loggato = True

                # FIX: garantiamo tutti i campi
                st.session_state.dati = {
                    "email": user.get("email",""),
                    "nome_genitore": user.get("nome_genitore",""),
                    "telefono": user.get("telefono",""),
                    "nome_bambino": user.get("nome_bambino",""),
                    "nascita": user.get("nascita",""),
                    "taglia": user.get("taglia","50-56 cm"),
                    "locker": user.get("locker","")
                }

                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()


# =========================
# QUI INIZIA LA TUA APP ORIGINALE
# =========================

st.title("LOOPBABY")

# NAV
col = st.columns(7)
menu = ["Home","Info","Box","Vetrina","Profilo","Carrello","ChiSiamo"]

for i,m in enumerate(menu):
    with col[i]:
        if st.button(m, key=f"nav_{m}"):
            vai(m)


# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":
    st.write("### Ciao 👋")
    st.write(st.session_state.dati.get("nome_genitore",""))

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":
    st.write("## Box 📦")

    for b in ["LUNA 🌙","SOLE ☀️"]:
        st.write(b)
        if st.button(f"Scegli {b}", key=f"box_{b}"):
            aggiungi(b, 19.9)

# =========================
# PROFILO (FIX ERRORI)
# =========================
elif st.session_state.pagina == "Profilo":

    u = st.session_state.dati

    st.write("## Profilo")

    st.write("Email:", u.get("email",""))
    st.write("Telefono:", u.get("telefono",""))
    st.write("Bambino:", u.get("nome_bambino",""))
    st.write("Taglia:", u.get("taglia",""))

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.write("## Carrello")

    totale = 0

    for i in st.session_state.carrello:
        st.write(i["nome"], i["prezzo"])
        totale += i["prezzo"]

    st.write("Totale:", totale)


# =========================
# LOGOUT
# =========================
st.markdown("---")
if st.button("Logout"):
    st.session_state.loggato = False
    st.rerun()
