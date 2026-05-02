import streamlit as st
import os
import json
import base64

# =========================
# SETUP
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# ASSETS
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = load_img("logo.png")
baby = load_img("bimbo.jpg")

# =========================
# DB PROFILO
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
        "paese":"Italia",
        "citta":"",
        "locker":""
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
# LOCKER DATABASE
# =========================
LOCKERS = {
    "Italia": {
        "Milano": ["Milano Centrale", "Porta Romana"],
        "Lecco": ["Calolziocorte", "Lecco Centro"],
        "Roma": ["Termini", "Tiburtina"]
    }
}

def locker_system():
    paese = st.selectbox("Paese", list(LOCKERS.keys()))
    citta = st.selectbox("Città", list(LOCKERS[paese].keys()))
    locker = st.selectbox("Locker", LOCKERS[paese][citta])
    return paese, citta, locker

# =========================
# SIDEBAR (HAMBURGER MENU)
# =========================
with st.sidebar:
    st.image("logo.png", width=140)

    if st.button("🏠 Home"): go("Home")
    if st.button("📦 Box"): go("Box")
    if st.button("🛍️ Vetrina"): go("Vetrina")
    if st.button("ℹ️ Info"): go("Info")
    if st.button("🔥 Promo"): go("Promo")
    if st.button("👤 Profilo"): go("Profilo")
    if st.button("🛒 Carrello"): go("Carrello")

    st.markdown("---")
    st.markdown("📞 WhatsApp: https://wa.me/393921404637")
    st.markdown("✉️ assistenza.loopbaby@gmail.com")

# =========================
# LOGO HEADER
# =========================
st.image("logo.png", width=180)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    d = st.session_state.dati
    nome = d.get("nome","")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"## Ciao {nome or '👋'}")
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
    if st.button("Accedi alla promo"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("Promo Mamme Fondatrici")

    st.markdown("Dona 10 capi → ricevi BOX OMAGGIO")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    paese, citta, locker = locker_system()

    if st.button("Invia richiesta"):
        st.success("Entro 48h riceverai etichetta")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box LoopBaby")

    tipo = st.radio("Seleziona", ["Standard","Premium"])

    if tipo == "Standard":

        boxes = [
            ("SOLE ☀️", "#FFD600"),
            ("LUNA 🌙", "#E5E7EB"),
            ("NUVOLA ☁️", "#94A3B8")
        ]

        for name,color in boxes:
            st.markdown(f"""
            <div style="background:{color};padding:15px;border-radius:20px;margin:10px 0">
            <b>{name}</b><br>
            14,90€ spedizione inclusa
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}"):
                st.session_state.cart.append({"name":name,"price":14.90})

    else:

        st.markdown("""
        <div style="background:#4F46E5;color:white;padding:15px;border-radius:20px">
        <b>BOX PREMIUM 💎</b><br>
        24,90€ capi nuovi/semi nuovi
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name":"Premium","price":24.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.markdown("""
I capi acquistati restano per sempre.

🚚 Spedizione:
- gratuita sopra 50€
- oppure con Box
""")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body Bio","price":9.90})

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        col1,col2,col3 = st.columns([3,1,1])
        col1.write(item["name"])
        col2.write(str(item["price"])+"€")

        if col3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

    if st.button("Checkout (domani)"):
        st.success("Pagamento da integrare")

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona")

    st.markdown("""
LoopBaby è un sistema:

1. Ricevi Box
2. Usi capi
3. Dopo 90 giorni:
   - nuova taglia
   - restituzione

⏱ 10 giorni: controllo qualità  
♻️ Patto del 10: equilibrio circolare
""")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    d = st.session_state.dati

    st.title("Profilo")

    d["nome"] = st.text_input("Nome", d["nome"])
    d["email"] = st.text_input("Email", d["email"])
    d["telefono"] = st.text_input("Telefono", d["telefono"])
    d["bimbo"] = st.text_input("Nome bambino", d["bimbo"])
    d["taglia"] = st.selectbox("Taglia", ["50-56","62-68","74-80","86-92"])

    d["paese"], d["citta"], d["locker"] = locker_system()

    if st.button("Salva"):
        save(d)
        st.success("Profilo salvato")

# =========================
# FOOTER INFO
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp: https://wa.me/393921404637 | ✉️ assistenza.loopbaby@gmail.com")
