import streamlit as st
import requests
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# AUTH
# =========================
def register(nome, email, password):
    requests.post(SHEETDB_URL, json={
        "data":[{"nome": nome, "email": email, "password": password}]
    })

def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower() and u.get("password") == password:
                st.session_state.user = u
                return True
    except:
        pass
    return False

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login","Registrati"])

    nome = st.text_input("Nome e Cognome")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            register(nome, email, password)
            st.success("Account creato")

    if mode == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p

def add_item(name, price):
    st.session_state.cart.append({"name":name,"price":price})

# =========================
# SIDEBAR (HAMBURGER)
# =========================
with st.sidebar:
    st.title("☰ LoopBaby")

    pages = ["Home","Box","Promo","Info","ChiSiamo","Carrello","Profilo","Contatti"]

    for p in pages:
        if st.button(p):
            st.session_state.page = p

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{
    max-width:450px;
    margin:auto;
    background:#FDFBF7;
}

div.stButton > button{
    width:100%;
    border-radius:15px;
    background:#f43f5e;
    color:white;
}

.card{
    background:white;
    padding:15px;
    border-radius:20px;
    margin:10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO
# =========================
st.markdown("""
<div style="text-align:center;padding:10px 0;">
    <img src="logo.png" style="height:80px;object-fit:contain;">
</div>
""", unsafe_allow_html=True)

# =========================
# USER NAME FIX
# =========================
user = st.session_state.get("user", {})
nome = user.get("nome","")

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    st.markdown(f"## Ciao {nome if nome else '👋'}")

    st.markdown("""
<style>
.home{
    display:flex;
    gap:15px;
    align-items:center;
}
.left{flex:1;}
.right{
    flex:1;
    font-size:14px;
    color:#334155;
    line-height:1.5;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="home">

    <div class="left">
        <img src="bimbo.jpg" style="width:100%;border-radius:20px;">
    </div>

    <div class="right">

        <b>LoopBaby non è un e-commerce.</b><br><br>

        È uno stile. Una scelta. Un sistema.<br><br>

        ♻️ crescita circolare<br>
        👶 bambini al centro<br>
        🔄 riuso intelligente<br><br>

        <div style="background:#fff1f2;padding:10px;border-radius:15px;">
            <b>🔥 Promo Mamme Fondatrici</b><br>
            Dona 10 capi → Box omaggio
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

    if st.button("Vai alla Promo"):
        go("Promo")

# =========================
# BOX
# =========================
elif st.session_state.page == "Box":

    st.markdown("## 📦 Box")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
### STANDARD

🌙 LUNA  
☀️ SOLE  
☁️ NUVOLA  

14,90€ spedizione inclusa  
capi usati in buono stato
""")

        style = st.selectbox("Scegli stile",["Sole","Luna","Nuvola"])

        if st.button("Aggiungi Standard"):
            add_item(f"Box Standard {style}",14.90)

    with col2:
        st.markdown("""
### PREMIUM 💎

24,90€  
capi nuovi o seminuovi
""")

        if st.button("Aggiungi Premium"):
            add_item("Box Premium",24.90)

# =========================
# PROMO
# =========================
elif st.session_state.page == "Promo":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    st.markdown("""
✔ minimo 10 capi  
✔ spedizione pagata da noi  
✔ etichetta entro 48h  
""")

    with st.form("promo"):

        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")
        citta = st.text_input("Città")
        locker = st.text_input("Locker")

        if st.form_submit_button("Invia"):
            st.success("Etichetta inviata entro 48h")

# =========================
# INFO
# =========================
elif st.session_state.page == "Info":

    st.markdown("## 🔄 Come funziona")

    st.markdown("""
📦 Ricevi Box  
👶 90 giorni utilizzo  
⚠️ 48h controllo problemi  

Dopo 90 giorni:
- nuova Box (ritiro gratis)
- oppure restituzione 7,90€

♻️ Patto del 10:
10 capi = nuova Box
""")

# =========================
# CHI SIAMO
# =========================
elif st.session_state.page == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
LoopBaby nasce da genitori veri.

Non è un negozio.

È uno stile di vita:

♻️ sostenibilità  
👶 crescita intelligente  
💛 semplicità reale  
🌍 impatto positivo  
""")

# =========================
# CARRELLO
# =========================
elif st.session_state.page == "Carrello":

    st.markdown("## 🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["name"], "-", item["price"], "€")

        with c2:
            if st.button("❌", key=i):
                st.session_state.cart.pop(i)
                st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
elif st.session_state.page == "Profilo":

    st.markdown("## 👤 Profilo")

    if nome:
        st.success(f"Ciao {nome}")

# =========================
# CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.markdown("## 📞 Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")

    st.markdown("""
📱 WhatsApp:
https://wa.me/393921404637
""")
