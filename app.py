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
    st.toast(f"{nome} aggiunto!")


# =========================
# LOGIN (SOLO BLOCCO)
# =========================
if not st.session_state.loggato:

    st.markdown("## LOOPBABY 🔐")

    scelta = st.radio("Seleziona", ["Accedi", "Registrati"], horizontal=True)

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if scelta == "Registrati":
        if st.button("CREA ACCOUNT", key="reg_btn"):
            register_sheetdb(email, password)
            st.success("Account creato!")

    if scelta == "Accedi":
        if st.button("ENTRA", key="login_btn"):
            user = login_sheetdb(email, password)

            if user:
                st.session_state.loggato = True

                # FIX SICURO DATI
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
# DA QUI IN POI = TUO CODICE ORIGINALE
# (NON MODIFICATO NEL DESIGN)
# =========================


# --- NAV ---
c = st.columns(7)
menu = [("🏠","Home"),("📖","Info"),("📦","Box"),("🛍️","Vetrina"),("👤","Profilo"),("🛒","Carrello"),("👋","ChiSiamo")]

for i,(icon,pag) in enumerate(menu):
    with c[i]:
        if st.button(icon, key=f"nav_{pag}"):
            vai(pag)


# =========================
# HOME (TUO DESIGN)
# =========================
if st.session_state.pagina == "Home":

    st.markdown("""
    <div style="text-align:center;font-size:30px;font-weight:800;">
    LOOPBABY
    </div>
    """, unsafe_allow_html=True)

    nome = st.session_state.dati.get("nome_genitore","")

    st.markdown(f"""
    <div style="padding:20px;">
        <h2>Ciao {nome} 👋</h2>
        <p>L'armadio circolare per il tuo bambino</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# INFO (TUO)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## Come funziona LoopBaby 🔄")

    st.markdown("""
    <div style="padding:20px;">
    1. Scegli Box<br>
    2. Ricevi nel locker<br>
    3. Usala 3 mesi
    </div>
    """, unsafe_allow_html=True)


# =========================
# BOX (TUO STILE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## Scegli Box 📦")

    for b in ["LUNA 🌙","SOLE ☀️","NUVOLA ☁️"]:
        st.markdown(f"""
        <div style="padding:20px;border-radius:20px;background:white;margin:10px;">
        <b>{b}</b><br>19.90€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Scegli {b}", key=f"box_{b}"):
            aggiungi(b, 19.9)


# =========================
# PROFILO (FIX COMPLETO ERRORI)
# =========================
elif st.session_state.pagina == "Profilo":

    u = st.session_state.dati

    st.markdown("## Profilo 👤")

    st.markdown(f"""
    <div style="background:white;padding:20px;border-radius:20px;">
    Email: {u.get('email','')}<br>
    Tel: {u.get('telefono','')}<br>
    Bambino: {u.get('nome_bambino','')}<br>
    Taglia: {u.get('taglia','')}
    </div>
    """, unsafe_allow_html=True)


# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## Carrello 🛒")

    totale = 0

    for i in st.session_state.carrello:
        st.write(i["nome"], i["prezzo"])
        totale += i["prezzo"]

    st.write("Totale:", totale)


# =========================
# CHIUSURA / LOGOUT
# =========================
st.markdown("---")

if st.button("Logout"):
    st.session_state.loggato = False
    st.rerun()
