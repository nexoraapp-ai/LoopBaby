import streamlit as st
import requests
import bcrypt
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# PASSWORD
# =========================
def hash_pw(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_pw(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

# =========================
# LOCKER REALI
# =========================
LOCKERS = {
    "Calolziocorte": ["Esselunga Locker", "Poste Italiane", "InPost Point"],
    "Milano": ["Duomo Locker", "Centrale", "CityLife"],
}

# =========================
# DB
# =========================
def get_users():
    return requests.get(API).json()

def email_exists(email):
    return any(u["email"].lower() == email.lower() for u in get_users())

def save_user(data):
    requests.post(API, json={"data":[data]})

def login(email, pw):
    for u in get_users():
        if u["email"].lower() == email.lower():
            if check_pw(pw, u["password"]):
                st.session_state.user = u
                return True
    return False

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "cart" not in st.session_state:
    st.session_state.cart = []

def go(p):
    st.session_state.page = p

def add(n,p):
    st.session_state.cart.append((n,p))
    st.toast("Aggiunto!")

# =========================
# STYLE BASE BEIGE
# =========================
st.markdown("""
<style>
.stApp {background:#F5F1E8;}
.card {background:white;padding:18px;border-radius:18px;margin:10px 0;}
.header {text-align:center;font-size:28px;font-weight:900;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">LOOPBABY</div>', unsafe_allow_html=True)

# =========================
# LOGIN / REGISTRAZIONE
# =========================
if not st.session_state.auth:

    mode = st.radio("Accesso", ["Login","Registrati"])

    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")

    if mode == "Registrati":

        nome = st.text_input("Nome")
        cognome = st.text_input("Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")

        # taglia automatica
        if nascita.year >= 2024:
            taglia = "50-56"
        elif nascita.year >= 2023:
            taglia = "62-68"
        else:
            taglia = "74-80"

        città = st.selectbox("Città", list(LOCKERS.keys()))
        locker = st.selectbox("Locker", LOCKERS[città])

        if st.button("Registrati"):

            if email_exists(email):
                st.error("Email già registrata")
            else:
                save_user({
                    "nome":nome,
                    "cognome":cognome,
                    "email":email,
                    "password":hash_pw(pw),
                    "bambino":bambino,
                    "nascita":str(nascita),
                    "taglia":taglia,
                    "citta":città,
                    "locker":locker
                })
                st.success("Account creato")
                st.rerun()

    else:
        if st.button("Login"):
            if login(email,pw):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user

# =========================
# MENU
# =========================
page = st.sidebar.radio("Menu",[
    "Home","Box","Vetrina","Profilo",
    "Come funziona","Promo","Contatti","Carrello"
])

# =========================
# HOME (COMPLETA COME VOLEVI)
# =========================
if page == "Home":

    st.markdown(f"""
    <div style="display:flex;gap:20px;">

        <div style="width:60%;">
            <h2>Ciao {user['nome']} 👋</h2>

            <p>👶 Capi selezionati</p>
            <p>🔄 Cresce con il bambino</p>
            <p>💰 Risparmio reale</p>
            <p>🏠 Locker vicino a te</p>
            <p>♻️ Zero sprechi</p>

            <div class="card">
            <b>✨ Promo Mamme Fondatrici</b><br>
            Dona 10+ capi → gift card Box valida 3 mesi
            </div>
        </div>

        <div style="width:40%;">
            <img src="https://via.placeholder.com/180"
            style="border-radius:20px;width:100%;">
        </div>

    </div>
    """, unsafe_allow_html=True)

    if st.button("Dona 10 capi"):
        st.info("Entro 24h ricevi etichetta locker")

# =========================
# BOX
# =========================
elif page == "Box":

    st.title("Box")

    tipo = st.radio("Seleziona",["Standard 14,90","Premium 24,90"])

    if "Standard" in tipo:
        scelta = st.radio("Tipo",["Luna","Sole","Nuvola"])
        if st.button("Aggiungi"):
            add(scelta,14.90)
    else:
        if st.button("Premium"):
            add("Premium",24.90)

# =========================
# VETRINA
# =========================
elif page == "Vetrina":

    st.title("Vetrina")
    if st.button("Body 9.90"):
        add("Body",9.90)

# =========================
# PROFILO
# =========================
elif page == "Profilo":

    st.title("Profilo")

    st.write(user)

# =========================
# PROMO
# =========================
elif page == "Promo":

    st.title("Promo Mamme Fondatrici")

    st.write("""
    Dona 10 capi → noi ritiro gratuito  
    Ricevi gift card box valida 3 mesi
    """)

# =========================
# CONTATTI
# =========================
elif page == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📞 3921404637")

# =========================
# CARRELLO
# =========================
elif page == "Carrello":

    st.title("Carrello")

    tot = 0
    for n,p in st.session_state.cart:
        st.write(n,p)
        tot += p

    st.write("Totale:", tot)
