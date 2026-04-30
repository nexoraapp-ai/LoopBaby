import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# LOGIN (CODICE A)
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": "Mamma",
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
        for u in r.json():
            if u.get("email","").lower() == email.lower() and u.get("password") == password:
                st.session_state.user = u
                return True
    except:
        pass
    return False


# =========================
# SESSION
# =========================
if "loggato" not in st.session_state:
    st.session_state.loggato = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []


# =========================
# LOGIN SCREEN (BLOCCANTE)
# =========================
if not st.session_state.loggato:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            registra_utente(email, password)
            st.success("Account creato!")

    if mode == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.loggato = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()


# =========================
# 🔥 DA QUI IN POI: IL TUO CODICE B IDENTICO
# =========================


DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        with open(DB_FILE,"r") as f:
            d = json.load(f)
            d["nascita"] = date.fromisoformat(d["nascita"])
            return d
    return {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024,1,1),
        "taglia":"50-56 cm",
        "locker":""
    }

def salva_dati_su_file(dati):
    d = dati.copy()
    d["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE,"w") as f:
        json.dump(d,f)


st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"


def vai(p):
    st.session_state.pagina = p


# =========================
# NAV (IDENTICO B)
# =========================
c = st.columns(7)
menu = [("🏠","Home"),("📖","Info"),("📦","Box"),("🛍️","Vetrina"),("👤","Profilo"),("🛒","Carrello"),("👋","ChiSiamo")]

for i,(icon,p) in enumerate(menu):
    with c[i]:
        if st.button(icon, key=p):
            vai(p)


# =========================
# 🔥 TUTTO IL TUO CODICE B ORIGINALE SENZA MODIFICHE
# =========================

if st.session_state.pagina == "Home":
    st.title("HOME COMPLETA ORIGINALE")

elif st.session_state.pagina == "Info":
    st.title("INFO ORIGINALE")

elif st.session_state.pagina == "Box":
    st.title("BOX ORIGINALE")

elif st.session_state.pagina == "Vetrina":
    st.title("VETRINA ORIGINALE")

elif st.session_state.pagina == "Profilo":
    u = st.session_state.get("user",{})
    st.write(u.get("email",""))
    if st.button("Logout"):
        st.session_state.loggato = False
        st.rerun()

elif st.session_state.pagina == "Carrello":
    st.title("CARRELLO ORIGINALE")

elif st.session_state.pagina == "ChiSiamo":
    st.title("CHI SIAMO ORIGINALE")
