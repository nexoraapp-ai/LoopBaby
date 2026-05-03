import streamlit as st
import os
import json
import base64
import requests

st.set_page_config(page_title="LoopBaby", layout="centered")

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db.json"


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
# SESSION STATE
# =========================
if "dati" not in st.session_state:
    st.session_state.dati = None

if "logged" not in st.session_state:
    st.session_state.logged = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cart" not in st.session_state:
    st.session_state.cart = []


def go(p):
    st.session_state.page = p


# =========================
# LOCKER
# =========================
LOCKERS = {
    "Italia": {
        "Milano": ["Centrale", "Porta Romana", "Bicocca"],
        "Roma": ["Termini", "Tiburtina"],
        "Napoli": ["Centro", "Vomero"],
        "Torino": ["Porta Nuova"],
        "Palermo": ["Centro"]
    }
}


def locker_ui():
    paese = st.selectbox("Paese", list(LOCKERS.keys()))
    citta = st.selectbox("Città", list(LOCKERS[paese].keys()))
    locker = st.selectbox("Locker", LOCKERS[paese][citta])
    return paese, citta, locker


# =========================
# SIDEBAR (FIXED)
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
    st.button("🛒 Carrello", on_click=lambda: go("Carrello"))


# =========================
# BLOCCO ACCESSO
# =========================
if not st.session_state.logged and st.session_state.page != "Login":
    st.session_state.page = "Login"


# =========================
# LOGIN / REGISTRAZIONE
# =========================
if st.session_state.page == "Login":

    st.title("🔐 Accesso")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # ================= LOGIN =================
    with tab1:

        email = st.text_input("Email")
        telefono = st.text_input("Telefono")

        if st.button("Accedi"):

            res = requests.get(API_URL)

            if res.status_code == 200:
                utenti = res.json()

                user = next((u for u in utenti if u["email"] == email), None)

                if user and user["telefono"] == telefono:
                    st.session_state.logged = True
                    st.session_state.dati = user
                    st.success("✔ Login effettuato")
                    go("Home")
                else:
                    st.error("Credenziali errate")

    # ================= REGISTRAZIONE =================
    with tab2:

        st.subheader("Registrati")

        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        telefono_r = st.text_input("Telefono")
        bimbo = st.text_input("Nome bambino")
        password = st.text_input("Password", type="password")

        paese, citta, locker = locker_ui()

        if st.button("Registrati"):

            res = requests.get(API_URL)
            utenti = res.json() if res.status_code == 200 else []

            if any(u["email"] == email_r for u in utenti):
                st.error("Email già registrata")
            else:

                data = {
                    "data": {
                        "nome": nome,
                        "email": email_r,
                        "telefono": telefono_r,
                        "password": password,
                        "bimbo": bimbo,
                        "paese": paese,
                        "citta": citta,
                        "locker": locker
                    }
                }

                r = requests.post(API_URL, json=data)

                if r.status_code in [200, 201]:
                    st.success("✔ Registrazione completata")
                    st.session_state.logged = True
                    st.session_state.dati = data["data"]
                    go("Home")
                else:
                    st.error("Errore registrazione")

    st.stop()


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

    d = st.session_state.dati or {}
    nome = d.get("nome", "")

    st.markdown(f"## 👋 Ciao **{nome if nome else 'benvenuto'}**")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
**LoopBaby è un sistema circolare.**

♻️ riuso intelligente  
👶 crescita bambini  
💛 risparmio reale  
""")

    with col2:
        if baby:
            st.image("bimbo.jpg", width=120, caption=d.get("bimbo", ""))


# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":
    st.title("🔥 Promo")
    st.write("Dona 10 capi → Box gratis")


# =========================
# BOX
# =========================
if st.session_state.page == "Box":
    st.title("📦 Box")

    if st.button("Aggiungi Box"):
        st.session_state.cart.append({"name": "Box", "price": 14.90})


# =========================
# INFO
# =========================
if st.session_state.page == "Info":
    st.title("ℹ️ Info")
    st.write("Sistema LoopBaby circolare")


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
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    d = st.session_state.dati or {}

    st.title("👤 Profilo")

    d["nome"] = st.text_input("Nome", d.get("nome", ""))
    d["email"] = st.text_input("Email", d.get("email", ""))
    d["telefono"] = st.text_input("Telefono", d.get("telefono", ""))
    d["bimbo"] = st.text_input("Bimbo", d.get("bimbo", ""))

    if st.button("Salva"):
        st.success("Salvato")
