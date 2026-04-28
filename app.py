import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. CONFIGURAZIONE E MEMORIA ---
DB_FILE = "db_loopbaby.json"
st.set_page_config(page_title="LoopBaby", layout="centered")

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

# --- 2. STATO DELL'APP ---
if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    # Se il nome genitore è vuoto, mostra Welcome, altrimenti Home
    st.session_state.pagina = "Welcome" if not st.session_state.dati["nome_genitore"] else "Home"
if "carrello" not in st.session_state:
    st.session_state.carrello = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_bg = get_base64("logo.png")
img_data = get_base64("bimbo.jpg")

# --- 3. CSS "PUBLISH READY" ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 30px; border-radius: 0 0 35px 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-text {{ color: white; font-size: 34px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); text-transform: uppercase; }}

    /* Pulsanti Moderni con Ombra */
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 20px !important;
        width: 100% !important; font-weight: 800 !important; border: none !important;
        padding: 12px !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.3) !important;
        transition: all 0.3s ease;
    }}
    div.stButton > button:active {{ transform: scale(0.98); box-shadow: 0 2px 5px rgba(244, 63, 94, 0.2) !important; }}

    .card {{ 
        border-radius: 25px; padding: 20px; margin: 15px 20px; 
        border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 26px; font-weight: 900; margin-top: 10px; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA PAGINE ---

# A. LANDING PAGE DI BENVENUTO
if st.session_state.pagina == "Welcome":
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in famiglia! 🌸</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; padding: 0 30px;'>L'app che trasforma l'armadio del tuo bambino in un cerchio infinito di amore e risparmio.</p>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        nome = st.text_input("Come ti chiami?", placeholder="Inserisci il tuo nome")
        st.markdown("<p style='font-size:12px; color:gray;'>Iniziamo con il tuo nome per personalizzare la tua esperienza.</p>", unsafe_allow_html=True)
        if st.form_submit_button("INIZIA L'AVVENTURA"):
            if nome:
                st.session_state.dati["nome_genitore"] = nome
                salva_dati_su_file(st.session_state.dati)
                vai("Home"); st.rerun()
            else: st.error("Per favore, inserisci il tuo nome.")

# B. HOME PAGE
elif st.session_state.pagina == "Home":
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    u_nome = st.session_state.dati['nome_genitore'].split()[0]
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo" style="width:100%; border-radius:25px;">' if img_data else "👶"
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"<div style='font-size:28px; font-weight:800;'>Ciao {u_nome}! 👋</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:14px; font-weight:600; color:#334155;'>Cresciamo insieme, un capo alla volta.</div>", unsafe_allow_html=True)
        st.markdown("<br><div style='font-size:11px;'>🔥 Qualità garantita<br>🔄 Cambi infiniti<br>💰 Risparmio assicurato</div>", unsafe_allow_html=True)
    with col2: st.markdown(img_html, unsafe_allow_html=True)
    
    st.markdown("""<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Mamme Fondatrici</b><br>Dona 10 capi, ricevi una Box OMAGGIO!</div>""", unsafe_allow_html=True)
    if st.button("Partecipa ora"): vai("PromoDettaglio"); st.rerun()

# C. CARRELLO E PAGAMENTO
elif st.session_state.pagina == "Carrello":
    st.markdown('<div class="header-custom"><div class="header-text">CARRELLO</div></div>', unsafe_allow_html=True)
    if not st.session_state.carrello:
        st.warning("Il carrello è ancora vuoto!")
        if st.button("Torna allo shopping"): vai("Home"); st.rerun()
    else:
        totale = 0
        for item in st.session_state.carrello:
            st.markdown(f"<div style='display:flex; justify-content:space-between; padding:15px; background:white; border-radius:15px; margin-bottom:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'><b>{item['nome']}</b> <span>{item['prezzo']:.2f}€</span></div>", unsafe_allow_html=True)
            totale += item['prezzo']
        
        st.markdown(f"<h2 style='text-align:right;'>Totale: {totale:.2f}€</h2>", unsafe_allow_html=True)
        
        st.info("💳 Pagamento Sicuro tramite Stripe/PayPal")
        if st.button("PAGA ORA"):
            # Qui si inserirebbe l'integrazione API reale. 
            # Per ora simuliamo il reindirizzamento al gateway.
            st.warning("Reindirizzamento al modulo di pagamento sicuro...")
            st.success("Pagamento completato con successo! (Simulazione)")
            st.session_state.carrello = []
            
        if st.button("Svuota Carrello"): st.session_state.carrello = []; st.rerun()
        if st.button("Continua Shopping"): vai("Home"); st.rerun()

# [Le altre pagine Info, Box, Vetrina, Profilo, ChiSiamo rimangono uguali ma con CSS migliorato]
# ... (inserire qui il resto del codice delle sezioni precedenti)

# --- 5. NAV BAR FISSA ---
if st.session_state.pagina != "Welcome":
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            # Aggiungiamo un badge per il carrello
            label = f"{icon}"
            if pag == "Carrello" and len(st.session_state.carrello) > 0:
                label = f"🛒({len(st.session_state.carrello)})"
            if st.button(label, key=f"nav_{pag}"): vai(pag); st.rerun()
