import streamlit as st
import requests
import json
import os
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db_loopbaby.json"

# =========================
# LOGIN + REGISTRAZIONE COMPLETA
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

def registra(data):
    requests.post(SHEETDB_URL, json={"data":[data]})

# =========================
# DATI LOCAZIONE LOCKER (SEMPLIFICATO MA REALISTICO)
# =========================
LOCKER = {
    "Milano": ["Milano Centrale", "Milano Porta Romana", "Milano Loreto"],
    "Roma": ["Roma Termini", "Roma Tiburtina", "Roma EUR"],
    "Napoli": ["Napoli Centrale", "Napoli Vomero"],
    "Torino": ["Torino Porta Nuova", "Torino Lingotto"],
    "Palermo": ["Palermo Centro", "Palermo Notarbartolo"],
    "Catania": ["Catania Centrale", "Catania Borgo"],
    "Canicattì": ["Canicattì Centro"],
    "Calolziocorte": ["Lecco Locker 1", "Bergamo Locker Nord"],
    "Giffone": ["Reggio Calabria Hub", "Giffone Punto Ritiro"]
}

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p

def add_cart(n, p):
    st.session_state.cart.append({"name": n, "price": p})

def remove_item(i):
    st.session_state.cart.pop(i)

# =========================
# LOGIN
# =========================
if not st.session_state.auth:
    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome Bambino")
        telefono = st.text_input("Telefono (WhatsApp)")
        provincia = st.text_input("Provincia")
        taglia = st.selectbox("Taglia", ["50-56","62-68","74-80","86-92"])

        if st.button("Crea account"):
            data = {
                "email": email,
                "password": password,
                "nome": nome,
                "bambino": bambino,
                "telefono": telefono,
                "provincia": provincia,
                "taglia": taglia
            }
            registra(data)
            st.success("Creato!")

    if st.button("Entra"):
        if login(email,password):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Errore login")

    st.stop()

# =========================
# SIDEBAR (HAMBURGER MENU)
# =========================
with st.sidebar:
    st.title("Menu")
    if st.button("Home"): go("Home")
    if st.button("Box"): go("Box")
    if st.button("Vetrina"): go("Vetrina")
    if st.button("Come funziona"): go("Info")
    if st.button("Profilo"): go("Profilo")
    if st.button("Carrello"): go("Cart")
    if st.button("Chi siamo"): go("About")

# =========================
# HEADER LOGO
# =========================
st.markdown("""
<div style='text-align:center; padding:10px'>
    <img src='https://via.placeholder.com/180x60?text=LOOPBABY' />
</div>
""", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="width:60%">
            <h2>Ciao 👋</h2>

            <b>LoopBaby non è un e-commerce.</b><br><br>

            È uno stile. Una scelta. Un sistema.<br><br>

            ♻️ crescita circolare<br>
            👶 bambini al centro<br>
            🔄 riuso intelligente<br><br>

            <div style="background:#ffe4e6;padding:10px;border-radius:10px">
                <b>🔥 Promo Mamme Fondatrici</b><br>
                Dona 10 capi → Box omaggio
            </div>
        </div>

        <div style="width:35%">
            <img src="https://via.placeholder.com/200x250" style="border-radius:20px;width:100%">
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
elif st.session_state.page == "Box":

    st.title("Box LoopBaby 📦")

    tipo = st.radio("Scegli", ["Standard", "Premium"])

    if tipo == "Standard":
        col = st.selectbox("Tipologia", ["SOLE ☀️", "LUNA 🌙", "NUVOLA ☁️"])

        st.write("✔ capi usati in ottimo stato")
        st.write("✔ selezione premium second hand")

        if st.button("Aggiungi Box Standard 14.90€"):
            add_cart(col, 14.90)

    else:
        st.write("✔ capi nuovi o seminuovi")
        if st.button("Box Premium 24.90€"):
            add_cart("Premium", 24.90)

# =========================
# VETRINA
# =========================
elif st.session_state.page == "Vetrina":
    st.title("Vetrina 🛍️")

    st.info("I capi restano tuoi per sempre")

    if st.button("Body 9.90€"):
        add_cart("Body", 9.90)

# =========================
# INFO - COME FUNZIONA
# =========================
elif st.session_state.page == "Info":

    st.title("Come funziona")

    st.markdown("""
LoopBaby è un sistema:

📦 Ricevi Box  
👶 Usi i capi  

⏱ 10 giorni: controllo qualità  
♻️ Patto del 10: equilibrio circolare  

Dopo 90 giorni:
- nuova taglia
- oppure restituzione
""")

# =========================
# PROFILO + LOCKER
# =========================
elif st.session_state.page == "Profilo":

    st.title("Profilo")

    provincia = st.text_input("Dove abiti (provincia)")

    if provincia in LOCKER:
        st.write("Locker disponibili:")
        st.write(LOCKER[provincia])
    else:
        st.warning("Provincia non trovata (demo)")

# =========================
# CARRELLO
# =========================
elif st.session_state.page == "Cart":

    st.title("Carrello 🛒")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        st.write(f"{item['name']} - {item['price']}€")
        if st.button(f"Rimuovi {i}"):
            remove_item(i)
            st.rerun()
        total += item["price"]

    st.write("Totale:", total)

# =========================
# CHI SIAMO
# =========================
elif st.session_state.page == "About":

    st.title("Chi siamo")

    st.write("""
LoopBaby è uno stile, non un negozio.

Nasce per ridurre sprechi, far risparmiare famiglie e creare un ciclo intelligente di vestiti per bambini.
""")
