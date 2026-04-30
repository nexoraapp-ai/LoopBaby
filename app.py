import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# SHEETDB
# =========================
SHEETDB_API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# FUNZIONI UTILI
# =========================
def safe_get(d, k, default=""):
    return d.get(k, default)

def login(email, password):
    url = f"{SHEETDB_API}/search?email={email}&password={password}"
    r = requests.get(url)
    if r.status_code == 200 and len(r.json()) > 0:
        return r.json()[0]
    return None

def registra_utente(email, password, dati):
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
    r = requests.post(SHEETDB_API, json=payload)
    return r.status_code in [200, 201]

def vai(p):
    st.session_state.pagina = p

def aggiungi_al_carrello(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast(f"✅ {n} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

# =========================
# CONFIG
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
# LOGIN / REGISTRAZIONE
# =========================
if st.session_state.utente is None:

    st.markdown("## LoopBaby 🔐")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # ---------------- LOGIN ----------------
    with tab1:
        email = st.text_input("Email", key="log_email")
        password = st.text_input("Password", type="password", key="log_pass")

        if st.button("Accedi"):
            user = login(email, password)
            if user:
                st.session_state.utente = user
                st.session_state.dati = user
                st.session_state.pagina = "Home"
                st.rerun()
            else:
                st.error("Credenziali errate")

    # ---------------- REGISTRAZIONE ----------------
    with tab2:
        email = st.text_input("Email ", key="reg_email")
        password = st.text_input("Password ", type="password", key="reg_pass")

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

            ok = registra_utente(email, password, dati)

            if ok:
                st.success("Registrazione completata")
            else:
                st.error("Errore registrazione")

    st.stop()

# =========================
# FIX DATI SICURI
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
# CSS (NON MODIFICATO)
# =========================
st.markdown("""
<style>
.stApp { background-color: #FDFBF7; max-width: 450px; margin: 0 auto; }
.card { border-radius: 25px; padding: 20px; margin: 10px; background: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h2 style="text-align:center;">LOOPBABY</h2>', unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = safe_get(st.session_state.dati, "nome_genitore").split(" ")[0]

    st.markdown(f"### Ciao {nome} 👋")

    st.markdown("""
    <div class="card">
    Benvenuto in LoopBaby 🔄<br>
    Armadio circolare per bambini
    </div>
    """, unsafe_allow_html=True)

    if st.button("Vai ai Box"):
        vai("Box")
        st.rerun()

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## Scegli Box 📦")

    tg = safe_get(st.session_state.dati, "taglia")

    st.info(f"Taglia: {tg}")

    if st.button("Box Standard 19.90€"):
        aggiungi_al_carrello("Box Standard", 19.90)

    if st.button("Box Premium 29.90€"):
        aggiungi_al_carrello("Box Premium", 29.90)

# =========================
# PROFILO (FIXATO)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## Profilo 👤")

    st.markdown(f"""
    <div class="card">
    👤 Nome: {safe_get(st.session_state.dati,'nome_genitore')}<br>
    📧 Email: {safe_get(st.session_state.dati,'email')}<br>
    📞 Tel: {safe_get(st.session_state.dati,'telefono')}<br>
    👶 Bambino: {safe_get(st.session_state.dati,'nome_bambino')}<br>
    📏 Taglia: {safe_get(st.session_state.dati,'taglia')}<br>
    📍 Locker: {safe_get(st.session_state.dati,'locker','Da scegliere')}
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
            st.success("Pagamento simulato")
            st.session_state.carrello = []
            st.rerun()

# =========================
# NAV
# =========================
st.markdown("---")
c = st.columns(4)

menu = ["Home", "Box", "Profilo", "Carrello"]

for i, m in enumerate(menu):
    with c[i]:
        if st.button(m):
            vai(m)
            st.rerun()
