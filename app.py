import streamlit as st
import os
import base64
import json
from datetime import date

# --- DATABASE ---
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except: pass
    return {
        "nome_genitore": "", "email": "", "telefono": "",
        "nome_bambino": "", "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm", "locker": ""
    }

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)

# --- CONFIG ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

def vai(p):
    st.session_state.pagina = p
    st.session_state.menu_open = False
    st.rerun()

# --- IMMAGINI ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")

# --- CSS ---
st.markdown(f"""
<style>
[data-testid="stHeader"], #MainMenu {{display:none;}}
.stApp {{ background-color:#FDFBF7; max-width:450px; margin:auto; }}

.header {{
    background-image:url("data:image/png;base64,{logo_bg}");
    background-size:cover;
    height:120px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-weight:800;
    font-size:30px;
    border-radius:0 0 25px 25px;
}}

.menu-box {{
    position:fixed;
    top:0;
    left:0;
    width:260px;
    height:100%;
    background:white;
    z-index:9999;
    padding:20px;
    box-shadow:2px 0 10px rgba(0,0,0,0.1);
}}

.card {{
    border-radius:20px;
    padding:20px;
    margin:15px;
    border:1px solid #EAE2D6;
    background:white;
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER + HAMBURGER ---
col1, col2 = st.columns([1,6])
with col1:
    if st.button("☰"):
        st.session_state.menu_open = not st.session_state.menu_open
with col2:
    st.markdown('<div class="header">LOOPBABY</div>', unsafe_allow_html=True)

# --- MENU ---
if st.session_state.menu_open:
    st.markdown('<div class="menu-box"><b>Menu</b></div>', unsafe_allow_html=True)

    if st.button("🏠 Home"): vai("Home")
    if st.button("📖 Info"): vai("Info")
    if st.button("📦 Box"): vai("Box")
    if st.button("🛍️ Shop"): vai("Vetrina")
    if st.button("👤 Profilo"): vai("Profilo")
    if st.button("👋 Chi siamo"): vai("ChiSiamo")
    if st.button("💬 Contatti"): vai("Contatti")

# --- PAGINE ---

if st.session_state.pagina == "Home":
    st.markdown("<h3>Ciao 👋</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">👶 Vestiti che crescono con il tuo bambino</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<div class="card">📖 Come funziona LoopBaby</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div class="card">📦 Scegli la tua Box</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div class="card">🛍️ Shop Vetrina</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    if not st.session_state.edit_mode:
        d = st.session_state.dati
        st.markdown(f"""
        <div class="card">
        👤 {d['nome_genitore']}<br>
        📧 {d['email']}<br>
        👶 {d['nome_bambino']}
        </div>
        """, unsafe_allow_html=True)

        if st.button("Modifica"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        with st.form("form"):
            n = st.text_input("Nome", st.session_state.dati['nome_genitore'])
            if st.form_submit_button("Salva"):
                st.session_state.dati['nome_genitore'] = n
                salva_dati_su_file(st.session_state.dati)
                st.session_state.edit_mode = False
                st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div class="card">❤️ Siamo genitori</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Contatti":
    st.markdown('<div class="card">💬 Contattaci</div>', unsafe_allow_html=True)
