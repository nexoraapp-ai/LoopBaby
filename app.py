import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# IMMAGINI
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = load_img("logo.png")
baby = load_img("bimbo.jpg")

# =========================
# DB
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome":"", "email":"", "telefono":"",
        "bimbo":"", "taglia":"50-56",
        "paese":"Italia","citta":"","locker":""
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
# LOCKER (MIGLIORATO)
# =========================
LOCKERS = {
    "Italia": {
        "Milano": ["Milano Centrale","Porta Romana"],
        "Lecco": ["Calolziocorte","Lecco Centro"],
        "Roma": ["Termini","Tiburtina"],
        "Palermo": ["Palermo Centro"],
        "Catania": ["Catania Centrale"],
        "Canicattì": ["Canicattì Hub"],
        "Giffone": ["Reggio Calabria Locker"]
    }
}

def locker_ui():
    paese = st.selectbox("Paese", list(LOCKERS.keys()))
    citta = st.selectbox("Città", list(LOCKERS[paese].keys()))
    locker = st.selectbox("Locker", LOCKERS[paese][citta])
    return paese, citta, locker

# =========================
# SIDEBAR (HAMBURGER)
# =========================
with st.sidebar:
    if logo:
        st.image("logo.png", width=130)

    st.button("🏠 Home", on_click=lambda: go("Home"))
    st.button("📦 Box", on_click=lambda: go("Box"))
    st.button("🛍️ Vetrina", on_click=lambda: go("Vetrina"))
    st.button("ℹ️ Info", on_click=lambda: go("Info"))
    st.button("🔥 Promo", on_click=lambda: go("Promo"))
    st.button("👤 Profilo", on_click=lambda: go("Profilo"))
    st.button("🛒 Carrello", on_click=lambda: go("Carrello"))

    st.markdown("---")
    st.markdown("📞 WhatsApp: https://wa.me/393921404637")
    st.markdown("✉️ assistenza.loopbaby@gmail.com")

# =========================
# HEADER LOGO (SOLO LOGO)
# =========================
if logo:
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{logo}' width='170'></div>",
        unsafe_allow_html=True
    )

# =========================
# HOME (FIX COMPLETO)
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

    st.markdown("""
### 🔥 Promo Mamme Fondatrici
Dona 10 capi → ricevi BOX OMAGGIO
""")

    if st.button("Partecipa alla promo"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("Promo Mamme Fondatrici")

    st.markdown("""
**Cos’è:**
Un programma speciale per mamme fondatrici.

🎁 Doni 10 capi  
📦 Ricevi Box gratuita  
🚚 Spedizione inclusa  
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    paese, citta, locker = locker_ui()

    if st.button("Invia richiesta"):
        st.success("Entro 48h riceverai etichetta via email/WhatsApp")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box LoopBaby")

    tipo = st.radio("Scegli tipo", ["Standard","Premium"])

    if tipo == "Standard":

        st.markdown("### Box Standard 14,90€ (spedizione inclusa)")

        boxes = [
            ("SOLE ☀️","giallo"),
            ("LUNA 🌙","grigio"),
            ("NUVOLA ☁️","blu")
        ]

        for name,color in boxes:
            st.markdown(f"""
            <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0">
                <b>{name}</b><br>
                capi usati in ottimo stato
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}"):
                st.session_state.cart.append({"name":name,"price":14.90})

    else:

        st.markdown("""
        <div style="background:#4F46E5;color:white;padding:15px;border-radius:15px">
        <b>BOX PREMIUM 💎</b><br>
        capi nuovi o seminuovi - 24,90€
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name":"Premium","price":24.90})

# =========================
# INFO (COMPLETO VERO SISTEMA)
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona LoopBaby")

    st.markdown("""
LoopBaby è un sistema:

📦 Ricevi Box  
👶 Usi i capi  

⏱ 10 giorni: controllo qualità  
♻️ Patto del 10: equilibrio circolare  

Dopo 90 giorni:
- nuova taglia (ritiro gratis)
- oppure restituzione (7,90€)

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(str(item["price"])+"€")

        if c3.button("❌",key=i):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    d = st.session_state.dati

    st.title("Profilo")

    d["nome"] = st.text_input("Nome", d["nome"])
    d["email"] = st.text_input("Email", d["email"])
    d["telefono"] = st.text_input("Telefono", d["telefono"])
    d["bimbo"] = st.text_input("Bambino", d["bimbo"])

    d["paese"], d["citta"], d["locker"] = locker_ui()

    if st.button("Salva"):
        save(d)
        st.success("Salvato")

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.markdown("""
I capi restano tuoi per sempre.

🚚 spedizione gratuita sopra 50€
""")

    if st.button("Aggiungi capo 9.90€"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp: https://wa.me/393921404637 | ✉️ assistenza.loopbaby@gmail.com")
