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
# PASSWORD
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

# =========================
# LOCKER REALI (ESEMPIO)
# =========================
LOCKERS = {
    "Milano": ["Milano Centrale", "Milano Porta Romana", "Milano Lambrate"],
    "Calolziocorte": ["Calolziocorte Centro", "Lecco Nord Locker"],
    "Lecco": ["Lecco Centro", "Lecco Stazione"]
}

# =========================
# DATABASE
# =========================
def get_users():
    try:
        return requests.get(SHEETDB_URL).json()
    except:
        return []

def save_user(user):
    requests.post(SHEETDB_URL, json={"data":[user]})

def find_user(email):
    for u in get_users():
        if u.get("email","").lower() == email.lower():
            return u
    return None

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

# =========================
# SIDEBAR MENU
# =========================
if st.session_state.auth:
    with st.sidebar:
        st.title("Menu")
        if st.button("🏠 Home"): st.session_state.page="Home"
        if st.button("📦 Box"): st.session_state.page="Box"
        if st.button("🛍️ Vetrina"): st.session_state.page="Vetrina"
        if st.button("👤 Profilo"): st.session_state.page="Profilo"
        if st.button("📞 Contatti"): st.session_state.page="Contatti"
        if st.button("🚪 Logout"):
            st.session_state.auth=False
            st.rerun()

# =========================
# LOGIN / REGISTRAZIONE
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":

        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")

        taglia = st.selectbox("Taglia suggerita", ["50-56", "62-68", "74-80", "86-92"])

        citta = st.selectbox("Città", list(LOCKERS.keys()))
        locker = st.selectbox("Locker", LOCKERS[citta])

        if st.button("Crea account"):

            if find_user(email):
                st.error("Email già registrata")
            elif "@" not in email:
                st.error("Email non valida")
            else:
                save_user({
                    "email": email,
                    "password": hash_password(password),
                    "nome": nome,
                    "bambino": bambino,
                    "nascita": str(nascita),
                    "taglia": taglia,
                    "citta": citta,
                    "locker": locker
                })

                st.success("Account creato")
                st.session_state.auth = True
                st.session_state.user = find_user(email)
                st.rerun()

    else:

        if st.button("Entra"):
            u = find_user(email)
            if u and check_password(password, u["password"]):
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# STYLE (BEIGE CLEAN)
# =========================
st.markdown("""
<style>
.stApp { background:#F5F1EA; }
.card { background:white; padding:18px; border-radius:18px; margin:10px 0; }
.title { font-size:28px; font-weight:800; }
.small { font-size:13px; color:#555; }
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO (SEMPRE SOPRA)
# =========================
st.markdown("""
<div style="text-align:center;padding:10px 0;">
    <img src="https://via.placeholder.com/160x50?text=LOOPBABY+LOGO" height="45">
</div>
""", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user
    nome = u.get("nome","Utente").split()[0]

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown(f"<div class='title'>Ciao {nome} 👋</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        👶 Capi selezionati<br>
        🔄 Cresce con il bambino<br>
        💰 Risparmio reale<br>
        🏠 Locker vicino a te<br>
        ♻️ Zero sprechi
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        <b>✨ Promo Mamme Fondatrici</b><br>
        Dona 10 capi → gift card valida 3 mesi
        </div>
        """, unsafe_allow_html=True)

        if st.button("Partecipa Promo"):
            st.session_state.page="Promo"
            st.rerun()

    with col2:
        st.image("https://images.unsplash.com/photo-1601758123927-196e1f6d4b5d", width=160)

# =========================
# PROMO
# =========================
elif st.session_state.page == "Promo":

    st.title("Promo Mamme Fondatrici")

    with st.form("promo"):

        peso = st.text_input("Peso pacco")
        dim = st.text_input("Dimensioni")

        lock = st.selectbox("Locker", LOCKERS[st.session_state.user["citta"]])

        ok = st.form_submit_button("Invia")

        if ok:
            st.success("📦 Etichetta inviata entro 24h")
            st.info("Ritiro a nostro carico")

    if st.button("Indietro"):
        st.session_state.page="Home"
        st.rerun()

# =========================
# BOX
# =========================
elif st.session_state.page == "Box":

    st.title("Box")

    st.markdown("Standard 14,90€")
    if st.button("Aggiungi Standard"):
        st.session_state.carrello.append("Box Standard")

    st.markdown("Premium 24,90€")
    if st.button("Aggiungi Premium"):
        st.session_state.carrello.append("Box Premium")

# =========================
# VETRINA
# =========================
elif st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.write("✔ Rimangono tuoi per sempre")
    st.write("✔ Gratis sopra 50€ o con box")
    st.write("✔ Sotto 50€ spedizione 7,90€")

# =========================
# PROFILO
# =========================
elif st.session_state.page == "Profilo":

    u = st.session_state.user

    st.title("Profilo")

    st.write("Nome:", u.get("nome",""))
    st.write("Bambino:", u.get("bambino",""))
    st.write("Taglia:", u.get("taglia",""))
    st.write("Locker:", u.get("locker",""))

# =========================
# CONTATTI
# =========================
elif st.session_state.page == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📞 3921404637")
    st.write("Rispondiamo il prima possibile su WhatsApp o email")
