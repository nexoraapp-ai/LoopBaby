import streamlit as st
import os
import base64
import json
from datetime import date
import requests
import hashlib

# ================= SHEETDB =================
API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def login_user(email, password):
    res = requests.get(f"{API_URL}/search", params={
        "email": email,
        "password": hash_password(password)
    })
    data = res.json()
    return data[0] if data else None

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

# ================= 1. FUNZIONI MEMORIA FISSA =================
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

# ================= 2. CONFIGURAZIONE E STATO =================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

if "pagina" not in st.session_state:
    st.session_state.pagina = "Login"

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

def vai(nome_pag):
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# BLOCCO ACCESSO
if not st.session_state.user and st.session_state.pagina not in ["Login", "Registrazione"]:
    st.session_state.pagina = "Login"

# ================= IMMAGINI =================
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")

# ================= 3. CSS (TUO IDENTICO) =================
st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
.stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
.main .block-container {{padding: 0 !important;}}
* {{ font-family: 'Lexend', sans-serif !important; }}

.header-custom {{
    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
    background-size: cover;
    height: 130px;
    display:flex;
    align-items:center;
    justify-content:center;
}}

.header-text {{
    color:white;
    font-size:32px;
    font-weight:800;
}}

.card {{
    border-radius:25px;
    padding:20px;
    margin:10px 20px;
    background:white;
}}

div.stButton > button {{
    background-color:#f43f5e !important;
    color:white !important;
    border-radius:18px !important;
    width:100% !important;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# ================= LOGIN =================
if st.session_state.pagina == "Login":
    st.markdown("## Login 🔐")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Accedi"):
        user = login_user(email, password)

        if user:
            st.session_state.user = user
            vai("Home")
            st.rerun()
        else:
            st.error("Credenziali errate")

    if st.button("Non hai un account? Registrati"):
        vai("Registrazione")
        st.rerun()

# ================= REGISTRAZIONE =================
elif st.session_state.pagina == "Registrazione":
    st.markdown("## Registrati ✨")

    with st.form("reg"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        nome = st.text_input("Nome genitore")
        bambino = st.text_input("Nome bambino")
        taglia = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm","86-92 cm"])
        locker = st.selectbox("Locker", ["Esselunga","InPost","Poste Italiane"])

        if st.form_submit_button("CREA ACCOUNT"):
            nuovo = {
                "email": email,
                "password": hash_password(password),
                "nome_genitore": nome,
                "nome_bambino": bambino,
                "taglia": taglia,
                "data_inizio": str(date.today()),
                "scadenza": "",
                "locker": locker
            }

            registra_user(nuovo)

            st.success("Account creato! Ora fai login 👇")
            vai("Login")
            st.rerun()

# ================= HOME =================
elif st.session_state.pagina == "Home":
    user = st.session_state.user

    nome = user.get("nome_genitore", "")

    st.markdown(f"""
    <div class="card">
        <h2>Ciao {nome} 👋</h2>
        <p>Benvenuto in LoopBaby</p>
    </div>
    """, unsafe_allow_html=True)

# ================= BOX =================
elif st.session_state.pagina == "Box":
    st.markdown("## Box 📦")

    if st.button("Box Luna"):
        aggiungi_al_carrello("Box Luna", 19.90)

    if st.button("Box Premium"):
        aggiungi_al_carrello("Box Premium", 29.90)

# ================= VETRINA =================
elif st.session_state.pagina == "Vetrina":
    st.markdown("## Vetrina 🛍️")

    if st.button("Body Bio"):
        aggiungi_al_carrello("Body Bio", 9.90)

# ================= CARRELLO =================
elif st.session_state.pagina == "Carrello":
    st.markdown("## Carrello 🛒")

    totale = sum(x["prezzo"] for x in st.session_state.carrello)

    for item in st.session_state.carrello:
        st.write(item["nome"], item["prezzo"])

    st.write("Totale:", totale)

# ================= PROFILO =================
elif st.session_state.pagina == "Profilo":
    user = st.session_state.user

    st.markdown("## Profilo 👤")

    st.write(user.get("email",""))
    st.write(user.get("nome_genitore",""))
    st.write(user.get("nome_bambino",""))
    st.write(user.get("taglia",""))
    st.write(user.get("locker",""))

    if st.button("Logout"):
        st.session_state.user = None
        vai("Login")
        st.rerun()

# ================= NAV =================
st.markdown("---")
c = st.columns(4)

if st.session_state.user:
    if c[0].button("Home"): vai("Home"); st.rerun()
    if c[1].button("Box"): vai("Box"); st.rerun()
    if c[2].button("Carrello"): vai("Carrello"); st.rerun()
    if c[3].button("Profilo"): vai("Profilo"); st.rerun()
