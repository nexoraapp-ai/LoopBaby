import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI PER LA MEMORIA FISSA (FILE JSON) ---
DB_FILE = "dati_utente.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            dati = json.load(f)
            # Converte la stringa data in oggetto date
            dati["nascita"] = date.fromisoformat(dati["nascita"])
            return dati
    return {
        "nome_genitore": "", "email": "", "telefono": "",
        "nome_bambino": "", "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm (0-3m)", "locker": ""
    }

def salva_dati(dati):
    dati_da_salvare = dati.copy()
    dati_da_salvare["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(dati_da_salvare, f)

# --- 2. CONFIGURAZIONE E STATO INIZIALE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Inizializza i dati dal file all'avvio
if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")

# --- 3. CSS (BEIGE + LOOK APP) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp { background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }
    .main .block-container {padding: 0 !important;}
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-h { font-size: 30px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .heart { color: #f43f5e; font-size: 34px; }
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .card { border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background-color: #FFFFFF; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    div.stButton > button { background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }
    [data-testid="stHorizontalBlock"] { position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important; }
    [data-testid="stHorizontalBlock"] button { background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><div class="logo-h"><span class="heart">💗</span> LoopBaby</div><div style="font-size:13px; color:#64748b;">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 4. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    saluto = f"Ciao {st.session_state.dati['nome_genitore']}!" if st.session_state.dati['nome_genitore'] else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    
    if not st.session_state.edit_mode:
        # --- MODALITÀ VISUALIZZAZIONE ---
        st.markdown(f"""
        <div class="card" style="text-align:left;">
            <b>👤 Genitore:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<br><br>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br><br>
            <b>📍 Locker:</b> {st.session_state.dati['locker']}
        </div>
        """, unsafe_allow_html=True)
        if st.button("MODIFICA DATI"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        # --- MODALITÀ MODIFICA ---
        with st.form("form_profilo"):
            nome = st.text_input("Nome e Cognome", st.session_state.dati['nome_genitore'])
            email = st.text_input("Email", st.session_state.dati['email'])
            tel = st.text_input("Cellulare", st.session_state.dati['telefono'])
            nome_b = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            nascita = st.date_input("Data di nascita", st.session_state.dati['nascita'])
            taglia = st.selectbox("Taglia", ["50-56 cm (0-3m)", "62-68 cm (3-6m)", "74-80 cm (6-12m)", "86-92 cm (12-24m)"], 
                                  index=["50-56 cm (0-3m)", "62-68 cm (3-6m)", "74-80 cm (6-12m)", "86-92 cm (12-24m)"].index(st.session_state.dati['taglia']))
            
            st.markdown("### 📍 Punto di Ritiro")
            if st.form_submit_button("🔍 Clicca qui per posizione Locker più vicino"):
                st.session_state.temp_locker = "Locker Via Roma 10, Calolziocorte (Rilevato)"
            
            locker = st.text_input("Indirizzo Locker", st.session_state.dati['locker'])
            
            if st.form_submit_button("SALVA E BLOCCA DATI"):
                st.session_state.dati = {
                    "nome_genitore": nome, "email": email, "telefono": tel,
                    "nome_bambino": nome_b, "nascita": nascita,
                    "taglia": taglia, "locker": locker
                }
                salva_dati(st.session_state.dati)
                st.session_state.edit_mode = False
                st.success("Dati salvati nel database!")
                st.rerun()

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c5: 
    if st.button("👤\nProfilo"): vai("Profilo")
# (Altre icone per brevità omesse, ma incluse nel tuo codice completo)
