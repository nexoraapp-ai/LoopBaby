import streamlit as st
import base64
import os
import webbrowser

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# IMMAGINI
# =========================
def get_base64(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = get_base64("logo.png")
bimbo = "bimbo.jpg"

# =========================
# LOGO (SOLO CENTRATO)
# =========================
st.markdown(f"""
<div style="text-align:center; padding:10px;">
    <img src="data:image/png;base64,{logo}" style="width:180px;">
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "user" not in st.session_state:
    st.session_state.user = {"name":"Mamma","city":""}

# =========================
# LOCKER ITALIA
# =========================
LOCKERS = {
    "milano":["InPost Milano","Esselunga Milano","Amazon Locker Milano"],
    "roma":["Poste Roma","InPost Roma"],
    "torino":["InPost Torino"],
    "napoli":["Poste Napoli"],
    "bergamo":["Locker Bergamo"],
    "lecco":["InPost Lecco"],
    "calolzio":["Locker Calolziocorte"]
}

def get_lockers(city):
    c = city.lower()
    for k,v in LOCKERS.items():
        if k in c:
            return v
    return ["InPost Italia","Poste Italiane","Amazon Locker Italia"]

# =========================
# NAV
# =========================
def go(p):
    st.session_state.page = p

def add_item(name, price):
    st.session_state.cart.append({"name":name,"price":price})

def whatsapp():
    webbrowser.open("https://wa.me/393921404637")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button{background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
with st.sidebar:
    st.radio("Menu",[
        "Home","Box","Vetrina","Promo Mamme","Profilo",
        "Carrello","Info","Chi Siamo","Contatti","App"
    ], key="m")
    go(st.session_state.m)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    name = st.session_state.user["name"]

    col1,col2 = st.columns([2,1])

    with col1:
        st.markdown(f"## Ciao {name} 👋")

        st.markdown("""
        **LoopBaby non è un e-commerce.**  
        È uno stile. Una scelta. Un sistema.

        👶 Crescita intelligente  
        🔄 Circolo continuo  
        ♻️ Zero sprechi  
        """)

    with col2:
        st.image(bimbo, width=130)

    if st.button("🔥 PROMO MAMME FONDATRICI"):
        go("Promo Mamme")

# =========================
# BOX (COME TUO ORIGINALE)
# =========================
elif st.session_state.page == "Box":

    st.markdown("## 📦 Box LoopBaby")

    col1,col2 = st.columns(2)

    # STANDARD
    with col1:
        st.markdown("""
        <div class="card" style="background:#fef9c3;">
        <h3>SOLE ☀️</h3>
        <b>14,90€ spedizione inclusa</b><br><br>
        ✔ capi usati in buono stato<br>
        ✔ igienizzati<br>
        ✔ selezione LoopBaby
        </div>
        """, unsafe_allow_html=True)

        style = st.selectbox("Stile",["Neutro","Rosa","Azzurro","Mix"])

        if st.button("Aggiungi Standard"):
            add_item(f"Box Sole ({style})",14.90)

    # PREMIUM
    with col2:
        st.markdown("""
        <div class="card">
        <h3>PREMIUM 💎</h3>
        <b>24,90€</b><br><br>
        ✔ nuovi o seminuovi<br>
        ✔ qualità alta
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            add_item("Box Premium",24.90)

# =========================
# VETRINA
# =========================
elif st.session_state.page == "Vetrina":

    st.markdown("## 🛍️ Vetrina")

    st.markdown("""
    I capi della Vetrina restano sempre tuoi.

    🚚 Spedizione:
    - GRATIS con Box
    - GRATIS sopra 50€
    - 7,90€ sotto 50€
    """)

# =========================
# PROMO MAMME
# =========================
elif st.session_state.page == "Promo Mamme":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    st.markdown("""
    Accedi al programma fondatrici.

    ✔ spedizione gratuita  
    ✔ etichetta inclusa  
    ✔ risposta entro 48h  
    """)

    with st.form("promo"):

        name = st.text_input("Nome")
        weight = st.text_input("Peso pacco")
        size = st.text_input("Dimensioni")
        city = st.text_input("Città")

        locker = st.selectbox("Locker", get_lockers(city))

        send = st.form_submit_button("Invia")

        if send:
            st.success("Ricevuto! Entro 48h riceverai etichetta.")

# =========================
# PROFILO (FIXED)
# =========================
elif st.session_state.page == "Profilo":

    st.markdown("## 👤 Profilo")

    u = st.session_state.user

    u["name"] = st.text_input("Nome",u["name"])
    u["city"] = st.text_input("Città",u["city"])

    if u["city"]:
        st.markdown("### Locker vicino a te")
        st.write(get_lockers(u["city"]))

    st.session_state.user = u

# =========================
# CARRELLO (AMAZON STYLE)
# =========================
elif st.session_state.page == "Carrello":

    st.markdown("## 🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["name"],item["price"],"€")

        with c2:
            if st.button("❌",key=i):
                st.session_state.cart.pop(i)
                st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# INFO (BUSINESS)
# =========================
elif st.session_state.page == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    LoopBaby è un sistema, non uno shop.

    📦 1. Ricevi Box  
    ⏱️ 2. Usi per 90 giorni  

    ⚠️ entro 2 giorni puoi segnalare problemi  

    🔁 dopo 90 giorni:
    - nuova Box (gratis ritiro)
    - oppure restituzione (7,90€)

    ♻️ Patto del 10:
    10 capi = nuova Box o sostituzione
    """)

# =========================
# CHI SIAMO (BRAND)
# =========================
elif st.session_state.page == "Chi Siamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    LoopBaby non è un e-commerce.

    È uno stile. Una scelta. Un sistema.

    🌍 Nata da un problema reale:

    - vestiti costosi  
    - crescita veloce  
    - spreco enorme  

    ♻️ Soluzione:

    un sistema circolare dove i vestiti vivono più vite.

    🎯 Missione:

    rendere l’abbigliamento bambino sostenibile e intelligente.
    """)

# =========================
# CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.markdown("## 📞 Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 3921404637 (WhatsApp)")

    if st.button("Apri WhatsApp"):
        whatsapp()

# =========================
# APP DOWNLOAD (SIMULATO)
# =========================
elif st.session_state.page == "App":

    st.markdown("## 📲 App LoopBaby")

    st.markdown("Scarica la nostra app:")

    if st.button("Android"):
        st.info("Link Play Store / APK")

    if st.button("iPhone"):
        st.info("Link App Store")
