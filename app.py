import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA ---
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            d = json.load(f)
            d["nascita"] = date.fromisoformat(d["nascita"])
            return d
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
if "locker_trovati" not in st.session_state:
    st.session_state.locker_trovati = []

# Gestione link "contattaci"
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

# --- 3. CSS TOTALE (BEIGE + SCHELETRO BLINDATO) ---
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
    .card { border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }
    .box-luna { background-color: #f1f5f9 !important; }
    .box-sole { background-color: #FFD600 !important; color: #000 !important; } 
    .box-nuvola { background-color: #94A3B8 !important; color: white !important; }
    .box-premium { background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .link-inline { color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }
    div.stButton > button { background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }
    [data-testid="stHorizontalBlock"] { position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important; }
    [data-testid="stHorizontalBlock"] button { background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><div class="logo-h"><span class="heart">💗</span> LoopBaby</div><div style="font-size:13px; color:#64748b;">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 4. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Opzioni:</b> Box <b>Standard</b> (usato ottimo) o <b>Premium</b> (nuovi). Vetrina: capi tuoi per sempre.<br><br>
            <b>2. Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi, per problemi <a href="/?nav=contatti" target="_self" class="link-inline">contattaci</a>.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o cambiare taglia (ti ricordiamo noi 10gg prima).
        </div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    qualita = st.radio("Seleziona la qualità:", ["Standard", "Premium"], horizontal=True)
    if qualita == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio nuvola")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=f"s_{s}"): st.success(f"{s} aggiunta!")
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Box Premium"): st.success("Premium aggiunta!")

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

# --- PROFILO CON SCELTA LOCKER REALE ---
elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<br>
            <hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br>
            <hr>
            <b>📍 Locker Selezionato:</b><br><span style="color:#0d9488; font-weight:800;">{st.session_state.dati['locker'] if st.session_state.dati['locker'] else 'Nessuno scelto'}</span>
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        with st.form("edit_profilo"):
            nome = st.text_input("Nome e Cognome", st.session_state.dati['nome_genitore'])
            mail = st.text_input("Email", st.session_state.dati['email'])
            tel = st.text_input("Telefono", st.session_state.dati['telefono'])
            nome_b = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            nascita = st.date_input("Data di nascita", st.session_state.dati['nascita'])
            taglia = st.selectbox("Taglia attuale", ["50-56 cm (0-3m)", "62-68 cm (3-6m)", "74-80 cm (6-12m)", "86-92 cm (12-24m)"], index=0)
            
            st.markdown("---")
            st.markdown("### 📍 Scegli il tuo Locker")
            # Simulazione Posizione
            if st.form_submit_button("🔍 Trova Locker vicino alla mia posizione"):
                st.session_state.locker_trovati = [
                    "Locker Esselunga - Via Roma 10, Calolziocorte",
                    "Locker Stazione FS - Piazza Garibaldi, Lecco",
                    "Locker LoopBaby - Via Mazzini 5, Olginate"
                ]
            
            lock_scelto = st.selectbox("Seleziona dalla lista:", 
                                      ["Seleziona un punto..."] + st.session_state.locker_trovati if st.session_state.locker_trovati else [st.session_state.dati['locker']])

            if st.form_submit_button("SALVA E BLOCCA DATI"):
                st.session_state.dati = {"nome_genitore": nome, "email": mail, "telefono": tel, "nome_bambino": nome_b, "nascita": nascita, "taglia": taglia, "locker": lock_scelto}
                salva_dati_su_file(st.session_state.dati)
                st.session_state.edit_mode = False
                st.rerun()

elif st.session_state.pagina == "Contatti":
    st.markdown('<div class="card" style="background:#FFF5F5;"><b>Contattaci</b><br>💬 333 1234567<br>📧 hello@loopbaby.it</div>', unsafe_allow_html=True)
    if st.button("Indietro"): vai("Info")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div class="card"><b>Siamo genitori, come te.</b><br>Creato per ridurre sprechi e costi.</div>', unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: if st.button("🏠\nHome"): vai("Home")
with c2: if st.button("📖\nInfo"): vai("Info")
with c3: if st.button("📦\nBox"): vai("Box")
with c4: if st.button("🛍️\nVetrina"): vai("Vetrina")
with c5: if st.button("👤\nProfilo"): vai("Profilo")
with c6: if st.button("👋\nChi"): vai("ChiSiamo")
