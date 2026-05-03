import streamlit as st
import os
import json
import base64
import hashlib
import uuid

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "users.json"
ORDER_FILE = "orders.json"


# =========================
# IMMAGINI
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path, "rb").read()).decode()
    return ""

logo = load_img("logo.png")
baby = load_img("bimbo.jpg")


# =========================
# DATABASE LOCALE
# =========================
def load_db(file):
    if os.path.exists(file):
        return json.load(open(file))
    return {}

def save_db(file, data):
    json.dump(data, open(file, "w"))


users = load_db(DB_FILE)
orders = load_db(ORDER_FILE)


# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "user" not in st.session_state:
    st.session_state.user = None

if "cart" not in st.session_state:
    st.session_state.cart = []


def go(p):
    st.session_state.page = p


# =========================
# PASSWORD HASH (base futura Firebase)
# =========================
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()


# =========================
# LOCKER ITALIA
# =========================
LOCKERS = {
    "Milano": ["Centrale", "Porta Romana", "Bicocca"],
    "Roma": ["Termini", "Tiburtina"],
    "Napoli": ["Centro", "Vomero"],
    "Torino": ["Porta Nuova"],
    "Palermo": ["Centro"],
    "Bologna": ["Centro"],
    "Firenze": ["SMN"],
    "Bari": ["Centro"],
    "Catania": ["Centrale"],
    "Brescia": ["Centro"],
    "Verona": ["Centro"],
    "Genova": ["Porto Antico"]
}


# =========================
# SIDEBAR (STESSO DESIGN TUO)
# =========================
with st.sidebar:
    if logo:
        st.image("logo.png", width=130)

    st.button("🏠 Home", on_click=lambda: go("Home"))
    st.button("📦 Box", on_click=lambda: go("Box"))
    st.button("🛍️ Vetrina", on_click=lambda: go("Vetrina"))
    st.button("ℹ️ Info", on_click=lambda: go("Info"))
    st.button("🔥 Promo", on_click=lambda: go("Promo"))
    st.button("👤 Profilo", on_click=lambda: go("Profilo"))
    st.button("🔐 Login", on_click=lambda: go("Login"))
    st.button("🛒 Carrello", on_click=lambda: go("Carrello"))

    st.markdown("---")
    st.markdown("📞 WhatsApp: https://wa.me/393921404637")
    st.markdown("✉️ assistenza.loopbaby@gmail.com")


# =========================
# HEADER
# =========================
if logo:
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{logo}' width='180'></div>",
        unsafe_allow_html=True
    )


# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    user = st.session_state.user
    nome = user["nome"] if user else ""

    st.markdown(f"## 👋 Ciao **{nome if nome else 'benvenuto'}**")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
**LoopBaby non è un e-commerce. È un sistema.**

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
💛 risparmio reale  
""")

    with col2:
        if baby:
            st.image("bimbo.jpg", width=120, caption="👶 Il tuo bambino")

    st.markdown("### 🔥 Promo Mamme Fondatrici")
    st.markdown("Dona 10+ capi → Box omaggio")

    if st.button("Partecipa alla promo"):
        go("Promo")


# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.page == "Login":

    st.title("🔐 Accesso LoopBaby")

    tab1, tab2, tab3 = st.tabs(["Login", "Registrati", "Password dimenticata"])


    # =========================
    # LOGIN
    # =========================
    with tab1:

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):

            if email in users:

                if users[email]["password"] == hash_pw(password):

                    st.session_state.user = users[email]
                    st.success("Login effettuato")
                    go("Home")

                else:
                    st.error("Password errata")

            else:
                st.error("Utente non trovato")


    # =========================
    # REGISTER
    # =========================
    with tab2:

        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        telefono = st.text_input("Telefono")
        bimbo = st.text_input("Nome bambino")
        password_r = st.text_input("Password", type="password")

        paese = st.selectbox("Paese", ["Italia"])
        citta = st.selectbox("Città", list(LOCKERS.keys()))
        locker = st.selectbox("Locker", LOCKERS[citta])

        if st.button("Registrati"):

            if email_r in users:
                st.error("Email già registrata")

            else:

                users[email_r] = {
                    "nome": nome,
                    "email": email_r,
                    "telefono": telefono,
                    "bimbo": bimbo,
                    "password": hash_pw(password_r),
                    "paese": paese,
                    "citta": citta,
                    "locker": locker
                }

                save_db(DB_FILE, users)

                st.success("Registrazione completata")
                st.session_state.user = users[email_r]
                go("Home")


    # =========================
    # PASSWORD RESET (SIMULATO)
    # =========================
    with tab3:

        email_f = st.text_input("Email recupero")

        if st.button("Reset password"):

            if email_f in users:

                token = str(uuid.uuid4())[:6]

                users[email_f]["reset_code"] = token
                save_db(DB_FILE, users)

                st.success(f"Codice reset (simulato): {token}")

            else:
                st.error("Email non trovata")

        code = st.text_input("Codice")
        new_pw = st.text_input("Nuova password", type="password")

        if st.button("Cambia password"):

            if email_f in users and users[email_f].get("reset_code") == code:

                users[email_f]["password"] = hash_pw(new_pw)
                users[email_f]["reset_code"] = ""

                save_db(DB_FILE, users)

                st.success("Password aggiornata")

            else:
                st.error("Codice errato")

    st.stop()


# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.text_input("Peso pacco")
    st.text_input("Dimensioni")

    st.selectbox("Città locker", list(LOCKERS.keys()))

    if st.button("Invia richiesta"):
        st.success("✔ Richiesta inviata")


# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    if st.button("Aggiungi Box 14.90€"):
        st.session_state.cart.append({"name": "Box", "price": 14.90})


# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("🛒 Carrello")

    total = 0

    for i, item in enumerate(st.session_state.cart):
        c1, c2, c3 = st.columns([3, 1, 1])

        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")


# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("ℹ️ LoopBaby")

    st.markdown("""
♻️ Sistema circolare bambini  
👶 crescita intelligente  
💛 risparmio reale  
""")


# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp | ✉️ assistenza.loopbaby@gmail.com")
