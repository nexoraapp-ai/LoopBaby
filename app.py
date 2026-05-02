import streamlit as st
import requests
import json
import os
import base64
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db_loopbaby.json"

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# LOGO
# =========================
def img(file):
    if os.path.exists(file):
        return base64.b64encode(open(file,"rb").read()).decode()
    return ""

logo = img("logo.png")
baby = img("bimbo.jpg")

# =========================
# LOGIN / REGISTER
# =========================
def login(email,password):
    try:
        r = requests.get(SHEETDB_URL).json()
        for u in r:
            if u["email"].lower()==email.lower() and u["password"]==password:
                st.session_state.user = u
                return True
    except:
        pass
    return False

def register(data):
    requests.post(SHEETDB_URL, json={"data":[data]})

# =========================
# DB LOCAL PROFILO
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome":"",
        "email":"",
        "telefono":"",
        "bimbo":"",
        "nascita":"",
        "taglia":"50-56",
        "locker":"",
        "paese":"Italia"
    }

def save(d):
    json.dump(d, open(DB_FILE,"w"))

if "dati" not in st.session_state:
    st.session_state.dati = load()

if "auth" not in st.session_state:
    st.session_state.auth = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

def go(p):
    st.session_state.page = p

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
.stApp {{
    max-width:450px;
    margin:auto;
    font-family: Arial;
}}

.header {{
    text-align:center;
    padding:10px;
}}

.logo {{
    width:160px;
    margin:auto;
    display:block;
}}

.row {{
    display:flex;
    gap:10px;
}}

.card {{
    border-radius:20px;
    padding:15px;
    margin:10px 0;
    background:#fff;
    border:1px solid #eee;
}}

.btn {{
    background:#ff2d55;
    color:white;
    padding:10px;
    border-radius:15px;
    text-align:center;
    cursor:pointer;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.auth:
    st.image("logo.png", width=160)
    st.title("LoopBaby")

    mode = st.radio("Accesso",["Login","Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password",type="password")

    if mode=="Registrati":
        nome = st.text_input("Nome completo")
        telefono = st.text_input("Telefono")

        if st.button("Crea account"):
            data = {
                "email":email,
                "password":password,
                "nome":nome,
                "telefono":telefono
            }
            register(data)
            st.success("Creato!")

    if mode=="Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth=True
                st.rerun()

    st.stop()

# =========================
# HEADER
# =========================
st.image("logo.png", width=160)

# =========================
# HOME
# =========================
if st.session_state.page=="Home":

    nome = st.session_state.user.get("nome","Ciao")

    col1,col2 = st.columns([2,1])

    with col1:
        st.markdown(f"## Ciao {nome} 👋")
        st.write("LoopBaby non è un e-commerce. È uno stile. Una scelta. Un sistema.")
        st.write("♻️ crescita circolare")
        st.write("👶 bambini al centro")
        st.write("🔄 riuso intelligente")

    with col2:
        if baby:
            st.image("bimbo.jpg")

    st.markdown("### 🔥 Promo Mamme Fondatrici")
    if st.button("Accedi promo"):
        go("promo")

# =========================
# PROMO
# =========================
if st.session_state.page=="promo":
    st.title("Promo Mamme Fondatrici")

    with st.form("promo"):
        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")
        paese = st.selectbox("Paese",["Italia"])
        locker = st.text_input("Città locker")

        if st.form_submit_button("Invia"):
            st.success("Entro 48h riceverai etichetta")

# =========================
# BOX
# =========================
if st.session_state.page=="Box":
    st.title("Box LoopBaby")

    tipo = st.radio("Tipo",["Standard","Premium"])

    if tipo=="Standard":
        boxes = [
            ("SOLE ☀️","giallo",14.90),
            ("NUVOLA ☁️","blu",14.90),
            ("LUNA 🌙","grigio",14.90),
        ]

        for name,color,price in boxes:
            st.markdown(f"### {name}")
            st.write(f"{price}€ spedizione inclusa")
            if st.button("Aggiungi "+name):
                st.session_state.cart.append({"name":name,"price":price})

    else:
        st.markdown("### PREMIUM 💎")
        st.write("24.90€ nuovi/seminuovi")
        if st.button("Aggiungi premium"):
            st.session_state.cart.append({"name":"Premium","price":24.90})

# =========================
# CARRELLO
# =========================
if st.session_state.page=="Carrello":
    st.title("Carrello")

    total=0
    for i,item in enumerate(st.session_state.cart):
        col1,col2,col3 = st.columns([3,1,1])
        col1.write(item["name"])
        col2.write(str(item["price"])+"€")
        if col3.button("X",key=i):
            st.session_state.cart.pop(i)
            st.rerun()
        total+=item["price"]

    st.write("Totale:",total)

    if st.button("Checkout (domani)"):
        st.success("Placeholder pagamento")

# =========================
# INFO
# =========================
if st.session_state.page=="Info":
    st.title("Come funziona")

    st.write("""
LoopBaby è un sistema circolare:

1. Ricevi Box
2. Usi vestiti
3. Dopo 90 giorni scegli:
   - nuova taglia
   - restituzione

Nei primi 10 giorni puoi segnalare problemi.
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page=="ChiSiamo":
    st.title("Chi siamo")

    st.write("""
LoopBaby nasce da genitori.

Non è un negozio.

È un sistema per:
- risparmiare
- ridurre sprechi
- semplificare la crescita dei bambini
""")

# =========================
# PROFILO
# =========================
if st.session_state.page=="Profilo":

    d = st.session_state.dati

    st.title("Profilo")

    d["nome"] = st.text_input("Nome",d["nome"])
    d["email"] = st.text_input("Email",d["email"])
    d["telefono"] = st.text_input("Telefono",d["telefono"])
    d["bimbo"] = st.text_input("Nome bambino",d["bimbo"])
    d["taglia"] = st.selectbox("Taglia",["50-56","62-68","74-80","86-92"])

    d["paese"] = st.selectbox("Paese",["Italia"])

    if st.button("Salva"):
        save(d)
        st.success("Salvato")

# =========================
# VETRINA
# =========================
if st.session_state.page=="Vetrina":
    st.title("Vetrina")

    st.write("I capi restano per sempre")
    st.write("Spedizione gratis sopra 50€")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# FOOTER NAV
# =========================
st.markdown("---")

cols = st.columns(5)

menu = [
    ("Home","Home"),
    ("Box","Box"),
    ("Cart","Carrello"),
    ("Info","Info"),
    ("Profilo","Profilo")
]

for i,(n,p) in enumerate(menu):
    if cols[i].button(n):
        go(p)
        st.rerun()
