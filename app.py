import streamlit as st
import requests
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "local_db.json"

# =========================
# STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "menu" not in st.session_state:
    st.session_state.menu = False


def go(p):
    st.session_state.page = p
    st.session_state.menu = False
    st.rerun()

# =========================
# LOCAL DB (backup)
# =========================
def save_local(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def load_local():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {}

# =========================
# STYLE PREMIUM BEIGE
# =========================
st.markdown("""
<style>
.stApp{
    background:#f5efe6;
    max-width:520px;
    margin:auto;
    font-family:Arial;
}

.header{
    text-align:center;
    font-size:30px;
    font-weight:900;
    color:#2b2b2b;
    margin-top:10px;
}

.sub{
    text-align:center;
    font-size:13px;
    color:#6b6258;
    margin-bottom:15px;
}

.card{
    background:white;
    border-radius:18px;
    padding:15px;
    margin:10px 0;
    border:1px solid #e8dfd2;
}

.btn button{
    background:#f4b400 !important;
    color:black !important;
    border-radius:12px !important;
    width:100%;
    font-weight:700;
}

.menu-btn button{
    font-size:22px !important;
    background:transparent !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HAMBURGER MENU
# =========================
col1, col2, col3 = st.columns([1,6,1])

with col1:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

with col2:
    st.markdown("<div class='header'>LOOPBABY</div>", unsafe_allow_html=True)

with col3:
    if st.button("🛒"):
        go("cart")

if st.session_state.menu:
    st.markdown("""
    <div class="card">
    <b>Menu</b><br><br>
    🏠 Home<br>
    📦 Box<br>
    🛍️ Vetrina<br>
    👤 Profilo<br>
    ℹ️ Info
    </div>
    """, unsafe_allow_html=True)

# =========================
# AUTH SYSTEM (EMAIL UNICA)
# =========================
if st.session_state.user is None:

    st.markdown("<div class='sub'>Accesso LoopBaby</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):
            r = requests.get(API, params={"email": email}).json()

            if not r:
                st.error("Utente non trovato")
            elif r[0]["password"] != password:
                st.error("Password errata")
            else:
                st.session_state.user = r[0]
                go("home")

    # REGISTER
    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        password_r = st.text_input("Password")

        if st.button("Crea account"):

            check = requests.get(API, params={"email": email_r}).json()

            if check:
                st.error("Email già registrata")
            else:
                payload = {
                    "data": {
                        "nome": nome,
                        "email": email_r,
                        "password": password_r
                    }
                }
                requests.post(API, json=payload)

                st.success("Account creato")
                st.rerun()

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user
nome = user.get("nome", "")

st.markdown(f"<div class='header'>Ciao {nome} 👋</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Benvenuto nel tuo sistema LoopBaby</div>", unsafe_allow_html=True)

# =========================
# NAV BAR
# =========================
c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    if st.button("Home"): go("home")
with c2:
    if st.button("Box"): go("box")
with c3:
    if st.button("Shop"): go("shop")
with c4:
    if st.button("Profilo"): go("profile")
with c5:
    if st.button("Info"): go("info")

# =========================
# HOME (BRAND)
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby è un sistema di crescita intelligente.</b><br><br>
    Non compri tutto. Usi ciò che serve mentre il bambino cresce.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    ♻️ zero sprechi<br>
    👶 crescita continua<br>
    💛 risparmio reale<br>
    📦 sistema circolare
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX CORE
# =========================
if st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    boxes = [
        ("SOLE ☀️", 14.90),
        ("LUNA 🌙", 14.90),
        ("NUVOLA ☁️", 14.90),
        ("PREMIUM 💎", 24.90)
    ]

    for name, price in boxes:

        st.markdown(f"""
        <div class="card">
        <b>{name}</b><br>
        {price}€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name": name, "price": price})

# =========================
# SHOP
# =========================
if st.session_state.page == "shop":

    st.title("🛍️ Vetrina")

    products = [
        ("Body cotone", 9.90),
        ("Tutina soft", 12.90),
        ("Set notte", 14.90)
    ]

    for n,p in products:
        st.markdown(f"<div class='card'><b>{n}</b><br>{p}€</div>", unsafe_allow_html=True)

        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": p})

# =========================
# PROFILE
# =========================
if st.session_state.page == "profile":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""))
    user["email"] = st.text_input("Email", user.get("email",""))

    if st.button("Salva"):
        st.session_state.user = user
        save_local(user)
        st.success("Salvato")

# =========================
# CART
# =========================
if st.session_state.page == "cart":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=f"rm{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# INFO
# =========================
if st.session_state.page == "info":

    st.title("ℹ️ LoopBaby")

    st.markdown("""
    <div class="card">
    Sistema circolare per bambini.<br><br>
    ✔ meno sprechi<br>
    ✔ più risparmio<br>
    ✔ crescita intelligente
    </div>
    """, unsafe_allow_html=True)
