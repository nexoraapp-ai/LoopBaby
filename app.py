import streamlit as st
import os
import json
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# STILE (BEIGE ZALANDO-LIKE)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F5F1E8;
    max-width: 520px;
    margin: auto;
}
button {
    border-radius: 12px !important;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
DB_FILE = "db.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            return json.load(open(DB_FILE))
        except:
            return []
    return []

def save_users(data):
    json.dump(data, open(DB_FILE, "w"))

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
# HEADER
# =========================
col1, col2 = st.columns([1, 6])

with col1:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

with col2:
    st.markdown("## 🟡 LoopBaby")

# MENU
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
# LOGIN / REGISTER (FIX DUPLICATI)
# =========================
if not st.session_state.user:

    st.title("LoopBaby")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    users = load_users()

    # -------------------------
    # LOGIN
    # -------------------------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Accedi"):
            found = None
            for u in users:
                if u.get("email") == email and u.get("password") == password:
                    found = u
                    break

            if found:
                st.session_state.user = found
                st.rerun()
            else:
                st.error("Credenziali errate")

    # -------------------------
    # REGISTER
    # -------------------------
    with tab2:
        nome = st.text_input("Nome", key="reg_nome")
        email_r = st.text_input("Email", key="reg_email")
        telefono = st.text_input("Telefono", key="reg_tel")
        password_r = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Registrati"):
            if any(u.get("email") == email_r for u in users):
                st.error("Email già registrata")
            else:
                new_user = {
                    "nome": nome,
                    "email": email_r,
                    "telefono": telefono,
                    "password": password_r,
                    "nome_bimbo": "",
                    "taglia": "50-56",
                    "via": "",
                    "citta": "",
                    "cap": "",
                    "note": ""
                }
                users.append(new_user)
                save_users(users)

                st.session_state.user = new_user
                st.rerun()

    st.stop()

# =========================
# HOME (ZALANDO STYLE)
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user

    st.markdown(f"## 👋 Ciao {u.get('nome','')}")

    st.markdown("""
### LoopBaby System

♻️ crescita circolare  
🔄 riuso intelligente  
💛 risparmio reale  
👶 crescita senza sprechi  
""")

    st.markdown("""
<div style="background:#fff;padding:16px;border-radius:16px;">
<b>🔥 Mamme Fondatrici</b><br>
Dona 10 capi → Box gratuita + spedizione inclusa
</div>
""", unsafe_allow_html=True)

    if st.button("Partecipa"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("Mamme Fondatrici")

    st.markdown("""
🎁 Dona 10 capi  
📦 Box gratuita  
🚚 Etichetta in 48h  
""")

    peso = st.text_input("Peso pacco", key="peso")
    dim = st.text_input("Dimensioni", key="dim")

    if st.button("Invia"):
        st.success("Etichetta inviata entro 48h")

# =========================
# BOX (STANDARD + PREMIUM)
# =========================
if st.session_state.page == "Box":

    st.title("Box LoopBaby")

    tipo = st.radio("Scegli", ["Standard", "Premium"])

    taglia = st.session_state.user.get("taglia", "50-56")

    if tipo == "Standard":

        st.markdown("### 🧸 Standard 14,90€")
        st.markdown("Capi usati in buono stato")

        boxes = [
            ("SOLE ☀️", "#FFD600"),
            ("LUNA 🌙", "#E5E7EB"),
            ("NUVOLA ☁️", "#94A3B8")
        ]

        for i, (name, color) in enumerate(boxes):
            st.markdown(f"""
            <div style="background:{color};padding:14px;border-radius:12px;margin:10px 0;">
            {name}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}", key=f"s{i}"):
                st.session_state.cart.append({"name": f"{name} Box {taglia}", "price": 14.90})

    else:

        st.markdown("### 💎 Premium 24,90€")
        st.markdown("Capi nuovi o seminuovi")

        st.markdown("""
        <div style="background:#6D28D9;color:white;padding:16px;border-radius:16px;">
        BOX PREMIUM ZALANDO STYLE ✨
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name": f"Premium Box {taglia}", "price": 24.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.markdown("""
I capi restano tuoi.

🚚 spedizione:
- gratis sopra 50€
- 7,90€ standard
""")

    if st.button("Aggiungi Body 9.90€"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona")

    st.markdown("""
Ricevi Box → usi → restituisci → continui

⏳ ciclo: 90 giorni

♻️ Patto 10x10:
10 capi → 10 capi indietro

Se rompi:
- jeans x jeans
- oppure 5€ a capo
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "Chi":

    st.title("Chi siamo")

    st.markdown("""
LoopBaby è un sistema, non un negozio.

Riduce sprechi, aumenta riuso.

✔ sostenibile  
✔ intelligente  
✔ continuo  
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    total = 0

    for i, item in enumerate(st.session_state.cart):
        c1, c2, c3 = st.columns([3,1,1])

        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=f"c{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")

# =========================
# PROFILO (ROBUSTO + ZALANDO STYLE)
# =========================
if st.session_state.page == "Profilo":

    u = st.session_state.user
    users = load_users()

    st.title("Profilo")

    st.markdown(f"### Ciao {u.get('nome','')}")

    u["nome"] = st.text_input("Nome", u.get("nome",""))
    u["telefono"] = st.text_input("Telefono", u.get("telefono",""))

    st.subheader("Bambino")
    u["nome_bimbo"] = st.text_input("Nome bimbo", u.get("nome_bimbo",""))
    u["taglia"] = st.selectbox("Taglia", ["50-56","62-68","74-80","86-92"])

    st.subheader("Indirizzo")
    u["via"] = st.text_input("Via", u.get("via",""))
    u["citta"] = st.text_input("Città", u.get("citta",""))
    u["cap"] = st.text_input("CAP", u.get("cap",""))

    u["note"] = st.text_area("Note", u.get("note",""))

    if st.button("Salva profilo"):

        for i in range(len(users)):
            if users[i].get("email") == u.get("email"):
                users[i] = u

        save_users(users)
        st.session_state.user = u

        st.success("Profilo salvato")
