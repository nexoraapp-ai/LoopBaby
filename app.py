import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# STILE BEIGE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F5F1E8;
    max-width: 480px;
    margin: auto;
}
button {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# IMMAGINI
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path, "rb").read()).decode()
    return ""

logo = load_img("logo.png")

# =========================
# DB SICURO
# =========================
DB_FILE = "db.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            data = json.load(open(DB_FILE))
            if isinstance(data, list):
                return data
        except:
            pass
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
col1, col2 = st.columns([1,6])

with col1:
    if st.button("☰"):
        st.session_state.menu = not st.session_state.menu

with col2:
    if logo:
        st.markdown(f"<img src='data:image/png;base64,{logo}' width='140'>", unsafe_allow_html=True)

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
# LOGIN / REGISTER
# =========================
if not st.session_state.user:

    st.title("LoopBaby")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    users = load_users()

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):
            for u in users:
                if isinstance(u, dict) and u.get("email") == email and u.get("password") == password:
                    st.session_state.user = u
                    st.rerun()
            st.error("Credenziali errate")

    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email registrazione")
        telefono = st.text_input("Telefono")
        password_r = st.text_input("Password", type="password")

        if st.button("Registrati"):
            if any(isinstance(u, dict) and u.get("email") == email_r for u in users):
                st.error("Email già registrata")
            else:
                new_user = {
                    "nome": nome,
                    "email": email_r,
                    "telefono": telefono,
                    "password": password_r,
                    "nome_bimbo": "",
                    "taglia": "",
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
# HOME
# =========================
if st.session_state.page == "Home":

    nome = st.session_state.user.get("nome","")

    st.markdown(f"## 👋 Ciao {nome}")

    st.markdown("""
LoopBaby è un sistema circolare per vestire i bambini.

♻️ crescita circolare  
🔄 riuso intelligente  
💛 risparmio reale  
👶 meno sprechi  
""")

    st.markdown("### 🔥 Mamme Fondatrici")
    st.write("Dona almeno 10 capi → ricevi Box gratuita")

    if st.button("Partecipa"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("Mamme Fondatrici")

    st.markdown("""
Diventa fondatrice LoopBaby.

🎁 Dona 10 capi  
📦 Ricevi Box gratis  
🚚 Spedizione inclusa  

Ricevi etichetta entro 48h
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    if st.button("Invia richiesta"):
        st.success("Etichetta inviata entro 48h")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    taglia = st.session_state.dati.get("taglia", "50-56")

    st.markdown(
        f"""
        <div style="
            background:#f5f1e8;
            padding:12px 18px;
            border-radius:12px;
            font-weight:700;
            margin-bottom:15px;
        ">
            📏 Taglia attuale: {taglia}
        </div>
        """,
        unsafe_allow_html=True
    )

    tipo = st.radio("Scegli tipologia", ["Standard", "Premium"], horizontal=True)

    # =========================
    # STANDARD
    # =========================
    if tipo == "Standard":

        st.markdown("## 🧸 Box Standard — 14,90€")
        st.caption("Capi usati in buono stato, selezionati e igienizzati.")

        boxes = [
            ("SOLE ☀️", "#FFD600", "Colori vivaci e allegri"),
            ("LUNA 🌙", "#EDEDED", "Toni neutri e puliti"),
            ("NUVOLA ☁️", "#B8C0CC", "Colori soft e delicati")
        ]

        for i, (name, color, desc) in enumerate(boxes):

            st.markdown(f"""
            <div style="
                background:{color};
                padding:16px;
                border-radius:16px;
                margin:10px 0;
                color:#111827;
            ">
                <div style="font-size:18px;font-weight:800;">{name}</div>
                <div style="font-size:13px;opacity:0.8;">{desc}</div>
                <div style="margin-top:8px;font-size:12px;">
                    💰 14,90€
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"➕ Aggiungi {name}", key=f"std_{i}"):

                st.session_state.cart.append({
                    "name": f"Box Standard {name} ({taglia})",
                    "price": 14.90
                })

                st.toast("Aggiunto al carrello ✔")

    # =========================
    # PREMIUM
    # =========================
    else:

        st.markdown("## 💎 Box Premium — 24,90€")
        st.caption("Capi nuovi o seminuovi di qualità superiore.")

        st.markdown(
            """
            <div style="
                background:linear-gradient(135deg,#111827,#4F46E5);
                color:white;
                padding:18px;
                border-radius:18px;
                margin:15px 0;
                text-align:center;
            ">
                <div style="font-size:20px;font-weight:900;">BOX PREMIUM 💎</div>
                <div style="font-size:13px;opacity:0.9;">
                    Selezione premium curata a mano
                </div>
                <div style="margin-top:8px;font-size:14px;">
                    💰 24,90€
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("➕ Aggiungi Box Premium", key="premium_btn"):

            st.session_state.cart.append({
                "name": f"Box Premium ({taglia})",
                "price": 24.90
            })

            st.toast("Premium aggiunta ✔")
# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.markdown("""
I capi acquistati rimangono a te.

🚚 Spedizione:
- GRATIS sopra 50€
- GRATIS con Box
- 7,90€ senza Box
""")

    if st.button("Aggiungi Body 9,90€"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})

# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona")

    st.markdown("""
Ricevi Box → usi → restituisci → continui

Durata: 90 giorni

Se continui:
✔ spedizione gratis

Se ti fermi:
✔ 7,90€

♻️ Patto 10x10:
Ricevi 10 capi → restituisci 10

Se rompi:
👖 jeans x jeans oppure 5€
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "Chi":

    st.title("Chi siamo")

    st.markdown("""
LoopBaby nasce da un problema reale:

i bambini crescono troppo in fretta.

Troppi vestiti inutilizzati,
troppi soldi sprecati.

Abbiamo creato un sistema:

✔ meno sprechi  
✔ più riuso  
✔ più risparmio  

Non vendiamo solo vestiti.

Cambiamo il modo di usarli.
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    totale = 0

    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([3,1,1])

        col1.write(item["name"])
        col2.write(f"{item['price']}€")

        if col3.button("❌", key=f"del{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

        totale += item["price"]

    st.write(f"Totale: {totale}€")

# =========================
# PROFILO COMPLETO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo")

    users = load_users()
    user = st.session_state.user

    st.markdown(f"### Ciao {user.get('nome','')} 👋")

    nome = st.text_input("Nome", user.get("nome",""))
    telefono = st.text_input("Telefono", user.get("telefono",""))

    st.subheader("Bambino")

    nome_bimbo = st.text_input("Nome bambino", user.get("nome_bimbo",""))
    taglia = st.selectbox("Taglia", ["50-56","62-68","74-80","86-92"])

    st.subheader("Indirizzo")

    via = st.text_input("Via", user.get("via",""))
    citta = st.text_input("Città", user.get("citta",""))
    cap = st.text_input("CAP", user.get("cap",""))

    note = st.text_area("Note", user.get("note",""))

    if st.button("Salva"):

        user.update({
            "nome": nome,
            "telefono": telefono,
            "nome_bimbo": nome_bimbo,
            "taglia": taglia,
            "via": via,
            "citta": citta,
            "cap": cap,
            "note": note
        })

        for u in users:
            if isinstance(u, dict) and u.get("email") == user.get("email"):
                u.update(user)

        save_users(users)

        st.success("Salvato")
