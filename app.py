import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# 1. SHEETDB LOGIN / REG
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": "",
            "nome_bambino": "",
            "telefono": "",
            "taglia": "50-56 cm",
            "nascita": "",
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
            if str(u.get("email","")).lower() == email.lower() and str(u.get("password","")) == password:
                st.session_state.dati = u
                return True
    except:
        pass
    return False


# =========================
# 2. SETUP
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "loggato" not in st.session_state:
    st.session_state.loggato = False

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
# 3. LOGIN / REGISTRAZIONE
# =========================
if not st.session_state.loggato:

    st.markdown("<h1 style='text-align:center;'>LOOPBABY</h1>", unsafe_allow_html=True)

    scelta = st.radio("Accesso", ["Accedi", "Registrati"], horizontal=True)

    email = st.text_input("Email", key="email_login")
    password = st.text_input("Password", type="password", key="pass_login")

    if scelta == "Registrati":
        if st.button("CREA ACCOUNT", key="reg_btn"):
            registra_utente(email, password)
            st.success("Account creato! Ora accedi.")

    if scelta == "Accedi":
        if st.button("ENTRA", key="login_btn"):
            if login(email, password):
                st.session_state.loggato = True

                # FIX: dati sempre presenti (evita KeyError)
                st.session_state.dati = {
                    "email": st.session_state.dati.get("email",""),
                    "nome_genitore": st.session_state.dati.get("nome_genitore",""),
                    "telefono": st.session_state.dati.get("telefono",""),
                    "nome_bambino": st.session_state.dati.get("nome_bambino",""),
                    "nascita": st.session_state.dati.get("nascita",""),
                    "taglia": st.session_state.dati.get("taglia","50-56 cm"),
                    "locker": st.session_state.dati.get("locker","")
                }

                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()


# =========================
# 4. CSS (TUO IDENTICO)
# =========================
st.markdown("""
<style>
.stApp { background-color:#FDFBF7; max-width:450px; margin:auto; }
div.stButton > button {
    background:#f43f5e; color:white; border-radius:18px;
    width:100%; font-weight:800;
}
.card {
    background:white; padding:20px; border-radius:25px;
    margin:10px; border:1px solid #eee;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 5. HOME (ESEMPIO TUO)
# =========================
if st.session_state.pagina == "Home":

    u = st.session_state.dati

    nome = u.get("nome_genitore","")

    st.markdown(f"<h2>Ciao {nome} 👋</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    LoopBaby è il tuo armadio circolare ♻️
    </div>
    """, unsafe_allow_html=True)


# =========================
# 6. BOX
# =========================
elif st.session_state.pagina == "Box":
    st.markdown("## Box 📦")

    for nome in ["LUNA 🌙", "SOLE ☀️"]:
        st.markdown(f"<div class='card'><b>{nome}</b><br>19.90€</div>", unsafe_allow_html=True)
        if st.button(f"Scegli {nome}", key=nome):
            aggiungi(nome, 19.9)


# =========================
# 7. PROFILO (FIX KEYERROR)
# =========================
elif st.session_state.pagina == "Profilo":

    u = st.session_state.dati

    st.markdown("## Profilo 👤")

    st.markdown(f"""
    <div class="card">
    📧 {u.get('email','')}<br>
    📞 {u.get('telefono','')}<br>
    👶 {u.get('nome_bambino','')}<br>
    📏 {u.get('taglia','')}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.loggato = False
        st.rerun()


# =========================
# 8. CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## Carrello 🛒")

    totale = 0

    for i in st.session_state.carrello:
        st.write(f"{i['nome']} - {i['prezzo']}€")
        totale += i["prezzo"]

    st.markdown(f"### Totale: {totale}€")


# =========================
# 9. NAV BAR
# =========================
st.markdown("<hr>", unsafe_allow_html=True)

col = st.columns(4)

menu = ["Home", "Box", "Profilo", "Carrello"]

for i, m in enumerate(menu):
    with col[i]:
        if st.button(m, key=f"nav_{m}"):
            vai(m)
