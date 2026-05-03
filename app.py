import streamlit as st
import os
import json
import base64
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
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
# DB LOCAL
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
    st.session_state.page = "Login"

if "menu" not in st.session_state:
    st.session_state.menu = False

def go(p):
    st.session_state.page = p
    st.rerun()

# =========================
# STYLE PREMIUM BEIGE (ZALANDO STYLE CLEAN)
# =========================
st.markdown("""
<style>
.stApp{
    background:#f5efe6;
    max-width:520px;
    margin:auto;
    font-family:Arial;
}

/* HEADER */
.header{
    text-align:center;
    font-size:30px;
    font-weight:900;
    color:#2b2b2b;
    margin-top:10px;
}

.sub{
    text-align:center;
    font-size:13px;
    color:#6b6258;
}

/* CARD */
.card{
    background:white;
    border-radius:16px;
    padding:16px;
    margin:10px 0;
    border:1px solid #e8dfd2;
}

/* BUTTON */
div.stButton > button{
    background:#f4b400 !important;
    color:black !important;
    width:100%;
    border-radius:12px;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER LOGO
# =========================
if logo:
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{logo}' width='160'></div>",
        unsafe_allow_html=True
    )

# =========================
# LOGIN / REGISTER (FIX EMAIL UNIQUE)
# =========================
if st.session_state.page == "Login":

    st.markdown("<div class='header'>LoopBaby</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Sistema circolare per bambini</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):

            r = requests.get(API_URL, params={"email": email}).json()

            if not r:
                st.error("Utente non trovato")
            elif r[0].get("password") != password:
                st.error("Password errata")
            else:
                st.session_state.dati = r[0]
                go("Home")

    # REGISTER
    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        telefono = st.text_input("Telefono")
        password_r = st.text_input("Password", type="password")

        if st.button("Registrati"):

            check = requests.get(API_URL, params={"email": email_r}).json()

            if check:
                st.error("Email già registrata")
            else:
                payload = {
                    "data": {
                        "nome": nome,
                        "email": email_r,
                        "telefono": telefono,
                        "password": password_r
                    }
                }

                requests.post(API_URL, json=payload)
                st.success("Registrazione completata")
                st.rerun()

    st.stop()

# =========================
# USER HEADER
# =========================
user = st.session_state.dati
nome = user.get("nome", "")

st.markdown(f"<div class='header'>Ciao {nome} 👋</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Benvenuto in LoopBaby</div>", unsafe_allow_html=True)

# =========================
# NAV BAR (SEMPLICE MA COMPLETA)
# =========================
c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    if st.button("Home"): go("Home")
with c2:
    if st.button("Box"): go("Box")
with c3:
    if st.button("Vetrina"): go("Vetrina")
with c4:
    if st.button("Info"): go("Info")
with c5:
    if st.button("Profilo"): go("Profilo")

# =========================
# HOME (PULITA + BRAND)
# =========================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="card">
    <b>LoopBaby è un sistema circolare per la crescita del bambino.</b><br><br>
    Non compri tutto subito.<br>
    Usi solo ciò che serve mentre cresce.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    ♻️ zero sprechi<br>
    👶 crescita continua<br>
    💛 risparmio reale<br>
    📦 sistema intelligente
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="background:#fff1f2">
    <b>🔥 Mamme Fondatrici</b><br>
    Dona 10+ capi → Box omaggio
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX (TUO SISTEMA ORIGINALE MIGLIORATO)
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    boxes = [
        ("SOLE ☀️", "#FFD600"),
        ("LUNA 🌙", "#E5E7EB"),
        ("NUVOLA ☁️", "#94A3B8")
    ]

    for name, color in boxes:

        st.markdown(f"""
        <div class="card" style="background:{color}">
        <b>{name}</b><br>
        14,90€
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name": name, "price": 14.90})

    st.markdown("""
    <div class="card" style="background:#4F46E5;color:white">
    <b>BOX PREMIUM 💎</b><br>
    24,90€
    </div>
    """, unsafe_allow_html=True)

    if st.button("Aggiungi Premium"):
        st.session_state.cart.append({"name": "Premium", "price": 24.90})

# =========================
# VETRINA (PRODOTTI TUOI)
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
    <div class="card">
    Questi capi rimangono tuoi per sempre.<br>
    Spedizione: GRATIS sopra 50€ o con Box / 7,90€ standard
    </div>
    """, unsafe_allow_html=True)

    products = [
        ("Body cotone bio", 9.90),
        ("Tutina soft", 12.90),
        ("Set notte", 14.90)
    ]

    for n,p in products:
        st.markdown(f"<div class='card'><b>{n}</b><br>{p}€</div>", unsafe_allow_html=True)

        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": p})

# =========================
# INFO (TUO TESTO MIGLIORATO SOLO FLUIDO)
# =========================
if st.session_state.page == "Info":

    st.title("ℹ️ Come funziona LoopBaby")

    st.markdown("""
<div class="card">
♻️ LoopBaby è un sistema circolare<br><br>

📦 Ricevi Box → usi → cambi quando cresce<br>
⏱ controllo qualità 48h<br>
🔄 ciclo continuo senza sprechi<br><br>

🚚 Spedizione:
- GRATIS sopra 50€
- GRATIS con Box
- 7,90€ standard
</div>
""", unsafe_allow_html=True)

# =========================
# PROFILO (COMPLETO E SALVABILE)
# =========================
if st.session_state.page == "Profilo":

    st.title("👤 Profilo")

    user["nome"] = st.text_input("Nome", user.get("nome",""))
    user["email"] = st.text_input("Email", user.get("email",""))
    user["telefono"] = st.text_input("Telefono", user.get("telefono",""))
    user["bimbo"] = st.text_input("Nome bambino", user.get("bimbo",""))

    if st.button("Salva"):
        st.session_state.dati = user
        save(user)
        st.success("Profilo salvato")

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
