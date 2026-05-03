import streamlit as st
import json
import os
import requests
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "local_db.json"

# =========================
# IMAGE
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path, "rb").read()).decode()
    return ""

logo = load_img("logo.png")

# =========================
# LOCAL DB SAFE
# =========================
def load_local():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {}

def save_local(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "menu" not in st.session_state:
    st.session_state.menu = False

# =========================
# HELPERS
# =========================
def go(p):
    st.session_state.page = p
    st.session_state.menu = False
    st.rerun()

def get_users(email):
    try:
        r = requests.get(API_URL, params={"email": email})
        return r.json() or []
    except:
        return []

def email_exists(email):
    users = get_users(email)
    for u in users:
        if u.get("email","").lower() == email.lower():
            return True
    return False

def create_user(data):
    requests.post(API_URL, json={"data": data})

# =========================
# STYLE WOW
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F0E6;
    max-width:480px;
    margin:auto;
    font-family:Arial;
}

/* HEADER */
.header{
    text-align:center;
    padding:15px;
}

/* CARD */
.card{
    background:white;
    border-radius:18px;
    padding:16px;
    margin:10px 0;
    border:1px solid #e8ddcc;
}

/* BUTTON */
div.stButton > button{
    background:#F4B400 !important;
    color:black !important;
    border-radius:12px !important;
    width:100%;
    font-weight:700;
}

/* MENU */
.menu{
    background:white;
    padding:10px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.user is None:

    st.markdown("## 🌸 LoopBaby")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    with tab1:
        email = st.text_input("Email", key="l1")
        password = st.text_input("Password", type="password", key="l2")

        if st.button("Entra", key="login"):
            users = get_users(email)

            if not users:
                st.error("Utente non trovato")
            elif users[0]["password"] != password:
                st.error("Password errata")
            else:
                st.session_state.user = users[0]
                go("home")

    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        pass_r = st.text_input("Password", type="password")
        tel = st.text_input("Telefono")

        if st.button("Registrati"):
            if email_exists(email_r):
                st.error("Email già registrata")
            else:
                user = {
                    "nome": nome,
                    "email": email_r,
                    "password": pass_r,
                    "telefono": tel,
                    "bimbo": "",
                    "taglia": "50-56"
                }

                create_user(user)
                st.success("Account creato")
                st.session_state.user = user
                go("home")

    st.stop()

# =========================
# HEADER WOW
# =========================
user = st.session_state.user
nome = user.get("nome","")

col1,col2 = st.columns([8,1])

with col1:
    if logo:
        st.markdown(f"""
        <div class="header">
        <img src="data:image/png;base64,{logo}" width="140">
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"### 👋 Ciao **{nome}**")

with col2:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

# =========================
# MENU HAMBURGER
# =========================
if st.session_state.menu:
    st.markdown("### MENU")

    if st.button("Home"): go("home")
    if st.button("Box"): go("box")
    if st.button("Vetrina"): go("vetrina")
    if st.button("Info"): go("info")
    if st.button("Promo"): go("promo")
    if st.button("Profilo"): go("profilo")
    if st.button("Carrello"): go("carrello")

# =========================
# HOME WOW
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby</b><br><br>
    Il sistema circolare per vestire bambini senza sprechi.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background:#fff3cd">
    🌸 Mamme Fondatrici attive
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "box":

    st.title("📦 Box")

    boxes = [
        ("SOLE ☀️",14.90),
        ("LUNA 🌙",14.90),
        ("NUVOLA ☁️",14.90),
        ("PREMIUM 💎",24.90)
    ]

    for i,(name,price) in enumerate(boxes):

        st.markdown(f"""
        <div class="card">
        <b>{name}</b><br>{price}€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}", key=i):
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# VETRINA
# =========================
if st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
    <div class="card">
    ✔ capi tuoi per sempre<br>
    🚚 gratis sopra 50€ o con box<br>
    💸 7,90€ senza box
    </div>
    """, unsafe_allow_html=True)

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "info":

    st.title("ℹ️ LoopBaby")

    st.markdown("""
    <div class="card">
    ♻️ sistema circolare<br>
    👶 crescita bambini<br>
    💛 risparmio reale<br><br>

    🔄 box ogni 90 giorni<br>
    🚚 spedizione gratuita con box<br>
    💸 ritorno 7,90€
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROMO
# =========================
if st.session_state.page == "promo":

    st.title("🌸 Mamme Fondatrici")

    st.markdown("""
    <div class="card">
    Dona 10 capi → Box gratuita
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROFILO
# =========================
if st.session_state.page == "profilo":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""))
    user["telefono"] = st.text_input("Telefono", user.get("telefono",""))

    if st.button("Salva"):
        st.session_state.user = user
        st.success("Salvato")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "carrello":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=f"d{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")
