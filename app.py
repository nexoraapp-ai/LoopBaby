import streamlit as st
import json
import os

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# STYLE (BEIGE CLEAN APP)
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
.title {
    font-size: 26px;
    font-weight: 800;
}
.subtitle {
    color: #555;
    font-size: 14px;
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
# AUTH
# =========================
if not st.session_state.user:

    st.markdown("<div class='title'>LoopBaby</div>", unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":

        nome = st.text_input("Nome")
        telefono = st.text_input("Telefono")
        bimbo = st.text_input("Nome bambino")

        if st.button("Crea account"):
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
                st.success("Account creato")
                st.session_state.user = db[email]
                st.session_state.user["email"] = email
                st.rerun()

    else:
        if st.button("Entra"):
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
    st.markdown("<b>LoopBaby</b>", unsafe_allow_html=True)

if st.session_state.menu:
    st.button("🏠 Home", on_click=lambda: go("Home"))
    st.button("📦 Box", on_click=lambda: go("Box"))
    st.button("🛍️ Vetrina", on_click=lambda: go("Vetrina"))
    st.button("🔥 Promo", on_click=lambda: go("Promo"))
    st.button("ℹ️ Info", on_click=lambda: go("Info"))
    st.button("❤️ Chi siamo", on_click=lambda: go("Chi"))
    st.button("👤 Profilo", on_click=lambda: go("Profilo"))
    st.button("🛒 Carrello", on_click=lambda: go("Carrello"))

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user

    st.markdown(f"## 👋 Ciao **{u.get('nome','')}**")

    st.markdown("""
LoopBaby non è un e-commerce.

È un sistema circolare intelligente per vestire il tuo bambino senza sprechi.
""")

    st.markdown("""
♻️ riuso intelligente  
🔄 crescita circolare  
💛 risparmio reale  
""")

    st.markdown("### 🔥 Mamme Fondatrici")

    if st.checkbox("Diventa mamma fondatrice"):
        u["fondatrice"] = True
        db[u["email"]] = u
        save_db(db)
        st.success("Sei nel programma fondatrici")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.markdown("## 📦 Box")

    tipo = st.radio("Tipo", ["Standard", "Premium"])

    if tipo == "Standard":

        st.markdown("### 14,90€")

        for i, b in enumerate(["SOLE", "LUNA", "NUVOLA"]):
            st.markdown(f"<div class='card'><b>{b}</b><br><span class='subtitle'>Box standard</span></div>", unsafe_allow_html=True)

            if st.button(f"Aggiungi {b}", key=f"box_{i}"):
                st.session_state.cart.append({"name": b, "price": 14.90})

    else:

        st.markdown("<div class='card'><b>Premium</b><br>24,90€</div>", unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name": "Premium", "price": 24.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.markdown("## 🛍️ Vetrina")

    st.markdown("""
Questi capi rimangono a te per sempre.

🚚 GRATIS sopra 50€  
📦 GRATIS con Box  
🚚 7,90€ senza Box  
""")

    prodotti = [
        ("Body", 9.90),
        ("Tutina", 12.90),
        ("Completo", 19.90)
    ]

    for i, p in enumerate(prodotti):
        st.markdown(f"<div class='card'><b>{p[0]}</b><br>{p[1]}€</div>", unsafe_allow_html=True)

        if st.button(f"Aggiungi {p[0]}", key=f"prod_{i}"):
            st.session_state.cart.append({"name": p[0], "price": p[1]})

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for i, item in enumerate(st.session_state.cart):
        c1, c2, c3 = st.columns([3,1,1])

        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        totale += item["price"]

    st.markdown(f"### Totale: {totale}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    u = st.session_state.user

    st.markdown("## 👤 Profilo")

    u["nome"] = st.text_input("Nome", u.get("nome",""))
    u["telefono"] = st.text_input("Telefono", u.get("telefono",""))
    u["bimbo"] = st.text_input("Bambino", u.get("bimbo",""))

    if st.button("Salva"):
        db[u["email"]] = u
        save_db(db)
        st.success("Dati aggiornati")

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.markdown("## ℹ️ Come funziona")

    st.markdown("""
Ricevi una Box → usi i capi → li cambi quando il bambino cresce.

⏳ Durata: 90 giorni  
🔄 Cambio libero  

🚚 Spedizione:
- GRATIS con Box
- 7,90€ se interrompi
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "Chi":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
Siamo genitori.

LoopBaby nasce per eliminare sprechi e semplificare la vita alle famiglie.

I bambini crescono troppo in fretta:
noi abbiamo creato un sistema per usare i vestiti nel momento giusto.
""")
