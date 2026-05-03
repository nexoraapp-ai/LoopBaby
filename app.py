import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="LoopBaby", layout="centered")

API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# STATE
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p
    st.rerun()

# =========================
# STYLE AZIENDALE
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F0E6;
    max-width:480px;
    margin:auto;
    font-family:Arial;
}

/* HERO STYLE */
.hero{
    padding:20px;
    text-align:center;
}

.title{
    font-size:28px;
    font-weight:900;
    color:#3b2f24;
}

.subtitle{
    font-size:14px;
    color:#6b5b4d;
    margin-top:10px;
    line-height:1.4;
}

/* CARD */
.card{
    background:white;
    padding:16px;
    border-radius:18px;
    margin:12px 0;
    border:1px solid #e6d8c7;
}

/* BUTTON */
div.stButton > button{
    background:#F4B400 !important;
    color:black !important;
    width:100%;
    border-radius:14px;
    font-weight:700;
}

/* MENU */
.menu{
    background:white;
    padding:10px;
    border-radius:16px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN (semplice ma reale)
# =========================
if st.session_state.user is None:

    st.markdown("""
    <div class="hero">
        <div class="title">LoopBaby</div>
        <div class="subtitle">
        Non vendiamo vestiti.<br>
        Gestiamo la crescita dei bambini in modo circolare.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Accedi", "Registrati"])

    with tab1:
        email = st.text_input("Email")
        pw = st.text_input("Password", type="password")

        if st.button("Entra"):
            r = requests.get(API, params={"email": email}).json()

            if not r:
                st.error("Utente non trovato")
            elif r[0]["password"] != pw:
                st.error("Password errata")
            else:
                st.session_state.user = r[0]
                go("home")

    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email ")
        pw_r = st.text_input("Password ", type="password")

        if st.button("Crea account"):

            check = requests.get(API, params={"email": email_r}).json()

            if check:
                st.error("Email già registrata")
            else:
                requests.post(API, json={"data":{
                    "nome":nome,
                    "email":email_r,
                    "password":pw_r,
                    "telefono":"",
                    "taglia":"50-56"
                }})

                st.success("Account creato")
                st.rerun()

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user
nome = user.get("nome","")

st.markdown(f"""
<div class="hero">
    <div class="title">Ciao {nome}</div>
    <div class="subtitle">
        Gestisci tutto da qui: Box, vestiti e crescita del tuo bambino.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# NAV AZIENDALE (3 COSE SOLO)
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home"):
        go("home")

with col2:
    if st.button("📦 Box"):
        go("box")

with col3:
    if st.button("🛍️ Shop"):
        go("shop")

# =========================
# HOME (AZIENDA)
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <div class="card">
    <b>Cos’è LoopBaby?</b><br><br>
    È un sistema che sostituisce l’acquisto continuo di vestiti bambini con un modello circolare intelligente.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    ✔ Risparmi soldi<br>
    ✔ Niente sprechi<br>
    ✔ Vestiti sempre della taglia giusta
    </div>
    """, unsafe_allow_html=True)

    if st.button("Inizia con una Box"):
        go("box")

# =========================
# BOX
# =========================
if st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    for name,price in [("SOLE ☀️",14.90),("LUNA 🌙",14.90),("NUVOLA ☁️",14.90),("PREMIUM 💎",24.90)]:

        st.markdown(f"""
        <div class="card">
        <b>{name}</b><br>{price}€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name":name,"price":price})

# =========================
# SHOP (VETRINA SERIA)
# =========================
if st.session_state.page == "shop":

    st.title("🛍️ Vetrina")

    st.markdown("""
    <div class="card">
    I capi acquistati qui restano tuoi per sempre.<br>
    Spedizione gratuita sopra 50€ o con Box.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body premium","price":9.90})

# =========================
# CARRELLO
# =========================
st.markdown("---")

total = 0

for i,item in enumerate(st.session_state.cart):
    c1,c2,c3 = st.columns([3,1,1])
    c1.write(item["name"])
    c2.write(f"{item['price']}€")

    if c3.button("❌", key=i):
        st.session_state.cart.pop(i)
        st.rerun()

    total += item["price"]

st.markdown(f"### Totale: {total}€")
