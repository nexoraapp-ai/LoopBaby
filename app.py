import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# STATE
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

def update_user(user):
    # SheetDB update (dipende dalla tua config)
    return requests.patch(API_URL, json={"data": user})

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

/* TITLE */
.title{
    text-align:center;
    font-size:28px;
    font-weight:900;
    color:#5a4636;
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

    st.markdown("## 🌸 LoopBaby")

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
        pass_r = st.text_input("Password", type="password", key="reg_pass")
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
                        "telefono": tel,
                        "bimbo": "",
                        "taglia": "50-56",
                        "locker": ""
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
    st.markdown(f"<div class='title'>Ciao {nome} 👋</div>", unsafe_allow_html=True)

with col2:
    if st.button("☰", key="menu_btn"):
        st.session_state.menu = not st.session_state.menu

# =========================
# MENU
# =========================
if st.session_state.menu:

    st.markdown("### MENU")

    if st.button("Home", key="m1"): go("home")
    if st.button("Box", key="m2"): go("box")
    if st.button("Vetrina", key="m3"): go("vetrina")
    if st.button("Info", key="m4"): go("info")
    if st.button("Promo", key="m5"): go("promo")
    if st.button("Profilo", key="m6"): go("profilo")
    if st.button("Carrello", key="m7"): go("carrello")

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

    st.title("📦 Box LoopBaby")

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

        if st.button(f"Aggiungi {name}", key=f"box_{i}"):
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
✔ uso 90 giorni<br>
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
# PROFILO
# =========================
if st.session_state.page == "profilo":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""), key="p1")
    user["telefono"] = st.text_input("Telefono", user.get("telefono",""), key="p2")

    if st.button("Salva", key="save_profile"):
        update_user(user)
        st.session_state.user = user
        st.success("Profilo aggiornato")

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
