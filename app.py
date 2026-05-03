import streamlit as st
import os
import json
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# STYLE (BEIGE UNIFORME)
# =========================
st.markdown("""
<style>
.stApp {
    background-color:#F5F1E8;
    max-width:520px;
    margin:auto;
}

button {
    border-radius:12px !important;
    font-weight:600 !important;
}

[data-testid="stSidebar"] {
    background:#efe7da;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
def load_users():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return []

def save_users(data):
    json.dump(data, open(DB_FILE, "w"))

users = load_users()

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
# HEADER + HAMBURGER
# =========================
col1, col2 = st.columns([1,6])

with col1:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

with col2:
    st.title("LoopBaby 🌿")

# MENU
if st.session_state.menu:
    st.button("Home", on_click=lambda: go("Home"))
    st.button("Box", on_click=lambda: go("Box"))
    st.button("Vetrina", on_click=lambda: go("Vetrina"))
    st.button("Info", on_click=lambda: go("Info"))
    st.button("Chi siamo", on_click=lambda: go("Chi"))
    st.button("Profilo", on_click=lambda: go("Profilo"))
    st.button("Carrello", on_click=lambda: go("Carrello"))
    st.markdown("---")

# =========================
# AUTH
# =========================
def register(nome, email, password):
    for u in users:
        if u.get("email") == email:
            return False

    users.append({
        "nome": nome,
        "email": email,
        "password": password,
        "taglia": "50-56",
        "telefono": "",
        "bimbo": "",
        "indirizzo": ""
    })

    save_users(users)
    return True

def login(email, password):
    for u in users:
        if u.get("email") == email and u.get("password") == password:
            st.session_state.user = u
            return True
    return False

# =========================
# LOGIN PAGE
# =========================
if st.session_state.user is None:

    st.title("LoopBaby Login")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):
            if login(email, password):
                st.rerun()
            else:
                st.error("Errore login")

    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email")
        password_r = st.text_input("Password", type="password")

        if st.button("Registrati"):
            if register(nome, email_r, password_r):
                st.success("Registrazione ok")
            else:
                st.error("Email già registrata")

    st.stop()

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user

    st.markdown(f"## 👋 Ciao {u.get('nome','')}")

    st.markdown("""
♻️ crescita circolare  
🔄 riuso intelligente  
💛 risparmio reale  
""")

# =========================
# BOX (ZALANDO STYLE)
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    taglia = st.session_state.user.get("taglia")

    st.info(f"Taglia: {taglia}")

    tipo = st.radio("Scegli", ["Standard", "Premium"], horizontal=True)

    # STANDARD
    if tipo == "Standard":

        st.subheader("🧸 Standard — 14,90€")

        boxes = [
            ("SOLE ☀️", "#FFD600", "vivaci"),
            ("LUNA 🌙", "#EDEDED", "neutri"),
            ("NUVOLA ☁️", "#C7D2FE", "soft")
        ]

        for i, (name, color, desc) in enumerate(boxes):

            st.markdown(f"""
            <div style="
                background:{color};
                padding:14px;
                border-radius:12px;
                margin:8px 0;
            ">
                <b>{name}</b><br>{desc}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}", key=f"s{i}"):
                st.session_state.cart.append((f"Box {name}", 14.90))

    # PREMIUM
    else:

        st.subheader("💎 Premium — 24,90€")

        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#0f172a,#4f46e5);
            color:white;
            padding:18px;
            border-radius:14px;
            text-align:center;
        ">
        ✨ SELEZIONE PREMIUM<br>
        qualità superiore
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append(("Box Premium", 24.90))

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    st.write("I capi rimangono tuoi per sempre")

    st.write("""
🚚 Spedizione:
- gratis sopra 50€
- 7,90€ sotto
""")

    if st.button("Aggiungi Body 9,90€"):
        st.session_state.cart.append(("Body", 9.90))

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona")

    st.write("""
Ricevi Box → usi → restituisci → continui

♻️ Patto 10x10:
10 capi → 10 capi o 5€ a capo mancante

Durata: 90 giorni
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "Chi":

    st.title("Chi siamo")

    st.write("""
LoopBaby nasce per un problema reale:

bambini crescono troppo velocemente.

✔ meno sprechi  
✔ più riuso  
✔ più risparmio  

Non vendiamo vestiti.

Costruiamo un sistema.
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    total = 0

    for i, item in enumerate(st.session_state.cart):

        name, price = item
        col1, col2, col3 = st.columns([3,1,1])

        col1.write(name)
        col2.write(f"{price}€")

        if col3.button("❌", key=f"d{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += price

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo")

    u = st.session_state.user

    u["nome"] = st.text_input("Nome", u.get("nome",""))
    u["telefono"] = st.text_input("Telefono", u.get("telefono",""))
    u["taglia"] = st.selectbox("Taglia", ["50-56","62-68","74-80","86-92"])

    u["bimbo"] = st.text_input("Nome bambino", u.get("bimbo",""))

    u["indirizzo"] = st.text_area("Indirizzo", u.get("indirizzo",""))

    if st.button("Salva"):
        for i, x in enumerate(users):
            if x.get("email") == u.get("email"):
                users[i] = u

        save_users(users)
        st.success("Salvato")
