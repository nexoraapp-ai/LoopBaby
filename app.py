import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# AUTH
# =========================
def register(nome, email, password, bambino, taglia):
    requests.post(SHEETDB_URL, json={
        "data":[{
            "nome": nome,
            "email": email,
            "password": password,
            "bambino": bambino,
            "taglia": taglia
        }]
    })

def login(email, password):
    r = requests.get(SHEETDB_URL)
    for u in r.json():
        if u["email"].lower() == email.lower() and u["password"] == password:
            st.session_state.user = u
            return True
    return False

# =========================
# LOGIN PAGE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.markdown("<h1 style='text-align:center;'>LoopBaby 🌸</h1>", unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login","Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome Bambino")
        taglia = st.selectbox("Taglia iniziale", ["50-56","62-68","74-80","86-92"])

        if st.button("Crea account"):
            register(nome, email, password, bambino, taglia)
            st.success("Profilo creato")

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

user = st.session_state.get("user", {})
nome = user.get("nome","")

def go(p):
    st.session_state.page = p

def add(name, price):
    st.session_state.cart.append({"name":name,"price":price})

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{
    max-width:480px;
    margin:auto;
    background:#FDFBF7;
}

div.stButton > button{
    width:100%;
    border-radius:14px;
    background:#f43f5e;
    color:white;
    font-weight:700;
}

.card{
    background:white;
    padding:15px;
    border-radius:18px;
    margin:10px 0;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
}

.logo{
    text-align:center;
    padding:10px 0;
}

.logo img{
    height:70px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO
# =========================
st.markdown("""
<div class="logo">
    <img src="logo.png">
</div>
""", unsafe_allow_html=True)

# =========================
# MENU (HAMBURGER)
# =========================
with st.sidebar:
    st.title("☰ Menu")

    pages = ["Home","Box","Promo","Info","ChiSiamo","Carrello","Profilo","Contatti"]

    for p in pages:
        if st.button(p):
            st.session_state.page = p

# =========================
# HOME (FIX DEFINITIVO)
# =========================
if st.session_state.page == "Home":

    st.markdown(f"## Ciao {nome if nome else '👋'}")

    col1, col2 = st.columns([1,1])

    with col1:
        st.image("bimbo.jpg")

    with col2:
        st.markdown("""
<b>LoopBaby non è un e-commerce.</b><br><br>

È uno stile. Una scelta. Un sistema.<br><br>

♻️ crescita circolare<br>
👶 bambini al centro<br>
🔄 riuso intelligente
""", unsafe_allow_html=True)

        st.markdown("""
<div class="card">
<b>🔥 Promo Mamme Fondatrici</b><br>
Dona 10 capi → Box omaggio
</div>
""", unsafe_allow_html=True)

    if st.button("Scopri Promo"):
        go("Promo")

# =========================
# BOX
# =========================
elif st.session_state.page == "Box":

    st.markdown("## 📦 Box")

    c1,c2 = st.columns(2)

    with c1:
        st.markdown("""
<div class="card">
<h3>STANDARD</h3>

🌙 ☀️ ☁️

<b>14,90€</b><br>
spedizione inclusa<br>
capi usati buono stato
</div>
""", unsafe_allow_html=True)

        if st.button("Aggiungi Standard"):
            add("Box Standard",14.90)

    with c2:
        st.markdown("""
<div class="card">
<h3>PREMIUM 💎</h3>

<b>24,90€</b><br>
capi nuovi o seminuovi
</div>
""", unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            add("Box Premium",24.90)

# =========================
# PROMO
# =========================
elif st.session_state.page == "Promo":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    st.markdown("""
✔ 10 capi minimo  
✔ spedizione gratuita  
✔ risposta 48h  
""")

    with st.form("promo"):
        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")
        città = st.text_input("Città")
        locker = st.text_input("Locker")

        if st.form_submit_button("Invia"):
            st.success("Etichetta entro 48h")

# =========================
# INFO
# =========================
elif st.session_state.page == "Info":

    st.markdown("## 🔄 Come funziona")

    st.markdown("""
📦 Box 90 giorni  
⚠️ 48h controllo  

Dopo 90 giorni:
- nuova Box gratis
- oppure restituzione 7,90€

♻️ 10 capi = nuova Box
""")

# =========================
# CHI SIAMO
# =========================
elif st.session_state.page == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
LoopBaby non è un negozio.

È un sistema di vita:

♻️ sostenibilità  
👶 crescita intelligente  
💛 fiducia  
🌍 impatto reale  
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

    st.write("Nome:", nome)
    st.write("Email:", user.get("email",""))
    st.write("Bambino:", user.get("bambino",""))
    st.write("Taglia:", user.get("taglia",""))

# =========================
# CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
📧 assistenza.loopbaby@gmail.com  

📱 WhatsApp:
https://wa.me/393921404637
""")
