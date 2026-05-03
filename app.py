import streamlit as st
import json
import os
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# IMMAGINE LOGO
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path, "rb").read()).decode()
    return ""

logo = load_img("logo.png")

# =========================
# STILE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F5F1E8;
    max-width: 430px;
    margin: auto;
}
button {
    border-radius: 14px !important;
    font-weight: 600 !important;
}
.card {
    background: white;
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 12px;
    border: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
def load_db():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {}

def save_db(db):
    json.dump(db, open(DB_FILE, "w"))

db = load_db()

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "menu" not in st.session_state:
    st.session_state.menu = False

def go(p):
    st.session_state.page = p
    st.session_state.menu = False

# =========================
# LOGIN / REGISTRAZIONE
# =========================
if not st.session_state.user:

    if logo:
        st.markdown(f"<div style='text-align:center'><img src='data:image/png;base64,{logo}' width='180'></div>", unsafe_allow_html=True)

    st.title("LoopBaby")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        nome = st.text_input("Nome")
        telefono = st.text_input("Telefono")
        bimbo = st.text_input("Nome bambino")

        if st.button("Registrati"):
            if email in db:
                st.error("Email già registrata")
            else:
                db[email] = {
                    "password": password,
                    "nome": nome,
                    "telefono": telefono,
                    "bimbo": bimbo,
                    "fondatrice": False
                }
                save_db(db)
                st.session_state.user = db[email]
                st.session_state.user["email"] = email
                st.rerun()

    else:
        if st.button("Login"):
            if email in db and db[email]["password"] == password:
                st.session_state.user = db[email]
                st.session_state.user["email"] = email
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()

# =========================
# HEADER + MENU
# =========================
col1, col2 = st.columns([1,5])

with col1:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

with col2:
    if logo:
        st.markdown(f"<img src='data:image/png;base64,{logo}' width='120'>", unsafe_allow_html=True)

if st.session_state.menu:
    st.button("Home", on_click=lambda: go("Home"))
    st.button("Box", on_click=lambda: go("Box"))
    st.button("Vetrina", on_click=lambda: go("Vetrina"))
    st.button("Promo", on_click=lambda: go("Promo"))
    st.button("Info", on_click=lambda: go("Info"))
    st.button("Chi siamo", on_click=lambda: go("Chi"))
    st.button("Profilo", on_click=lambda: go("Profilo"))
    st.button("Carrello", on_click=lambda: go("Carrello"))

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user

    st.markdown(f"## 👋 Ciao **{u.get('nome','')}**")

    st.markdown("""
**LoopBaby non è un e-commerce. È un sistema circolare.**

👶 vestiti sempre della taglia giusta  
♻️ crescita circolare intelligente  
🔄 riuso senza sprechi  
💛 risparmio reale ogni mese  
📦 zero pensieri  
""")

    st.markdown("### 🔥 Mamme Fondatrici")

    st.markdown("""
🎁 Dona almeno 10 capi  
📦 Ricevi una Box gratuita  
🚚 Spedizione inclusa  
♻️ Entri nel sistema LoopBaby  
""")

    if st.button("Partecipa ora"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("🔥 Mamme Fondatrici")

    st.markdown("""
1. Prepara almeno 10 capi  
2. Inserisci i dati  
3. Ricevi etichetta entro 48h  
4. Spedisci gratis  
5. Ricevi Box  
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")
    locker = st.text_input("Locker preferito")

    if st.button("Invia richiesta"):
        st.success("✔ Etichetta inviata entro 48h")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    st.markdown("### Standard 14,90€")

    boxes = [
        ("SOLE ☀️", "#FFD600"),
        ("LUNA 🌙", "#E5E7EB"),
        ("NUVOLA ☁️", "#94A3B8")
    ]

    for i, (name, color) in enumerate(boxes):
        st.markdown(f"<div style='background:{color};padding:15px;border-radius:15px'>{name}</div>", unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}", key=f"b{i}"):
            st.session_state.cart.append({"name": name, "price": 14.90})

    st.markdown("### Premium 24,90€")

    if st.button("Aggiungi Premium"):
        st.session_state.cart.append({"name": "Premium", "price": 24.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
I capi acquistati qui rimangono a te.

🚚 Spedizione:
- GRATIS sopra 50€
- GRATIS con Box
- 7,90€ senza Box
""")

    if st.button("Aggiungi Body 9,90€"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("🛒 Carrello")

    total = 0

    for i, item in enumerate(st.session_state.cart):
        c1, c2, c3 = st.columns([3,1,1])

        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=f"del{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    u = st.session_state.user

    st.title("👤 Profilo")

    u["nome"] = st.text_input("Nome", u.get("nome",""))
    u["telefono"] = st.text_input("Telefono", u.get("telefono",""))
    u["bimbo"] = st.text_input("Bambino", u.get("bimbo",""))

    if st.button("Salva"):
        db[u["email"]] = u
        save_db(db)
        st.success("Salvato")

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("ℹ️ Come funziona LoopBaby")

    st.markdown("""
📦 Ricevi la Box  
👶 Usi i capi fino a 90 giorni  
🔄 Cambi quando cresce  

🚚 Spedizione:
- GRATIS se continui
- 7,90€ se interrompi  

♻️ Patto 10x10:
Ricevi 10 capi → restituisci 10 capi  
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "Chi":

    st.title("❤️ Chi siamo")

    st.markdown("""
Siamo genitori.

LoopBaby nasce per ridurre sprechi e semplificare la vita.

I bambini crescono troppo velocemente:
noi abbiamo creato un sistema per usare i vestiti nel momento giusto.
""")
