import streamlit as st
import requests
import bcrypt
import base64
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# STYLE BASE (BEIGE SHOPIFY)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f5f0e8;
}

.block-container {
    padding-top: 20px;
    max-width: 500px;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.logo {
    text-align:center;
    font-size:28px;
    font-weight:900;
    margin-bottom:10px;
}

button {
    border-radius: 15px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# UTILS
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p, h):
    return bcrypt.checkpw(p.encode(), h.encode())

def carica_dati(email):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower():
                return u
    except:
        pass
    return None

def email_esiste(email):
    try:
        r = requests.get(SHEETDB_URL)
        return any(u.get("email","").lower() == email.lower() for u in r.json())
    except:
        return False

def registra(user):
    requests.post(SHEETDB_URL, json={"data":[user]})

# =========================
# LOCKER REALI (SIMULATI)
# =========================
LOCKERS = {
    "Milano": ["Milano Centrale", "Milano Porta Romana", "Milano Lambrate"],
    "Monza": ["Monza Centro", "Monza Est"],
    "Lecco": ["Lecco Stazione", "Calolziocorte Centro"]
}

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"
if "user" not in st.session_state:
    st.session_state.user = {}

# =========================
# LOGO TOP
# =========================
st.markdown('<div class="logo">LOOPBABY 👶</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR MENU (HAMBURGER)
# =========================
if st.session_state.auth:
    menu = st.sidebar.selectbox("Menu", [
        "Home","Box","Vetrina","Profilo","Promo","Come funziona","Contatti"
    ])
    st.session_state.pagina = menu

# =========================
# LOGIN / REGISTER
# =========================
if not st.session_state.auth:

    st.title("Accedi / Registrati")

    mode = st.radio("Modalità", ["Login", "Registrazione"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # ============ REGISTRAZIONE ============
    if mode == "Registrazione":

        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome Bambino")
        nascita = st.date_input("Data nascita")

        taglia = st.selectbox("Taglia suggerita", [
            "50-56","62-68","74-80","86-92"
        ])

        citta = st.selectbox("Città", list(LOCKERS.keys()))
        locker = st.selectbox("Locker vicino", LOCKERS[citta])

        if st.button("Crea account"):

            if email_esiste(email):
                st.error("Email già registrata")
            else:
                user = {
                    "email": email,
                    "password": hash_password(password),
                    "nome": nome,
                    "bambino": bambino,
                    "nascita": str(nascita),
                    "taglia": taglia,
                    "citta": citta,
                    "locker": locker,
                    "telefono": "",
                }
                registra(user)

                st.session_state.user = user
                st.session_state.auth = True
                st.session_state.pagina = "Home"
                st.rerun()

    # ============ LOGIN ============
    else:
        if st.button("Entra"):

            data = carica_dati(email)

            if data and check_password(password, data["password"]):
                st.session_state.user = data
                st.session_state.auth = True
                st.session_state.pagina = "Home"
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()

# =========================
# HEADER USER
# =========================
user = st.session_state.user
nome = user.get("nome","Utente").split()[0]

st.markdown(f"### Ciao {nome} 👋")

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    col1, col2 = st.columns([2,1])

    with col1:
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
        Dona 10+ capi → gift card valida 3 mesi
        </div>
        """, unsafe_allow_html=True)

        if st.button("Vai alla promo"):
            st.session_state.pagina = "Promo"
            st.rerun()

    with col2:
        st.image("https://via.placeholder.com/160", caption="Il tuo bambino")

# =========================
# PROMO
# =========================
elif st.session_state.pagina == "Promo":

    st.title("Promo Mamme Fondatrici")

    peso = st.text_input("Peso pacco")
    dimensioni = st.text_input("Dimensioni")

    locker = user.get("locker")

    st.info(f"Locker di default: {locker}")

    if st.button("Invia richiesta"):

        st.success("Etichetta inviata entro 24h al tuo locker 📦")

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.title("BOX")

    tipo = st.radio("Tipo box", ["Standard","Premium"])

    if tipo == "Standard":

        st.markdown("### 14,90€")

        scelta = st.selectbox("Scegli box", ["Luna","Sole","Nuvola"])

        st.write("Stile selezionato:", scelta)

    else:
        st.markdown("### 24,90€ Premium")

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":

    st.title("Vetrina")

    st.info("Spedizione gratis sopra 50€ o con box")

    st.markdown("""
    <div class="card">
    Body Bio LoopBaby - 9,90€
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROFILO
# =========================
elif st.session_state.pagina == "Profilo":

    st.title("Profilo")

    st.write(user)

    if st.button("Modifica dati"):
        st.warning("Funzione modifica (step successivo la rendiamo completa)")

# =========================
# CONTATTI
# =========================
elif st.session_state.pagina == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 3921404637")
    st.write("Rispondiamo entro poche ore (no chiamate)")
