import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import datetime, timedelta

# --- 1. CONNESSIONE SUPABASE (VERSIONE STABILE) ---
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def init_supabase():
    return create_client(URL_DB, KEY_DB)

supabase = init_supabase()

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        display: block !important; white-space: nowrap !important; border: none !important;
        box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA PAGINE ---

# LOGIN E REGISTRAZIONE
if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("login"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                        st.session_state.user = res.user
                        d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
                        if d.data: st.session_state.dati = d.data
                        vai("Home")
                    except: st.error("Email o Password errati.")
        with t2:
            with st.form("reg"):
                er, pr = st.text_input("Email "), st.text_input("Scegli Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"):
                    try:
                        supabase.auth.sign_up({"email": er, "password": pr})
                        st.success("📩 Mail inviata! Conferma l'account per entrare.")
                    except Exception as err: st.error(f"Errore tecnico: {err}")

# APP DOPO LOGIN
else:
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_u = st.session_state.dati.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
            <div>
                <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {nome_u}! 👋</div>
                <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa ora"): vai("PromoDettaglio")

    elif st.session_state.pagina == "PromoDettaglio":
        st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
        with st.form("promo"):
            p, d = st.text_input("Peso pacco (kg)"), st.text_input("Dimensioni")
            if st.form_submit_button("INVIA RICHIESTA"): st.success("Richiesta inviata!")
        if st.button("Torna in Home"): vai("Home")

    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona 🔄</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; font-size:14px;">1. <b>Scegli</b> box.<br>2. <b>Ricevi</b> e controlla qualità.<br>3. <b>Usa</b> per 3 mesi.<br>4. <b>Rendi</b> o cambia taglia.<br>📍 <b>Patto del 10:</b> rendi 10 per averne 10.</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        st.markdown('<h2 style="text-align:center;">Le tue Box 📦</h2>', unsafe_allow_html=True)
        for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", 19.90)

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left;">
                <b>👤 Nome:</b> {st.session_state.dati.get('nome_genitore', '---')}<br>
                <b>👶 Bambino:</b> {st.session_state.dati.get('nome_bambino', '---')}<hr>
                <b>📏 Taglia:</b> {st.session_state.dati.get('taglia', '---')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
            if st.button("Logout"): st.session_state.user = None; vai("Welcome")
        else:
            with st.form("p"):
                n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
                nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
                tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
                if st.form_submit_button("SALVA"):
                    nuovi = {"id": st.session_state.user.id, "nome_genitore": n, "nome_bambino": nb, "taglia": tg}
                    supabase.table("profili").upsert(nuovi).execute()
                    st.session_state.dati = nuovi
                    st.session_state.edit_mode = False; st.rerun()

    elif st.session_state.pagina == "Carrello":
        st.markdown("## Carrello 🛒")
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            tot = sum(i['prezzo'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            st.markdown(f"### Totale: {tot:.2f}€")
            if st.button("PAGA ORA"): st.info("Link Stripe in arrivo...")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori come te.</b></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 20px; font-size:14px; color:#475569; text-align:center;">LoopBaby nasce per eliminare lo spreco e farti risparmiare più di 1000€ l\'anno.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
