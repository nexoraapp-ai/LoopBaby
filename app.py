import streamlit as st
import requests
import json
import os
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# AUTH (SHEETDB)
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

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

def register(email, password):
    requests.post(SHEETDB_URL, json={"data":[{"email":email,"password":password}]})

# =========================
# LOGIN PAGE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login","Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            register(email,password)
            st.success("Account creato")

    if mode == "Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# DB PROFILO
# =========================
DB_FILE = "db.json"

def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome":"",
        "bambino":"",
        "taglia":"50-56",
        "locker":"",
        "citta":""
    }

def save(d):
    json.dump(d, open(DB_FILE,"w"))

if "data" not in st.session_state:
    st.session_state.data = load()

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
    st.markdown("## ☰ LoopBaby")

    pages = ["Home","Box","Promo","Info","ChiSiamo","Carrello","Profilo","Contatti"]

    for p in pages:
        if st.button(p):
            st.session_state.page = p

# =========================
# STYLE BASE
# =========================
st.markdown("""
<style>
.stApp{max-width:450px;margin:auto;background:#FDFBF7;}
div.stButton > button{width:100%;border-radius:15px;background:#f43f5e;color:white;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    nome = st.session_state.data["nome"]

    st.markdown(f"## Ciao {nome if nome else '👋'}")

    st.image("bimbo.jpg", use_container_width=True)

    st.markdown("""
LoopBaby non è un e-commerce.

È uno stile di vita:

♻️ circolare  
👶 bambini al centro  
🌍 meno sprechi  
""")

    st.markdown("""
<div class="card" style="background:#fff1f2;">
<b>🔥 PROMO MAMME FONDATRICI</b><br>
Dona 10 capi → BOX omaggio
</div>
""", unsafe_allow_html=True)

    if st.button("Partecipa alla Promo"):
        go("Promo")

# =========================
# BOX (TUO SISTEMA ORIGINALE RESTA INTEGRATO)
# =========================
elif st.session_state.page == "Box":

    st.markdown("## 📦 Box LoopBaby")

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

        style = st.selectbox("Seleziona stile",["Sole","Luna","Nuvola"])

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
# PROMO MAMME FONDATRICI
# =========================
elif st.session_state.page == "Promo":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    st.markdown("""
✔ dona 10 capi  
✔ noi paghiamo spedizione  
✔ ricevi etichetta entro 48h  
""")

    with st.form("promo"):

        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")
        citta = st.text_input("Città")
        locker = st.text_input("Locker di consegna")

        if st.form_submit_button("Invia richiesta"):
            st.success("Entro 48h ricevi etichetta")

# =========================
# INFO COMPLETA
# =========================
elif st.session_state.page == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
📦 ricevi Box  
👶 uso 90 giorni  
⚠️ 48h controllo problemi  

Dopo 90 giorni:
- nuova Box (ritiro gratis)
- restituzione 7,90€

♻️ Patto del 10:
10 capi = nuova Box
""")

# =========================
# CHI SIAMO
# =========================
elif st.session_state.page == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
LoopBaby non è un negozio.

È un sistema circolare per bambini:

♻️ meno sprechi  
👶 crescita intelligente  
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

    d = st.session_state.data

    st.markdown("## 👤 Profilo")

    d["nome"] = st.text_input("Nome genitore", d["nome"])
    d["bambino"] = st.text_input("Nome bambino", d["bambino"])
    d["taglia"] = st.selectbox("Taglia",["50-56","62-68","74-80","86-92"])

    save(d)

# =========================
# CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.markdown("## 📞 Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")

    st.markdown("📱 WhatsApp: 3921404637")
