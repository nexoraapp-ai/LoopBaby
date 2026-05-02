import streamlit as st
import requests
import bcrypt
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# SAFE UTILS (NO CRASH)
# =========================
def safe(d, key, default=""):
    return (d or {}).get(key, default)

def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

# =========================
# LOCKER SYSTEM
# =========================
LOCKER = {
    "Calolziocorte": ["InPost Centro", "Esselunga", "Poste Italiane"],
    "Milano": ["Duomo Locker", "Stazione Centrale"],
    "Lecco": ["Lecco Centro", "Bione Locker"]
}

# =========================
# DATABASE
# =========================
def get_users():
    try:
        return requests.get(SHEETDB_URL).json()
    except:
        return []

def find_user(email):
    for u in get_users():
        if safe(u,"email").lower() == email.lower():
            return u
    return None

def save_user(user):
    requests.post(SHEETDB_URL, json={"data":[user]})

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# DESIGN (BEIGE SHOPIFY STYLE)
# =========================
st.markdown("""
<style>
.stApp { background:#f6f1e8; }

.card{
    background:white;
    padding:18px;
    border-radius:18px;
    margin:10px 0;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
}

.title{
    font-size:26px;
    font-weight:800;
}

.small{
    font-size:13px;
    color:#555;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (SHOPIFY STYLE)
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Home", "Box", "Vetrina", "Profilo",
    "Come funziona", "Contatti", "Logout"
])

# =========================
# LOGIN / REGISTER (BULLETPROOF)
# =========================
if st.session_state.page == "login":

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # ---------------- REGISTER ----------------
    if mode == "Registrati":

        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")

        taglia = st.selectbox("Taglia", ["50-56", "62-68", "74-80"])

        città = st.selectbox("Città", list(LOCKER.keys()))
        locker = st.selectbox("Locker", LOCKER[città])

        if st.button("Crea account"):

            if find_user(email):
                st.error("Email già registrata")
                st.stop()

            if not email or "@" not in email:
                st.error("Email non valida")
                st.stop()

            user = {
                "email": email,
                "password": hash_password(password),
                "nome": nome,
                "bambino": bambino,
                "nascita": str(nascita),
                "taglia": taglia,
                "città": città,
                "locker": locker
            }

            save_user(user)

            st.success("Account creato!")
            st.session_state.user = user
            st.session_state.page = "home"
            st.rerun()

    # ---------------- LOGIN ----------------
    else:
        if st.button("Entra"):

            u = find_user(email)

            if not u:
                st.error("Utente non trovato")
                st.stop()

            if not check_password(password, safe(u,"password")):
                st.error("Password errata")
                st.stop()

            st.session_state.user = u
            st.session_state.page = "home"
            st.rerun()

    st.stop()

# =========================
# USER SAFE LOAD
# =========================
u = st.session_state.user or {}

nome = (safe(u,"nome") or "Utente").split()[0]

# =========================
# HOME (SHOPIFY DASHBOARD)
# =========================
if menu == "Home":

    st.markdown(f"""
    <div class="title">Ciao {nome} 👋</div>

    <div class="card">
    👶 Capi selezionati<br>
    🔄 Cresce con il bambino<br>
    💰 Risparmio reale<br>
    🏠 Locker vicino a te<br>
    ♻️ Zero sprechi
    </div>

    <div class="card">
    <b>✨ Promo Mamme Fondatrici</b><br>
    Dona 10+ capi → gift card box entro 3 mesi (OBBLIGATORIO)
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
elif menu == "Box":

    st.title("Box")

    tipo = st.radio("Scegli", ["Standard 14,90€", "Premium 24,90€"])

    if tipo.startswith("Standard"):

        scelta = st.selectbox("Seleziona Box", ["Luna 🌙", "Sole ☀️", "Nuvola ☁️"])

        st.info(f"Taglia automatica: {safe(u,'taglia')}")

        st.markdown("👕 Apri box e vedi contenuto selezionato")

    else:
        st.success("Premium: capi selezionati manualmente")

# =========================
# VETRINA
# =========================
elif menu == "Vetrina":

    st.title("Vetrina 🛍️")

    st.write("Tutto quello che acquisti resta tuo per sempre")

# =========================
# PROFILO
# =========================
elif menu == "Profilo":

    st.title("Profilo")

    st.write("Nome:", safe(u,"nome"))
    st.write("Bambino:", safe(u,"bambino"))
    st.write("Taglia:", safe(u,"taglia"))
    st.write("Locker:", safe(u,"locker"))

    if st.button("Modifica"):
        st.info("Editor completo nel prossimo step")

# =========================
# COME FUNZIONA
# =========================
elif menu == "Come funziona":

    st.title("Come funziona")

    st.write("""
LoopBaby è un sistema circolare:
1. scegli box
2. ricevi a casa/locker
3. usi capi
4. restituisci
5. ricevi nuova taglia
""")

# =========================
# CONTATTI
# =========================
elif menu == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📞 3921404637")
    st.write("Rispondiamo il prima possibile")

# =========================
# LOGOUT
# =========================
elif menu == "Logout":
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()
