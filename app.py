import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================
# SHEETDB CONFIG
# =========================
SHEETDB_API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# LOGIN / REGISTER SHEETDB
# =========================
def salva_su_sheetdb(dati, password):
    payload = {
        "data": [{
            "email": dati["email"],
            "password": password,
            "nome_genitore": dati["nome_genitore"],
            "nome_bambino": dati["nome_bambino"],
            "taglia": dati["taglia"],
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": dati["locker"],
            "telefono": dati.get("telefono", "")
        }]
    }
    requests.post(SHEETDB_API, json=payload)


def login_sheetdb(email, password):
    url = f"{SHEETDB_API}/search?email={email}&password={password}"
    r = requests.get(url)
    data = r.json()
    return len(data) > 0

# =========================
# FIX DATI (NO KEY ERROR)
# =========================
def safe_dati():
    return {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# SESSION STATE
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "dati" not in st.session_state:
    st.session_state.dati = safe_dati()

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

def vai(p):
    st.session_state.pagina = p

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"{nome} aggiunto")

# =========================
# LOGIN / REGISTER UI
# =========================
if not st.session_state.logged:

    st.title("LoopBaby Login")

    tab1, tab2 = st.tabs(["Login", "Registrazione"])

    # ---------------- LOGIN ----------------
    with tab1:
        email = st.text_input("Email")
        password_r = st.text_input("Password", type="password", key="reg_password")

        if st.button("ENTRA"):
            if login_sheetdb(email, password):
                st.session_state.logged = True
                st.session_state.dati["email"] = email
                st.success("Login ok")
                st.rerun()
            else:
                st.error("Credenziali errate")

    # ---------------- REGISTER ----------------
    with tab2:
        nome = st.text_input("Nome genitore")
        email_r = st.text_input("Email ")
        tel = st.text_input("Telefono")
        bambino = st.text_input("Nome bambino")
        taglia = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm","86-92 cm"])
        locker = st.text_input("Locker")
        password_r = st.text_input("Password", type="password")

        if st.button("REGISTRATI"):
            dati = {
                "nome_genitore": nome,
                "email": email_r,
                "telefono": tel,
                "nome_bambino": bambino,
                "taglia": taglia,
                "locker": locker
            }

            salva_su_sheetdb(dati, password_r)

            st.success("Registrazione completata")
            st.session_state.logged = True
            st.session_state.dati = dati
            st.rerun()

    st.stop()

# =========================
# DESIGN (IDENTICO AL TUO)
# =========================
st.markdown("""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
.stApp { background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }
.main .block-container {padding: 0 !important;}
* { font-family: 'Lexend', sans-serif !important; }

.header-custom {
    background: #000;
    height: 130px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:0 0 30px 30px;
}
.header-text {
    color:white;
    font-size:32px;
    font-weight:800;
}

.card { border-radius: 25px; padding: 20px; margin: 10px 20px; background:white;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# =========================
# HOME (UGUALE)
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.dati.get("nome_genitore","")

    st.markdown(f"### Ciao {nome} 👋")

    st.markdown("""
    <div class="card">
    Armadio circolare per bambini
    </div>
    """, unsafe_allow_html=True)

    if st.button("Vai Box"):
        vai("Box")
        st.rerun()

# =========================
# BOX (UGUALE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## Box")

    if st.button("Aggiungi"):
        aggiungi_al_carrello("Box", 19.9)

# =========================
# PROFILO (FIX KEYERROR)
# =========================
elif st.session_state.pagina == "Profilo":

    d = st.session_state.dati

    st.markdown(f"""
    <div class="card">
    Nome: {d.get('nome_genitore','')} <br>
    Email: {d.get('email','')} <br>
    Telefono: {d.get('telefono','')} <br>
    Bambino: {d.get('nome_bambino','')} <br>
    Nascita: {d.get('nascita','')} <br>
    Taglia: {d.get('taglia','')} <br>
    Locker: {d.get('locker','')}
    </div>
    """, unsafe_allow_html=True)

# =========================
# LOGOUT
# =========================
if st.button("Logout"):
    st.session_state.logged = False
    st.rerun()
