import streamlit as st
import requests
import json
import os
from datetime import date

# =========================
# 🔐 DATABASE LOGIN (SHEETDB)
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

LOCKERS_REALI = [
    "InPost Locker - Milano Centrale",
    "InPost Locker - Milano Porta Garibaldi",
    "InPost Locker - Esselunga via Ripamonti",
    "InPost Locker - Carrefour Viale Zara",
    "Poste Italiane - Milano Duomo",
    "Poste Italiane - Milano Lambrate",
    "Amazon Locker - Milano CityLife"
]

# =========================
# LOGIN / REGISTRAZIONE
# =========================
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

def registra(email, password):
    requests.post(SHEETDB_URL, json={
        "data":[
            {
                "email": email,
                "password": password,
                "nome_genitore": "",
                "telefono": "",
                "nome_bambino": "",
                "nascita": "",
                "taglia": "50-56 cm",
                "locker": ""
            }
        ]
    })

# =========================
# SESSIONE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login","Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        nome = st.text_input("Nome e Cognome")
        telefono = st.text_input("Telefono")
        bambino = st.text_input("Nome Bambino")
        nascita = st.date_input("Data nascita")
        locker = st.selectbox("Scegli Locker", LOCKERS_REALI)

        if st.button("Crea account"):
            registra(email, password)
            st.session_state.auth = True
            st.session_state.profile = {
                "email": email,
                "nome_genitore": nome,
                "telefono": telefono,
                "nome_bambino": bambino,
                "nascita": nascita,
                "taglia": "50-56 cm",
                "locker": locker
            }
            st.rerun()

    if mode == "Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()

# =========================
# UI BASE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(p): st.session_state.pagina = p

def add_cart(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast("Aggiunto al carrello")

# =========================
# 🎨 CSS (INVARIATO DESIGN)
# =========================
st.markdown("""
<style>
.stApp {background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button {background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.title("LOOPBABY 🌸")

# =========================
# 🍔 HAMBURGER MENU
# =========================
with st.sidebar:
    st.markdown("## 🍔 Menu")
    menu = st.radio("", ["Home","Box","Vetrina","Profilo","Carrello","Info","ChiSiamo","Contatti"])

vai(menu)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":
    st.markdown("### Ciao 👋")
    st.write("Benvenuta nella tua piattaforma circolare stile Shopify")

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":
    st.markdown("## 📦 Box")

    for b in ["LUNA 🌙","SOLE ☀️","NUVOLA ☁️"]:
        st.markdown(f"<div class='card'><b>{b}</b><br>19,90€</div>", unsafe_allow_html=True)
        if st.button(f"Scegli {b}"):
            add_cart(b, 19.9)

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":
    st.markdown("## 🛍️ Vetrina")
    st.markdown("<div class='card'>Body Bio LoopLove - 9,90€</div>", unsafe_allow_html=True)
    if st.button("Aggiungi"):
        add_cart("Body Bio LoopLove", 9.9)

# =========================
# PROFILO (EDIT SEMPRE ATTIVO)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    p = st.session_state.get("profile", {})

    nome = st.text_input("Nome", p.get("nome_genitore",""))
    tel = st.text_input("Telefono", p.get("telefono",""))
    bambino = st.text_input("Bambino", p.get("nome_bambino",""))
    nascita = st.date_input("Nascita", date.today())
    taglia = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm"])
    locker = st.selectbox("Locker", LOCKERS_REALI)

    if st.button("Salva"):
        st.session_state.profile = {
            "nome_genitore": nome,
            "telefono": tel,
            "nome_bambino": bambino,
            "nascita": nascita,
            "taglia": taglia,
            "locker": locker
        }
        st.success("Profilo aggiornato")

    st.markdown("### 📍 Locker attuale")
    st.info(st.session_state.profile.get("locker","non selezionato"))

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0
    for i in st.session_state.carrello:
        st.write(i["nome"], "-", i["prezzo"])
        totale += i["prezzo"]

    st.markdown(f"### Totale: {totale}€")

# =========================
# INFO
# =========================
elif st.session_state.pagina == "Info":
    st.write("Come funziona LoopBaby...")

# =========================
# CHI SIAMO
# =========================
elif st.session_state.pagina == "ChiSiamo":
    st.write("Siamo genitori come te ❤️")

# =========================
# CONTATTI
# =========================
elif st.session_state.pagina == "Contatti":
    st.write("WhatsApp + Email")
