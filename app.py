import streamlit as st
import requests
import os
import json
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# LOGIN
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

def registra(email, password):
    requests.post(SHEETDB_URL, json={"data":[{"email":email,"password":password}]})

# =========================
# AUTH
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login","Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea"):
            registra(email,password)
            st.success("Creato!")

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

def carica():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome_genitore":"",
        "nome_bambino":"",
        "taglia":"50-56",
        "locker":"",
        "citta":""
    }

def salva(d):
    json.dump(d, open(DB_FILE,"w"))

if "dati" not in st.session_state:
    st.session_state.dati = carica()

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

def go(p):
    st.session_state.pagina = p

def add(nome, prezzo):
    st.session_state.carrello.append({"nome":nome,"prezzo":prezzo})

# =========================
# HAMBURGER MENU
# =========================
with st.sidebar:
    st.markdown("## ☰ LoopBaby")

    for p in ["Home","Box","Promo","Info","ChiSiamo","Carrello","Profilo","Contatti"]:
        if st.button(p):
            st.session_state.pagina = p

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{max-width:450px;margin:auto;background:#FDFBF7;}
div.stButton > button{background:#f43f5e;color:white;width:100%;border-radius:15px;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.dati["nome_genitore"]

    st.markdown(f"## Ciao {nome if nome else '👋'}")

    st.image("bimbo.jpg", use_container_width=True)

    st.markdown("""
LoopBaby è uno stile.

Non un e-commerce.

♻️ circolare  
👶 crescita bambini  
🔄 riuso intelligente  
""")

    st.markdown("""
<div class="card" style="background:#fff1f2;">
<b>🔥 PROMO MAMME FONDATRICI</b><br>
Clicca per partecipare
</div>
""", unsafe_allow_html=True)

    if st.button("Vai alla Promo"):
        go("Promo")

# =========================
# BOX (IDENTICO CONCEPT ORIGINALE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Box")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
### STANDARD 🌈

☀️ SOLE  
🌙 LUNA  
☁️ NUVOLA  

14,90€ spedizione inclusa  
capi usati buono stato
""")

        style = st.selectbox("Stile",["Sole","Luna","Nuvola"])

        if st.button("Aggiungi Standard"):
            add(f"Box Standard {style}",14.90)

    with col2:
        st.markdown("""
### PREMIUM 💎

24,90€  
capi nuovi o seminuovi
""")

        if st.button("Aggiungi Premium"):
            add("Box Premium",24.90)

# =========================
# PROMO MAMME
# =========================
elif st.session_state.pagina == "Promo":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    st.markdown("Compila → etichetta entro 48h")

    with st.form("p"):

        nome = st.text_input("Nome")
        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")
        citta = st.text_input("Città")

        if st.form_submit_button("Invia"):
            st.success("Entro 48h ricevi etichetta")

# =========================
# INFO COMPLETA
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona")

    st.markdown("""
📦 1. Ricevi Box  
👶 2. Usi 90 giorni  
⚠️ 3. 48h controllo problemi  

Dopo 90 giorni:
- nuova Box (ritiro gratis)
- oppure restituzione 7,90€

♻️ Patto del 10:
10 capi = nuova Box
""")

# =========================
# CHI SIAMO
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
LoopBaby è un sistema.

Non un negozio.

♻️ meno sprechi  
👶 crescita sostenibile  
🌍 impatto reale  
""")

# =========================
# CARRELLO (AMAZON STYLE)
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    for i,item in enumerate(st.session_state.carrello):

        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["nome"], item["prezzo"], "€")

        with c2:
            if st.button("❌", key=i):
                st.session_state.carrello.pop(i)
                st.rerun()

# =========================
# PROFILO
# =========================
elif st.session_state.pagina == "Profilo":

    d = st.session_state.dati

    st.markdown("## 👤 Profilo")

    d["nome_genitore"] = st.text_input("Nome", d["nome_genitore"])
    d["nome_bambino"] = st.text_input("Bambino", d["nome_bambino"])
    d["taglia"] = st.selectbox("Taglia",["50-56","62-68","74-80","86-92"])

    salva(d)

# =========================
# CONTATTI
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 WhatsApp: 3921404637")
