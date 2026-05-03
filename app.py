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
        return base64.b64encode(open(path, "rb").read()).decode()
    return ""

logo = load_img("logo.png")

# =========================
# DB
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome": "",
        "email": "",
        "telefono": "",
        "bimbo": "",
        "taglia": "50-56",
        "paese": "Italia",
        "citta": "",
        "locker": ""
    }

def save(d):
    json.dump(d, open(DB_FILE, "w"))

if "dati" not in st.session_state:
    st.session_state.dati = load()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

def go(p):
    st.session_state.page = p
    st.session_state.menu_open = False
    st.rerun()

# =========================
# DESIGN GLOBAL
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
}

/* BOTTONI */
div.stButton > button{
    background:#f4b400;
    color:black;
    border-radius:14px;
    width:100%;
    font-weight:700;
    border:none;
}

/* CARD */
.card{
    background:#fffdf8;
    padding:14px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #e7dfd2;
}

/* HEADER */
.header{
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#5a4636;
}

/* MENU ICON GRANDE */
.menu-btn button{
    font-size:28px !important;
    background:#5a4636 !important;
    color:white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER + HAMBURGER
# =========================
col1, col2 = st.columns([8,1])

with col1:
    if logo:
        st.image("logo.png", width=140)

with col2:
    if st.button("☰"):
        st.session_state.menu_open = not st.session_state.menu_open

# =========================
# MENU (TOGGLE VERO)
# =========================
if st.session_state.menu_open:

    st.markdown("### Navigazione")

    if st.button("🏠 Home"): go("Home")
    if st.button("📦 Box"): go("Box")
    if st.button("🛍️ Vetrina"): go("Vetrina")
    if st.button("ℹ️ Info"): go("Info")
    if st.button("🔥 Promo Mamme Fondatrici"): go("Promo")
    if st.button("👤 Profilo"): go("Profilo")
    if st.button("🛒 Carrello"): go("Carrello")

    st.markdown("---")

# =========================
# HOME (ORA FATTA BENE)
# =========================
if st.session_state.page == "Home":

    d = st.session_state.dati

    st.markdown("<div class='header'>🌸 LoopBaby</div>", unsafe_allow_html=True)

    st.markdown(f"## 👋 Ciao **{d.get('nome','benvenuto')}**")

    # MAMME FONDATRICI (IMPORTANTE)
    st.markdown("""
<div class="card" style="background:#fff1f2;border:1px solid #fda4af;">
<b>🌸 Mamme Fondatrici</b><br>
Diventa parte del primo sistema circolare per bambini in Italia
</div>
""", unsafe_allow_html=True)

    st.markdown("""
✔ crescita circolare  
✔ risparmio reale  
✔ vestiti sempre utili  
✔ zero sprechi  
""")

    if st.button("Scopri Box"):
        go("Box")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("🔥 Mamme Fondatrici")

    st.markdown("""
🎁 Dona 10+ capi  
📦 Box gratuita  
🚚 spedizione inclusa  

Diventa parte del sistema LoopBaby.
""")

    st.text_input("Peso pacco")
    st.text_input("Dimensioni")

    if st.button("Invia richiesta"):
        st.success("✔ Ti contattiamo entro 48h")

# =========================
# BOX (COLORI ORIGINALI FIXATI)
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    st.markdown("💛 Prezzo: 14,90€")

    boxes = [
        ("SOLE ☀️", "#FFD600"),
        ("LUNA 🌙", "#E5E7EB"),
        ("NUVOLA ☁️", "#94A3B8")
    ]

    for name, color in boxes:

        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0;font-weight:700">
        {name}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name": name, "price": 14.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
✔ questi capi rimangono a te  
🚚 spedizione gratuita sopra 50€ o con Box  
💰 altrimenti 7,90€
""")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("ℹ️ Come funziona")

    st.markdown("""
1. ricevi Box  
2. usi i capi  
3. cambi quando cresce  

🚚 spedizione:
- gratis Box
- gratis sopra 50€
- 7,90€ senza Box
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")
        if c3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()
        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    st.title("👤 Profilo")

    d = st.session_state.dati

    d["nome"] = st.text_input("Nome", d["nome"])
    d["email"] = st.text_input("Email", d["email"])
    d["telefono"] = st.text_input("Telefono", d["telefono"])
    d["bimbo"] = st.text_input("Bambino", d["bimbo"])

    if st.button("Salva"):
        save(d)
        st.success("✔ Salvato")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp | ✉️ assistenza@loopbaby.it")
