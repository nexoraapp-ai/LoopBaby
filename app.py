import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# STILE GLOBALE (BEIGE)
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
# DATABASE
# =========================
DB_FILE = "db.json"

def load_users():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
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
# HEADER + HAMBURGER
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

    st.title("Accedi o Registrati")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    users = load_users()

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", key="login_pwd")

        if st.button("Accedi"):
            for u in users:
                if u["email"] == email and u["password"] == password:
                    st.session_state.user = u
                    st.rerun()
            st.error("Credenziali errate")

    # REGISTER
    with tab2:
        nome = st.text_input("Nome")
        email_r = st.text_input("Email registrazione")
        telefono = st.text_input("Telefono")
        password_r = st.text_input("Password", type="password", key="register_pwd")

        if st.button("Registrati"):
            if any(u["email"] == email_r for u in users):
                st.error("Email già registrata")
            else:
                new_user = {
                    "nome": nome,
                    "email": email_r,
                    "telefono": telefono,
                    "password": password_r
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
LoopBaby non è un e-commerce.

È un sistema circolare per vestire i bambini in modo intelligente.

♻️ crescita circolare  
🔄 riuso intelligente  
💛 risparmio reale  
👶 meno sprechi, più valore  
""")

    st.markdown("### 🔥 Mamme Fondatrici")
    st.write("Dona almeno 10 capi e ricevi una box gratuita")

    if st.button("Partecipa"):
        go("Promo")

# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("Mamme Fondatrici")

    st.markdown("""
Diventa fondatrice LoopBaby.

🎁 Dona almeno 10 capi  
📦 Ricevi una Box gratuita  
🚚 Spedizione pagata da noi  

Entro 48h riceverai etichetta.
""")

    peso = st.text_input("Peso pacco")
    dimensioni = st.text_input("Dimensioni")

    if st.button("Invia richiesta"):
        st.success("Etichetta inviata entro 48h")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box")

    st.markdown("Standard 14,90€")

    boxes = [
        ("SOLE ☀️", "#FFD600"),
        ("LUNA 🌙", "#E5E7EB"),
        ("NUVOLA ☁️", "#94A3B8")
    ]

    for name, color in boxes:
        st.markdown(f"<div style='background:{color};padding:15px;border-radius:10px'>{name}</div>", unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name": name, "price": 14.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

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
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona LoopBaby")

    st.markdown("""
Ricevi una box → usi i capi → restituisci → ricevi nuova box

Durata: fino a 90 giorni

Se continui:
✔ spedizione gratis

Se ti fermi:
✔ paghi 7,90€

♻️ Patto 10x10:
Ricevi 10 capi → restituisci 10 capi

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

i bambini crescono troppo velocemente.

Ogni mese vestiti inutilizzati,
spreco economico,
spreco ambientale.

Abbiamo creato un sistema:

✔ meno acquisti inutili  
✔ più riuso intelligente  
✔ risparmio continuo  

Non siamo un negozio.

Siamo un modello nuovo.
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

    st.title("👤 Profilo")

    users = load_users()
    user = st.session_state.user

    st.markdown(f"### Ciao {user.get('nome','')} 👋")

    # =========================
    # DATI GENITORE
    # =========================
    st.subheader("👤 Dati Genitore")

    nome = st.text_input("Nome e Cognome", user.get("nome",""))
    telefono = st.text_input("Telefono", user.get("telefono",""))
    email = user.get("email","")
    st.text_input("Email (non modificabile)", email, disabled=True)

    # =========================
    # DATI BAMBINO
    # =========================
    st.subheader("👶 Dati Bambino")

    nome_bimbo = st.text_input("Nome bambino", user.get("nome_bimbo",""))
    sesso = st.selectbox("Sesso", ["Non specificato","Maschio","Femmina"], index=0)
    nascita = st.date_input("Data nascita")
    taglia = st.selectbox("Taglia attuale", [
        "50-56","62-68","74-80","86-92"
    ])

    # =========================
    # INDIRIZZO
    # =========================
    st.subheader("📍 Indirizzo")

    via = st.text_input("Via e numero", user.get("via",""))
    citta = st.text_input("Città", user.get("citta",""))
    cap = st.text_input("CAP", user.get("cap",""))

    # =========================
    # PREFERENZE BOX
    # =========================
    st.subheader("📦 Preferenze Box")

    stile = st.selectbox("Stile preferito", [
        "Neutro",
        "Colorato",
        "Misto"
    ])

    note = st.text_area("Note (allergie, preferenze, ecc.)", user.get("note",""))

    # =========================
    # SALVA
    # =========================
    if st.button("💾 Salva Profilo"):

        user.update({
            "nome": nome,
            "telefono": telefono,
            "nome_bimbo": nome_bimbo,
            "sesso": sesso,
            "nascita": str(nascita),
            "taglia": taglia,
            "via": via,
            "citta": citta,
            "cap": cap,
            "stile": stile,
            "note": note
        })

        # aggiorna DB
        for u in users:
            if u["email"] == email:
                u.update(user)

        save_users(users)

        st.success("Profilo aggiornato ✅")
