import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA (DATABASE) ---
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
        "taglia": "50-56 cm (0-3m)", "locker": ""
    }

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

# Gestione link ipertestuale "contattaci"
if "nav" in st.query_params:
    st.session_state.pagina = "Contatti"
    st.query_params.clear()

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")
logo_data = get_base64("logo.png")  # 🔥 LOGO

# --- 3. CSS ---
st.markdown("""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
.stApp { background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }
.main .block-container {padding: 0 !important;}

.header-box { padding: 30px 20px 10px 20px; text-align:center; }
.header-box img { max-width: 220px; }

.slogan { font-size: 13px; color: #64748b; margin-top: 5px; }

.home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }
.ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
.headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
.item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
.baby-photo { width: 100%; border-radius: 25px; object-fit: cover; }

.card { border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }
.box-luna { background-color: #f1f5f9 !important; }
.box-sole { background-color: #FFD600 !important; }
.box-nuvola { background-color: #94A3B8 !important; color: white !important; }
.box-premium { background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; }

.promo-box { background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }
.prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

div.stButton > button { background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }

[data-testid="stHorizontalBlock"] { position: fixed !important; bottom: 0 !important; width: 100% !important; background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important; }
[data-testid="stHorizontalBlock"] button { background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# --- HEADER CON LOGO ---
st.markdown(f"""
<div class="header-box">
    <img src="data:image/png;base64,{logo_data}">
    <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
</div>
""", unsafe_allow_html=True)

# --- HOME ---
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)

# --- NAV ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("🏠\nHome"): vai("Home")
with c2:
    if st.button("📖\nInfo"): vai("Info")
with c3:
    if st.button("📦\nBox"): vai("Box")
with c4:
    if st.button("🛍️\nVetrina"): vai("Vetrina")
with c5:
    if st.button("👤\nProfilo"): vai("Profilo")
with c6:
    if st.button("👋\nChi Siamo"): vai("ChiSiamo")
