import streamlit as st
import os
import base64
import requests
from datetime import date

# =========================
# SHEETDB
# =========================
SHEETDB_API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# UTILS SICURE
# =========================
def safe(d, k, default=""):
    return d.get(k, default) if isinstance(d, dict) else default

def login(email, password):
    url = f"{SHEETDB_API}/search?email={email}&password={password}"
    r = requests.get(url)
    if r.status_code == 200 and len(r.json()) > 0:
        return r.json()[0]
    return None

def registra(email, password, dati):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": dati.get("nome_genitore",""),
            "nome_bambino": dati.get("nome_bambino",""),
            "telefono": dati.get("telefono",""),
            "taglia": dati.get("taglia","50-56 cm"),
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": dati.get("locker","")
        }]
    }
    requests.post(SHEETDB_API, json=payload)

def vai(p):
    st.session_state.pagina = p

def add_cart(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast(f"✅ {n} aggiunto!")

# =========================
# INIT STATE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Auth"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "utente" not in st.session_state:
    st.session_state.utente = None

if "dati" not in st.session_state:
    st.session_state.dati = {}

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.utente is None:

    st.title("LoopBaby 🔐")

    tab1, tab2 = st.tabs(["Login", "Registrazione"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Accedi"):
            user = login(email, password)
            if user:
                st.session_state.utente = user
                st.session_state.dati = user
                st.session_state.pagina = "Home"
                st.rerun()
            else:
                st.error("Credenziali errate")

    with tab2:
        email_r = st.text_input("Email ", key="r1")
        pass_r = st.text_input("Password ", type="password", key="r2")

        nome = st.text_input("Nome genitore")
        bimbo = st.text_input("Nome bambino")
        tel = st.text_input("Telefono")

        if st.button("Registrati"):
            dati = {
                "nome_genitore": nome,
                "nome_bambino": bimbo,
                "telefono": tel,
                "taglia": "50-56 cm",
                "locker": ""
            }
            registra(email_r, pass_r, dati)
            st.success("Registrazione completata")

    st.stop()

# =========================
# FIX DATI
# =========================
BASE = {
    "nome_genitore": "",
    "email": "",
    "telefono": "",
    "nome_bambino": "",
    "nascita": "",
    "taglia": "50-56 cm",
    "locker": ""
}

for k in BASE:
    if k not in st.session_state.dati:
        st.session_state.dati[k] = BASE[k]

# =========================
# DESIGN (NON TOCCATO)
# =========================
st.markdown("""
<style>
.stApp { background:#FDFBF7; max-width:450px; margin:auto; }
.card { background:white; padding:20px; border-radius:20px; margin:10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center'>LOOPBABY</h2>", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = safe(st.session_state.dati, "nome_genitore").split(" ")[0]

    st.markdown(f"### Ciao {nome} 👋")

    st.markdown("""
    <div class='card'>
    Armadio circolare bambini ♻️
    </div>
    """, unsafe_allow_html=True)

    if st.button("Vai ai Box"):
        vai("Box")
        st.rerun()

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## Box 📦")

    tag = safe(st.session_state.dati, "taglia")

    st.info(f"Taglia: {tag}")

    if st.button("Standard 19.90€"):
        add_cart("Box Standard", 19.90)

    if st.button("Premium 29.90€"):
        add_cart("Box Premium", 29.90)

# =========================
# PROFILO (FIX DEFINITIVO)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## Profilo 👤")

    st.markdown(f"""
    <div class='card'>
    👤 {safe(st.session_state.dati,'nome_genitore')}<br>
    📧 {safe(st.session_state.dati,'email')}<br>
    📞 {safe(st.session_state.dati,'telefono')}<br>
    👶 {safe(st.session_state.dati,'nome_bambino')}<br>
    📏 {safe(st.session_state.dati,'taglia')}<br>
    📍 {safe(st.session_state.dati,'locker','Da scegliere')}
    </div>
    """, unsafe_allow_html=True)

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## Carrello 🛒")

    if not st.session_state.carrello:
        st.write("Vuoto")
    else:
        tot = 0
        for i in st.session_state.carrello:
            st.write(f"{i['nome']} - {i['prezzo']}€")
            tot += i['prezzo']

        st.markdown(f"### Totale: {tot}€")

        if st.button("Paga"):
            st.success("Pagamento ok")
            st.session_state.carrello = []
            st.rerun()

# =========================
# NAV BAR
# =========================
st.markdown("---")
cols = st.columns(4)

menu = ["Home", "Box", "Profilo", "Carrello"]

for i, m in enumerate(menu):
    with cols[i]:
        if st.button(m):
            vai(m)
            st.rerun()
