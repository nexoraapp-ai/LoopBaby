import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =====================================================
# 🔐 AUTH (DAL CODICE A - SHEETDB)
# =====================================================
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
    headers = {"Content-Type": "application/json"}
    requests.post(SHEETDB_URL, json=payload, headers=headers)

def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        utenti = r.json()

        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == password:
                st.session_state.user_data = u
                return True
    except:
        pass
    return False


# =====================================================
# 📦 DATABASE LOCALE (CODICE B)
# =====================================================
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                if "nascita" in d and d["nascita"]:
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


# =====================================================
# ⚙️ CONFIG
# =====================================================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "loggato" not in st.session_state:
    st.session_state.loggato = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []


def vai(p):
    st.session_state.pagina = p
    st.rerun()


def aggiungi(nome):
    st.session_state.carrello.append(nome)
    st.toast("Aggiunto!")


# =====================================================
# 🔐 LOGIN / REGISTRAZIONE (BLOCCANTE)
# =====================================================
if not st.session_state.loggato:

    st.title("🔐 LoopBaby Accesso")

    scelta = st.radio("Scegli", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if scelta == "Registrati":
        if st.button("Crea account"):
            if email and password:
                registra_utente(email, password)
                st.success("Registrazione OK! Ora fai login.")
            else:
                st.error("Compila tutti i campi")

    if scelta == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.loggato = True
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()


# =====================================================
# 🧠 DATI UTENTE
# =====================================================
if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()

u = st.session_state.user_data


# =====================================================
# 🧭 NAVBAR
# =====================================================
c = st.columns(7)
menu = [("🏠","Home"),("📖","Info"),("📦","Box"),("🛍️","Vetrina"),("👤","Profilo"),("🛒","Carrello"),("👋","ChiSiamo")]

for i,(icon,pag) in enumerate(menu):
    with c[i]:
        if st.button(icon):
            vai(pag)


# =====================================================
# 🏠 HOME
# =====================================================
if st.session_state.pagina == "Home":
    st.title(f"Ciao {u.get('nome_genitore','Mamma')} 👋")

    st.write("LoopBaby attivo 🔄")

    if st.button("Logout"):
        st.session_state.loggato = False
        st.session_state.user_data = {}
        st.rerun()


# =====================================================
# 📖 INFO
# =====================================================
elif st.session_state.pagina == "Info":
    st.write("Come funziona LoopBaby 🔄")


# =====================================================
# 📦 BOX
# =====================================================
elif st.session_state.pagina == "Box":
    st.write("Scegli la Box 📦")
    if st.button("Box LUNA"):
        aggiungi("Box LUNA")


# =====================================================
# 🛍️ VETRINA
# =====================================================
elif st.session_state.pagina == "Vetrina":
    st.write("Shop 🛍️")
    if st.button("Compra Body"):
        aggiungi("Body")


# =====================================================
# 👤 PROFILO
# =====================================================
elif st.session_state.pagina == "Profilo":
    st.write("👤 Profilo")
    st.write("Email:", u.get("email"))
    st.write("Nome:", u.get("nome_genitore"))
    st.write("Taglia:", u.get("taglia"))


# =====================================================
# 🛒 CARRELLO
# =====================================================
elif st.session_state.pagina == "Carrello":
    st.write("Carrello:")
    for x in st.session_state.carrello:
        st.write("-", x)


# =====================================================
# 👋 CHI SIAMO
# =====================================================
elif st.session_state.pagina == "ChiSiamo":
    st.write("Siamo genitori come te ❤️")
