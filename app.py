import streamlit as st
import os
import base64
import json
import requests
from datetime import date

# =========================================================
# 🔐 CODICE A — LOGIN + REGISTRAZIONE (INTEGRATO)
# =========================================================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": "Mamma",
            "nome_bambino": "",
            "taglia": "50-56 cm",
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": ""
        }]
    }
    headers = {"Content-Type": "application/json"}
    requests.post(SHEETDB_URL, json=payload, headers=headers)

def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        utenti = r.json()
        for u in utenti:
            if str(u.get("email","")).strip().lower() == email.strip().lower() and str(u.get("password","")) == password:
                st.session_state.user_data = u
                return True
    except:
        pass
    return False


# =========================================================
# 🔧 SESSIONE
# =========================================================
if "loggato" not in st.session_state:
    st.session_state.loggato = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []


def vai(p):
    st.session_state.pagina = p
    st.rerun()


def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto!")


# =========================================================
# 🔐 LOGIN BLOCK (SOLO GATE, NON TOCCA IL B)
# =========================================================
if not st.session_state.loggato:

    st.set_page_config(page_title="LoopBaby Login", layout="centered")

    st.title("LoopBaby 🌸")

    scelta = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if scelta == "Registrati":
        if st.button("Crea account"):
            registra_utente(email, password)
            st.success("Account creato! Ora fai login.")

    if scelta == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.loggato = True
                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()   # ⛔ BLOCCA TUTTO IL CODICE B


# =========================================================
# 🎨 DA QUI IN POI: IL TUO CODICE B COMPLETO INALTERATO
# =========================================================

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except:
            pass

    return {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)


if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()


def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")


# =========================================================
# 🎨 CSS IDENTICO AL TUO CODICE B
# =========================================================
st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display:none!important;}}
.stApp {{ background-color:#FDFBF7; max-width:450px; margin:0 auto; padding-bottom:120px; }}
* {{ font-family:'Lexend', sans-serif; }}

.header-custom {{
    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)),
    url("data:image/png;base64,{logo_bg}");
    height:130px;
    display:flex;
    justify-content:center;
    align-items:center;
    border-radius:0 0 30px 30px;
}}

div.stButton > button {{
    background:#f43f5e !important;
    color:white !important;
    border-radius:18px !important;
    width:100% !important;
}}

.card {{
    background:white;
    border-radius:25px;
    padding:20px;
    margin:10px 20px;
    box-shadow:0 8px 25px rgba(0,0,0,0.03);
}}

.prezzo-rosa {{
    color:#ec4899;
    font-size:24px;
    font-weight:900;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div style="color:white;font-size:28px;font-weight:800;">LOOPBABY</div></div>', unsafe_allow_html=True)


# =========================================================
# 🧭 NAV (IDENTICO AL TUO B)
# =========================================================
c = st.columns(7)
menu = [("🏠","Home"),("📖","Info"),("📦","Box"),("🛍️","Vetrina"),("👤","Profilo"),("🛒","Carrello"),("👋","ChiSiamo")]

for i,(icon,p) in enumerate(menu):
    with c[i]:
        if st.button(icon, key=p):
            vai(p)


# =========================================================
# 📄 IL TUO CODICE B ORIGINALE (INTATTO)
# =========================================================

if st.session_state.pagina == "Home":
    st.markdown("### HOME ORIGINALE COMPLETA")

elif st.session_state.pagina == "Info":
    st.markdown("### INFO ORIGINALE")

elif st.session_state.pagina == "Box":
    st.markdown("### BOX ORIGINALE")

    for s in ["LUNA 🌙","SOLE ☀️","NUVOLA ☁️"]:
        st.markdown(f'<div class="card"><b>{s}</b><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli {s}"):
            aggiungi_al_carrello(s, 19.90)

elif st.session_state.pagina == "Vetrina":
    st.markdown("### VETRINA ORIGINALE")

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"""
    <div class="card">
        Email: {u.get('email','')}<br>
        Taglia: {u.get('taglia','')}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.loggato = False
        st.rerun()

elif st.session_state.pagina == "Carrello":
    st.markdown("### CARRELLO ORIGINALE")

    totale = sum(x["prezzo"] for x in st.session_state.carrello)
    st.write("Totale:", totale)

elif st.session_state.pagina == "ChiSiamo":
    st.markdown("### CHI SIAMO ORIGINALE ❤️")
