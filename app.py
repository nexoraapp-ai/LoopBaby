import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# SESSION STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "menu" not in st.session_state:
    st.session_state.menu = False

if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# NAV
# =========================
def go(page):
    st.session_state.page = page
    st.session_state.menu = False
    st.rerun()

# =========================
# API SAFE
# =========================
def get_user(email):
    try:
        r = requests.get(API_URL, params={"email": email})
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

def create_user(data):
    return requests.post(API_URL, json={"data": data})

# =========================
# STYLE BASE
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
}

/* BUTTON */
div.stButton > button{
    background:#F4B400 !important;
    color:black !important;
    border-radius:14px !important;
    width:100% !important;
    font-weight:700 !important;
}

/* CARD */
.card{
    background:white;
    padding:15px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #e6dccd;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.user is None:

    st.title("🌸 LoopBaby")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # ---------------- LOGIN ----------------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Entra", key="login_btn"):
            users = get_user(email)

            if len(users) == 0:
                st.error("Utente non trovato")
            elif users[0].get("password") != password:
                st.error("Password errata")
            else:
                st.session_state.user = users[0]
                st.rerun()

    # ---------------- REGISTER ----------------
    with tab2:
        nome = st.text_input("Nome", key="reg_nome")
        email_r = st.text_input("Email", key="reg_email")
        pass_r = st.text_input("Password", key="reg_pass")
        tel = st.text_input("Telefono", key="reg_tel")

        if st.button("Registrati", key="reg_btn"):

            if not email_r or not pass_r:
                st.error("Compila tutti i campi")
            else:
                check = get_user(email_r)

                if len(check) > 0:
                    st.error("Email già registrata")
                else:
                    create_user({
                        "nome": nome,
                        "email": email_r,
                        "password": pass_r,
                        "telefono": tel
                    })
                    st.success("Registrazione completata")

    st.stop()

# =========================
# HEADER
# =========================
user = st.session_state.user
nome = user.get("nome","")

col1,col2 = st.columns([8,1])

with col1:
    st.markdown(f"## 👋 Ciao {nome}")

with col2:
    if st.button("☰", key="menu_btn"):
        st.session_state.menu = not st.session_state.menu

# =========================
# MENU OVERLAY (NO DUPLICATI)
# =========================
if st.session_state.menu:

    st.markdown("### MENU")

    if st.button("Home", key="m_home"): go("home")
    if st.button("Box", key="m_box"): go("box")
    if st.button("Vetrina", key="m_vetrina"): go("vetrina")
    if st.button("Info", key="m_info"): go("info")
    if st.button("Promo", key="m_promo"): go("promo")
    if st.button("Carrello", key="m_cart"): go("carrello")

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby è un sistema circolare per bambini</b><br><br>
    ♻️ crescita intelligente<br>
    👶 vestiti che seguono il bambino<br>
    💛 risparmio reale
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background:#fff1f2">
    🌸 Mamme Fondatrici attive
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "box":

    st.title("📦 Box")

    boxes = [
        ("SOLE ☀️","#FFD600"),
        ("LUNA 🌙","#E5E7EB"),
        ("NUVOLA ☁️","#94A3B8"),
        ("PREMIUM 💎","#4F46E5")
    ]

    for i,(name,color) in enumerate(boxes):

        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0;font-weight:700">
        {name}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}", key=f"box_{i}"):
            price = 24.90 if "PREMIUM" in name else 14.90
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# VETRINA
# =========================
if st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
<div class="card">
✔ rimangono a te<br>
🚚 spedizione gratis sopra 50€ o con box<br>
💸 7,90€ senza box
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi capo", key="v1"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "info":

    st.title("ℹ️ Info")

    st.markdown("""
<div class="card">
✔ box gratis andata<br>
✔ 90 giorni utilizzo<br>
✔ ritorno 7,90€ senza box
</div>
""", unsafe_allow_html=True)

# =========================
# PROMO
# =========================
if st.session_state.page == "promo":

    st.title("🌸 Mamme Fondatrici")

    st.markdown("""
<div class="card">
✔ dona 10 capi<br>
✔ box gratuita<br>
✔ spedizione inclusa
</div>
""", unsafe_allow_html=True)

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

        if c3.button("❌", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")
