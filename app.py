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

def go(p):
    st.session_state.page = p
    st.session_state.menu = False
    st.rerun()

# =========================
# API USER
# =========================
def get_user(email):
    r = requests.get(API_URL, params={"email": email})
    return r.json()

def register_user(data):
    return requests.post(API_URL, json={"data": data})

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
    font-family:Arial;
}

/* HEADER */
.title{
    text-align:center;
    font-size:30px;
    font-weight:900;
    color:#5a4636;
    margin-top:10px;
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

/* MENU */
.menu-bg{
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.5);
    z-index:999;
}
.menu-box{
    background:white;
    width:80%;
    margin:80px auto;
    padding:20px;
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.user is None:

    st.markdown("## 🌸 LoopBaby")

    tab1, tab2 = st.tabs(["Login","Registrati"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Entra"):
            users = get_user(email)
            if users and users[0]["password"] == password:
                st.session_state.user = users[0]
                st.rerun()
            else:
                st.error("Errore login")

    with tab2:
        n = st.text_input("Nome")
        e = st.text_input("Email")
        p = st.text_input("Password")
        tel = st.text_input("Telefono")

        if st.button("Registrati"):

            check = get_user(e)

            if len(check) > 0:
                st.error("Email già registrata")
            else:
                register_user({
                    "nome": n,
                    "email": e,
                    "password": p,
                    "telefono": tel
                })
                st.success("Registrazione completata")

    st.stop()

# =========================
# HEADER APP
# =========================
user = st.session_state.user
nome = user.get("nome","")

col1,col2 = st.columns([8,1])

with col1:
    st.markdown(f"<div class='title'>Ciao {nome} 👋</div>", unsafe_allow_html=True)

with col2:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

# =========================
# MENU OVERLAY
# =========================
if st.session_state.menu:
    st.markdown("""
    <div class="menu-bg">
      <div class="menu-box">
    """, unsafe_allow_html=True)

    if st.button("🏠 Home"): go("home")
    if st.button("📦 Box"): go("box")
    if st.button("🛍️ Vetrina"): go("vetrina")
    if st.button("ℹ️ Info"): go("info")
    if st.button("🌸 Mamme Fondatrici"): go("promo")
    if st.button("👤 Profilo"): go("profilo")
    if st.button("🛒 Carrello"): go("carrello")

    st.markdown("</div></div>", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby è un sistema circolare per bambini.</b><br><br>

    ♻️ crescita intelligente<br>
    👶 vestiti che seguono il bambino<br>
    💛 risparmio reale per famiglie
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background:#fff1f2">
    🌸 <b>Mamme Fondatrici</b><br>
    Accesso esclusivo + box gratuita
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    boxes = [
        ("SOLE ☀️","#FFD600"),
        ("LUNA 🌙","#E5E7EB"),
        ("NUVOLA ☁️","#94A3B8"),
        ("PREMIUM 💎","#4F46E5")
    ]

    for name,color in boxes:
        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0;font-weight:800">
        {name}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            price = 14.90 if "PREMIUM" not in name else 24.90
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# VETRINA
# =========================
if st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
<div class="card">
✔ questi capi rimangono a te<br>
🚚 spedizione gratis sopra 50€ o con box<br>
💸 7,90€ senza box
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "info":

    st.title("ℹ️ Come funziona")

    st.markdown("""
<div class="card">
✔ Box gratis andata<br>
✔ uso 90 giorni<br>
✔ ritorno gratuito con box<br>
✔ 7,90€ senza box
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
✔ ricevi box gratuita<br>
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
        if c3.button("❌",key=i):
            st.session_state.cart.pop(i)
            st.rerun()
        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "profilo":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""))
    user["telefono"] = st.text_input("Telefono", user.get("telefono",""))

    if st.button("Salva"):
        requests.patch(API_URL, json={"data":user})
        st.success("Salvato")
