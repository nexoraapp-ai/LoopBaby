import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA ---
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

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (BEIGE + FIX MOBILE BAR) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* HEADER PANORAMICO */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 120px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; border-radius: 0 0 30px 30px;
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); }}

    /* FIX PER CELLULARE: BARRA ORIZZONTALE VERA */
    div[data-testid="stHorizontalBlock"] {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background-color: #FDFBF7 !important;
        border-top: 1px solid #EAE2D6 !important;
        z-index: 999999 !important;
        padding: 5px 0 !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
    }}
    
    /* Forza i bottoni a stare vicini e piccoli */
    div[data-testid="stHorizontalBlock"] .stButton {{
        width: 16% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stHorizontalBlock"] button {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #1e293b !important;
        font-size: 10px !important;
        line-height: 1 !important;
    }}

    /* Card e promo stile blindato */
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

    /* Pulsante Rosa Standard */
    .main div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 4. LOGICA PAGINE (BLINDATE) ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:20px;">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div style="padding: 20px;"><div style="font-size: 24px; font-weight:800;">{saluto} 👋</div><div style="margin-top:10px;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:12px; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio"); st.rerun()

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:24px; text-align:center;">Diventa Fondatrice 🌸</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:14px;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua <b>prima Box</b> da usare entro 3 mesi!</div>""", unsafe_allow_html=True)
    with st.form("promo"):
        p = st.text_input("Peso (kg)")
        d = st.text_input("Dimensioni")
        if st.form_submit_button("INVIA RICHIESTA"): st.success("Richiesta inviata!")
    if st.button("Indietro"): vai("Home"); st.rerun()

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 20px; font-size: 13px; line-height: 1.6;"><b>1. Opzioni:</b> Standard o Premium.<br><b>2. Ricevi:</b> Nel locker più vicino.<br><b>3. Controllo 48h:</b> Contattaci per problemi.<br><b>4. Dopo 3 mesi:</b> Cambi taglia.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole"), ("NUVOLA ☁️", "box-nuvola")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;"><b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br><b>📍 Locker:</b> {st.session_state.dati['locker']}</div>""", unsafe_allow_html=True)
        if st.button("MODIFICA"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("ed"):
            n = st.text_input("Nome", st.session_state.dati['nome_genitore'])
            l = st.text_input("Locker", st.session_state.dati['locker'])
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "locker": l})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; text-align:center;">Siamo genitori che credono nel futuro. LoopBaby nasce per accompagnare questo viaggio con cura.</div><div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Garantire il meglio al tuo bebè e proteggere il pianeta.</div>""", unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE FISSA (MOBILE FRIENDLY) ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.button("🏠\nHome", on_click=vai, args=("Home",))
with c2: st.button("📖\nInfo", on_click=vai, args=("Info",))
with c3: st.button("📦\nBox", on_click=vai, args=("Box",))
with c4: st.button("🛍️\nShop", on_click=vai, args=("Vetrina",))
with c5: st.button("👤\nProfilo", on_click=vai, args=("Profilo",))
with c6: st.button("👋\nChi", on_click=vai, args=("ChiSiamo",))
