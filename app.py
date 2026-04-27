import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA (DATABASE JSON) ---
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

# --- 2. CONFIGURAZIONE SIDEBAR (LE 3 LINETTE) ---
# Impostiamo il layout centrato e il menu laterale inizialmente chiuso
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# MENU LATERALE (Accessibile dalle 3 linette in alto a SX)
st.sidebar.markdown("## 🍼 Menu LoopBaby")
pagina = st.sidebar.radio("Vai a:", 
    ["Home", "Info", "Scegli la Box", "Shop Vetrina", "Il tuo Profilo", "Chi Siamo", "Contatti"])

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (BEIGE + HEADER PANORAMICO + STYLE MENU) ---
st.markdown(f"""
    <style>
    /* Nasconde header Streamlit ma tiene vive le 3 linette */
    [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    header {{background-color: transparent !important;}}
    
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* Pulsante 3 linette (Hamburger) in alto a SX rosa e tondo */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        left: 15px !important;
        top: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }}

    /* HEADER PANORAMICO CON LOGO.PNG */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; }}

    /* Stili Card e Elementi Blindati */
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 4. LOGICA PAGINE ---

if pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px; padding: 0 20px;">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split() if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div style="padding: 0 20px;"><div style="font-size: 28px; font-weight: 800;">{saluto} 👋</div><div style="font-size: 15px; margin-bottom: 10px; font-weight:600; color:#334155;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div>""", unsafe_allow_html=True)
    st.markdown(f"{img_html}", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size: 13px; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box Standard o Premium. <br><br>
            <b>2. Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi, per problemi contattaci nel menu laterale.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:13px;"><b>📍 La Regola del 10:</b> Rendi lo stesso numero di capi ricevuti. Se un capo manca, vale lo scambio <b>Jeans x Jeans</b> o 5€ di penale.</div>', unsafe_allow_html=True)

elif pagina == "Scegli la Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole"), ("NUVOLA ☁️", "box-nuvola")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

elif pagina == "Shop Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding:0 20px; font-size:14px; color:#475569;">I capi acquistati in Vetrina rimarranno nell\'armadio del tuo bimbo <b>per sempre</b>.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Cotone Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif pagina == "Il tuo Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📅 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📍 Locker scelto:</b><br><span style="color:#0d9488; font-weight:800;">{st.session_state.dati['locker']}</span>
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit"):
            n = st.text_input("Nome Genitore", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            l = st.text_input("Indirizzo Locker", st.session_state.dati['locker'])
            if st.form_submit_button("SALVA E BLOCCA DATI"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "locker": l})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif pagina == "Chi Siamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori che credono nel futuro.</b></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; line-height:1.7; text-align:center;">
            Sappiamo che ogni bambino è un miracolo e che vederlo crescere è l'emozione più bella del mondo.<br><br>
            Proprio perché i nostri piccoli crescono così in fretta, abbiamo creato <b>LoopBaby</b>: un modo per accompagnare i loro primi passi con capi di altissima qualità, riducendo gli sprechi e rispettando il pianeta che un giorno esploreranno.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Offrirti vestiti di qualità, farti risparmiare e lasciare un mondo migliore ai nostri figli.</div>', unsafe_allow_html=True)

elif pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background:#FFF5F5; border-color:#FECDD3;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it<br>🕒 Lun-Ven 9:00 - 18:00</div>""", unsafe_allow_html=True)
