import streamlit as st
import os
import json
import base64
import requests

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

st.set_page_config(page_title="LoopBaby", layout="centered")

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
# DB LOCALE
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome": "",
        "email": "",
        "telefono": "",
        "bimbo": "",
        "taglia": "50-56",
        "paese": "Italia",
        "citta": "",
        "locker": ""
    }

def save(d):
    json.dump(d, open(DB_FILE, "w"))


if "dati" not in st.session_state:
    st.session_state.dati = load()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged" not in st.session_state:
    st.session_state.logged = False


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
        "Palermo": ["Centro"],
        "Catania": ["Centrale"],
        "Bergamo": ["Centro"],
        "Brescia": ["Centro"],
        "Firenze": ["SMN"],
        "Bari": ["Centro"],
        "Canicattì": ["Hub"],
        "Giffone": ["Reggio Calabria Locker"]
    }
}

def locker_ui():
    paese = st.selectbox("Paese", list(LOCKERS.keys()), key="paese_sel")
    citta = st.selectbox("Città", list(LOCKERS[paese].keys()), key="citta_sel")
    locker = st.selectbox("Locker", LOCKERS[paese][citta], key="locker_sel")
    return paese, citta, locker


# =========================
# SIDEBAR
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
# LOGIN / REGISTRAZIONE
# =========================
if st.session_state.page == "Login":

    st.title("🔐 Accesso")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # LOGIN
    with tab1:

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Accedi"):

            if email and password:

                res = requests.get(API_URL, params={"email": email})

                if res.status_code == 200 and len(res.json()) > 0:

                    user = res.json()[0]

                    if user.get("password") == password:
                        st.session_state.logged = True
                        st.session_state.dati = user
                        st.success("✔ Login effettuato")
                        go("Home")
                    else:
                        st.error("Password errata")

                else:
                    st.error("Utente non trovato")

    # REGISTRAZIONE
    with tab2:

        nome = st.text_input("Nome", key="reg_nome")
        email_r = st.text_input("Email", key="reg_email")
        telefono_r = st.text_input("Telefono", key="reg_tel")
        bimbo = st.text_input("Nome bambino", key="reg_bimbo")
        password = st.text_input("Password", type="password", key="reg_pass")

        paese, citta, locker = locker_ui()

        if st.button("Registrati"):

            if nome and email_r and telefono_r and password:

                check = requests.get(API_URL, params={"email": email_r})

                if len(check.json()) > 0:
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

                    res = requests.post(API_URL, json=data)

                    if res.status_code in [200, 201]:
                        st.success("✔ Registrazione completata")
                        st.session_state.logged = True
                        st.session_state.dati = data["data"]
                        go("Home")
                    else:
                        st.error("Errore registrazione")

    st.stop()


# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    d = st.session_state.dati
    nome = d.get("nome", "")

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
            st.image("bimbo.jpg", width=120, caption=d.get("bimbo", "Il tuo bambino"))

    st.markdown("### 🔥 Promo Mamme Fondatrici")
    st.markdown("Dona 10+ capi → Box omaggio")

    if st.button("Partecipa alla promo"):
        go("Promo")


# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.markdown("""
🎁 Doni 10 o più capi  
📦 Ricevi Box gratuita  
🚚 Spedizione inclusa  
♻️ Economia circolare
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    locker_ui()

    if st.button("Invia richiesta"):
        st.success("✔ Etichetta inviata entro 48h")


# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    tipo = st.radio("Scegli", ["Standard", "Premium"])

    if tipo == "Standard":

        st.markdown("### 14,90€")

        for name, color, desc in [
            ("SOLE ☀️", "#FFD600", "colorati"),
            ("LUNA 🌙", "#E5E7EB", "neutri"),
            ("NUVOLA ☁️", "#94A3B8", "soft")
        ]:

            st.markdown(f"<div style='background:{color};padding:10px;border-radius:10px'><b>{name}</b> {desc}</div>", unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}"):
                st.session_state.cart.append({"name": name, "price": 14.90})

    else:

        st.markdown("### PREMIUM 24,90€")

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name": "Premium", "price": 24.90})


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
# INFO / PROFILO / VETRINA
# =========================
if st.session_state.page == "Info":
    st.title("ℹ️ Info")
    st.write("Sistema LoopBaby")

if st.session_state.page == "Profilo":
    st.title("👤 Profilo")
    d = st.session_state.dati
    st.write(d)

if st.session_state.page == "Vetrina":
    st.title("🛍️ Vetrina")
    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp | ✉️ assistenza.loopbaby@gmail.com")
