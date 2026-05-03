import streamlit as st
import requests

st.set_page_config(page_title="LoopBaby", layout="centered")

API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p
    st.rerun()

# =========================
# STYLE (ZALANDO INSPIRED CLEAN)
# =========================
st.markdown("""
<style>
.stApp{
    background:#f6f1e8;
    max-width:520px;
    margin:auto;
    font-family:Arial;
}

/* HEADER */
.header{
    text-align:center;
    font-size:28px;
    font-weight:900;
    color:#2f2a24;
    margin-top:10px;
}

/* SUB */
.sub{
    text-align:center;
    color:#6b6258;
    font-size:13px;
    margin-bottom:15px;
}

/* CARD (ZALANDO STYLE) */
.card{
    background:white;
    border-radius:16px;
    padding:16px;
    margin:10px 0;
    border:1px solid #e8dfd2;
    box-shadow:0 2px 8px rgba(0,0,0,0.03);
}

/* BUTTON */
div.stButton > button{
    background:#F4B400 !important;
    color:black !important;
    width:100%;
    border-radius:12px;
    font-weight:700;
    border:none;
}
</style>
""", unsafe_allow_html=True)

# =========================
# AUTH (CLEAN)
# =========================
if st.session_state.user is None:

    st.markdown("<div class='header'>LoopBaby</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Sistema circolare per la crescita dei bambini</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Accedi", "Registrati"])

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")

        if st.button("Accedi"):
            r = requests.get(API, params={"email": email}).json()

            if not r:
                st.error("Utente non trovato")
            elif r[0]["password"] != pw:
                st.error("Password errata")
            else:
                st.session_state.user = r[0]
                go("home")

    # REGISTER
    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        pw_r = st.text_input("Password")

        if st.button("Crea account"):

            check = requests.get(API, params={"email": email_r}).json()

            if check:
                st.error("Email già registrata")
            else:
                requests.post(API, json={"data":{
                    "nome":nome,
                    "email":email_r,
                    "password":pw_r
                }})

                st.success("Account creato")
                st.rerun()

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user
nome = user.get("nome","")

st.markdown(f"<div class='header'>Ciao {nome}</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Gestisci Box, Shop e crescita bambino</div>", unsafe_allow_html=True)

# =========================
# NAV (SIMPLE ZALANDO STYLE)
# =========================
col1,col2,col3,col4 = st.columns(4)

with col1:
    if st.button("Home"):
        go("home")

with col2:
    if st.button("Box"):
        go("box")

with col3:
    if st.button("Shop"):
        go("shop")

with col4:
    if st.button("Profilo"):
        go("profile")

# =========================
# HOME (ZALANDO STYLE HERO)
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby è un sistema di crescita circolare</b><br><br>
    Non compri vestiti ogni mese.<br>
    Li gestisci con la crescita del bambino.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    ✔ sempre taglia giusta<br>
    ✔ meno sprechi<br>
    ✔ risparmio continuo<br>
    ✔ sistema intelligente
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX (CORE BUSINESS)
# =========================
if st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    boxes = [
        ("SOLE ☀️",14.90),
        ("LUNA 🌙",14.90),
        ("NUVOLA ☁️",14.90),
        ("PREMIUM 💎",24.90)
    ]

    for name,price in boxes:

        st.markdown(f"""
        <div class="card">
        <b>{name}</b><br>
        <span>{price}€</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# SHOP (ZALANDO STYLE)
# =========================
if st.session_state.page == "shop":

    st.title("🛍️ Vetrina")

    st.markdown("""
    <div class="card">
    Capi singoli disponibili.<br>
    Rimangono sempre tuoi.
    </div>
    """, unsafe_allow_html=True)

    products = [
        ("Body cotone premium",9.90),
        ("Tutina soft",12.90),
        ("Pigiama bambino",8.90)
    ]

    for name,price in products:

        st.markdown(f"""
        <div class="card">
        <b>{name}</b><br>{price}€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# PROFILE
# =========================
if st.session_state.page == "profile":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""))
    user["email"] = st.text_input("Email", user.get("email",""))

    if st.button("Salva"):
        st.session_state.user = user
        st.success("Profilo aggiornato")

# =========================
# CART (SEMPLICE + SERIO)
# =========================
st.markdown("---")

total = 0

for i,item in enumerate(st.session_state.cart):

    c1,c2,c3 = st.columns([3,1,1])
    c1.write(item["name"])
    c2.write(f"{item['price']}€")

    if c3.button("❌", key=f"x{i}"):
        st.session_state.cart.pop(i)
        st.rerun()

    total += item["price"]

st.markdown(f"### Totale: {total}€")
