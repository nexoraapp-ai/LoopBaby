import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# DATA
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {"nome": ""}

def save(d):
    json.dump(d, open(DB_FILE,"w"))

if "dati" not in st.session_state:
    st.session_state.dati = load()

if "page" not in st.session_state:
    st.session_state.page = "home"

if "menu" not in st.session_state:
    st.session_state.menu = False

if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p
    st.session_state.menu = False
    st.rerun()

# =========================
# STYLE (COERENTE)
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
    font-family: sans-serif;
}

/* HEADER */
.header{
    text-align:center;
    font-size:28px;
    font-weight:900;
    color:#5a4636;
    margin-top:10px;
}

/* HAMBURGER */
.hamb{
    font-size:30px;
    background:#5a4636;
    color:white;
    border-radius:10px;
}

/* CARD */
.card{
    background:#fffdf8;
    padding:15px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #e6dccd;
}

/* BUTTON */
div.stButton > button{
    background:#f4b400;
    color:black;
    border-radius:12px;
    width:100%;
    font-weight:700;
}

/* MENU OVERLAY */
.menu{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:#00000055;
    z-index:999;
}
.menu-box{
    background:white;
    width:80%;
    margin:80px auto;
    padding:20px;
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1,col2 = st.columns([8,1])

with col1:
    st.markdown("<div class='header'>🌸 LoopBaby</div>", unsafe_allow_html=True)

with col2:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

# =========================
# MENU OVERLAY (VERO)
# =========================
if st.session_state.menu:

    st.markdown("""
    <div class="menu">
        <div class="menu-box">
    """, unsafe_allow_html=True)

    if st.button("🏠 Home"): go("home")
    if st.button("📦 Box"): go("box")
    if st.button("🛍️ Vetrina"): go("vetrina")
    if st.button("ℹ️ Info"): go("info")
    if st.button("🌸 Mamme Fondatrici"): go("promo")
    if st.button("👤 Profilo"): go("profilo")
    if st.button("🛒 Carrello"): go("carrello")

    st.markdown("</div></div>", unsafe_allow_html=True)

# =========================
# HOME (ORA FATTA BENE)
# =========================
if st.session_state.page == "home":

    n = st.session_state.dati.get("nome","")

    st.markdown(f"## Ciao {n if n else 'benvenuto'} 👋")

    st.markdown("""
<div class="card">
<b>LoopBaby è un sistema, non un negozio.</b><br><br>
✔ crescita circolare<br>
✔ meno sprechi<br>
✔ vestiti che ruotano con il bambino<br>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card" style="background:#fff1f2">
<b>🌸 Mamme Fondatrici</b><br>
Accedi al sistema esclusivo LoopBaby
</div>
""", unsafe_allow_html=True)

# =========================
# PROMO
# =========================
if st.session_state.page == "promo":

    st.title("🌸 Mamme Fondatrici")

    st.markdown("""
✔ dona 10 capi  
✔ ricevi box gratuita  
✔ spedizione inclusa  
""")

# =========================
# BOX (COLORI GIUSTI)
# =========================
if st.session_state.page == "box":

    st.title("📦 Box")

    boxes = [
        ("SOLE ☀️", "#FFD600"),
        ("LUNA 🌙", "#E5E7EB"),
        ("NUVOLA ☁️", "#94A3B8")
    ]

    for name,color in boxes:
        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0">
        <b>{name}</b>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name":name,"price":14.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
✔ capi tuoi per sempre  
🚚 spedizione gratuita sopra 50€ o con box  
💸 altrimenti 7,90€
""")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "info":

    st.title("ℹ️ Info")

    st.markdown("""
✔ Box gratis andata  
✔ 90 giorni utilizzo  
✔ ritorno gratuito con Box  
✔ 7,90€ senza Box  
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "carrello":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")
        if c3.button("❌",key=i):
            st.session_state.cart.pop(i)
            st.rerun()
        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "profilo":

    st.title("👤 Profilo")

    d = st.session_state.dati

    d["nome"] = st.text_input("Nome",d.get("nome",""))

    if st.button("Salva"):
        save(d)
        st.success("Salvato")
