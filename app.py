import streamlit as st
import requests
import json
import os
import base64
from datetime import date

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# ASSETS
# =========================
def img(file):
    if os.path.exists(file):
        return base64.b64encode(open(file,"rb").read()).decode()
    return ""

logo = img("logo.png")
baby = img("bimbo.jpg")

# =========================
# DB
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome":"",
        "email":"",
        "telefono":"",
        "bimbo":"",
        "taglia":"50-56",
        "locker":"",
        "paese":"Italia"
    }

def save(d):
    json.dump(d, open(DB_FILE,"w"))

if "dati" not in st.session_state:
    st.session_state.dati = load()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

def go(p):
    st.session_state.page = p

# =========================
# CSS SHOPIFY STYLE
# =========================
st.markdown("""
<style>
.stApp{max-width:450px;margin:auto;font-family:Arial;}
.logo{width:180px;margin:auto;display:block;}

.card{
background:white;
border-radius:20px;
padding:15px;
margin:10px 0;
border:1px solid #eee;
}

.row{display:flex;gap:10px;}

.btn{
background:#ff2d55;
color:white;
padding:10px;
border-radius:12px;
text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER LOGO
# =========================
st.image("logo.png", width=180)

# =========================
# HOME
# =========================
if st.session_state.page=="Home":

    d = st.session_state.dati

    col1,col2 = st.columns([2,1])

    with col1:
        st.markdown("## Ciao 👋")
        st.markdown("""
**LoopBaby non è un e-commerce.**

È uno stile. Una scelta. Un sistema.

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
""")

    with col2:
        if baby:
            st.image("bimbo.jpg")

    st.markdown("### 🔥 Promo Mamme Fondatrici")
    if st.button("Accedi"):
        go("promo")

# =========================
# PROMO
# =========================
if st.session_state.page=="promo":

    st.title("Promo Mamme Fondatrici")

    st.markdown("""
Dona 10 capi → ricevi BOX OMAGGIO
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    paese = st.selectbox("Paese",["Italia"])
    città = st.text_input("Città locker")

    if st.button("Invia"):
        st.success("Entro 48h ricevi etichetta")

# =========================
# BOX
# =========================
if st.session_state.page=="Box":

    st.title("Box")

    tipo = st.radio("Tipo",["Standard","Premium"])

    if tipo=="Standard":

        boxes = [
            ("SOLE ☀️","#FFD600"),
            ("LUNA 🌙","#E5E7EB"),
            ("NUVOLA ☁️","#94A3B8")
        ]

        for name,color in boxes:
            st.markdown(f"""
            <div class="card" style="background:{color}">
            <b>{name}</b><br>
            14,90€ spedizione inclusa
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}"):
                st.session_state.cart.append({"name":name,"price":14.90})

    else:
        st.markdown("""
        <div class="card" style="background:#4F46E5;color:white">
        <b>PREMIUM 💎</b><br>
        24,90€ nuovi/seminuovi
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name":"Premium","price":24.90})

# =========================
# VETRINA
# =========================
if st.session_state.page=="Vetrina":

    st.title("Vetrina")

    st.markdown("""
I capi restano per sempre.

Spedizione:
- gratis sopra 50€
- oppure con Box
""")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})

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
        st.success("Pagamento placeholder")

# =========================
# INFO
# =========================
if st.session_state.page=="Info":

    st.title("Come funziona")

    st.markdown("""
1. Ricevi box
2. Usi vestiti
3. Dopo 90 giorni:
   - nuova taglia
   - restituzione

📍 10 giorni: controllo qualità  
♻️ patto del 10: equilibrio capi
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page=="ChiSiamo":

    st.title("Chi siamo")

    st.write("""
LoopBaby è uno stile, non un negozio.

È un sistema per:
- crescere bambini
- ridurre sprechi
- semplificare la vita
""")

# =========================
# PROFILO COMPLETO
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
    d["locker"] = st.text_input("Locker città")

    if st.button("Salva"):
        save(d)
        st.success("Salvato")

# =========================
# NAV
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
