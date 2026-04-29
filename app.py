import streamlit as st
from supabase import create_client, Client
from datetime import date
import base64
import os

# --- 1. CONNESSIONE SUPABASE (CHIAVE CORRETTA INSERITA) ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Welcome" if not st.session_state.user else "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

# --- 3. FUNZIONI LOGICHE ---
def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        aggiorna_dati_da_db()
        vai("Home"); st.rerun()
    except: st.error("Email o Password errati. Hai confermato la mail?")

def registrazione(email, password):
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("📩 Ti abbiamo inviato una mail! Clicca sul link per attivare l'account.")
    except Exception as e: st.error(f"Errore: {e}")

def aggiorna_dati_da_db():
    try:
        res = supabase.table("profili").select("*").eq("id", st.session_state.user.id).execute()
        if res.data: st.session_state.dati = res.data[0]
    except: pass

def salva_profilo_db(nuovi_dati):
    try:
        nuovi_dati["id"] = st.session_state.user.id
        supabase.table("profili").upsert(nuovi_dati).execute()
        st.session_state.dati = nuovi_dati
        st.success("✅ Dati salvati online!")
    except Exception as e: st.error(f"Errore database: {e}")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 4. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; background-position: center; height: 130px; display: flex; align-items: center; justify-content: center; margin-bottom: 35px; border-radius: 0 0 30px 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGICA PAGINE ---
if st.session_state.user is None:
    if st.session_state.pagina == "Welcome":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login"); st.rerun()
    else:
        st.markdown('<div class="header-custom"><div class="header-text">LOGIN</div></div>', unsafe_allow_html=True)
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login(e, p)
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Email "), st.text_input("Scegli Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"): registrazione(er, pr)
else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;"><div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; font-weight:600; color:#334155;">Cresciamo insieme, senza sprechi.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
        if st.button("Logout"): supabase.auth.sign_out(); st.session_state.user = None; st.rerun()

    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona 🔄</h2>', unsafe_allow_html=True)
        st.write("1. Scegli Box\n2. Controlla in 48h\n3. Usa per 3 mesi\n4. Rinnova o rendi")

    elif st.session_state.pagina == "Profilo":
        st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left;">
                <b>👤 Nome:</b> {st.session_state.dati.get('nome_genitore', '---')}<br>
                <b>👶 Bambino:</b> {st.session_state.dati.get('nome_bambino', '---')}<br>
                <b>📏 Taglia:</b> {st.session_state.dati.get('taglia', '---')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
        else:
            with st.form("edit"):
                n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
                nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
                tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                if st.form_submit_button("SALVA ONLINE"):
                    salva_profilo_db({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                    st.session_state.edit_mode = False; st.rerun()

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<h2 style="text-align:center;">Chi siamo? ❤️</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per ridurre gli sprechi e aiutarti a risparmiare.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag); st.rerun()
