import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import base64
import os

# --- 1. MOTORE DATABASE (CON REFRESCH FORZATO) ---
API_URL = "https://sheetdb.io"

def carica_db_fresco():
    try:
        # Il trucco: aggiungiamo un numero casuale all'URL per distruggere la cache di SheetDB
        flash_url = f"{API_URL}?t={datetime.now().strftime('%H%M%S')}"
        res = requests.get(flash_url, timeout=10)
        if res.status_code == 200:
            dati = res.json()
            if dati and len(dati) > 0:
                df = pd.DataFrame(dati)
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def aggiungi_utente(nuovo):
    headers = {"Content-Type": "application/json"}
    return requests.post(API_URL, json={"data": [nuovo]}, headers=headers, timeout=15).status_code

def aggiorna_utente(email, dati):
    return requests.patch(f"{API_URL}/email/{email}", json={"data": dati}).status_code

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

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
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db_fresco()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        # Pulizia per sicurezza
                        df_globale['email_clean'] = df_globale['email'].astype(str).str.strip().str.lower()
                        df_globale['pass_clean'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        m = df_globale[(df_globale['email_clean'] == e) & (df_globale['pass_clean'] == p)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati.")
                    else:
                        st.warning("Il sistema si sta aggiornando. Registrati se non l'hai fatto!")
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Tua migliore Email"), st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Non impostato"}
                    if aggiungi_utente(nuovo) == 201:
                        st.success("✅ REGISTRATO! Ora aspetta 5 secondi e fai l'accesso.")
                        st.balloons()
else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio infinito è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Dona ora"): vai("Info")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida al Servizio 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 Locker InPost</span><br>Consegna in 3-5 giorni lavorativi. Ritira 24/7 nel Locker più comodo per te.</div>
        <div class="info-box"><span class="accent">🔄 Cambio Taglia</span><br>Quando i vestiti diventano piccoli, ordina la nuova Box: lo scambio avviene nello stesso momento.</div>
        <div class="info-box"><span class="accent">🧼 Igiene Professionale</span><br>Ogni capo viene sanificato ad alte temperature con prodotti certificati per neonati.</div>
        """, unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome'))
            nb = st.text_input("Nome Bambino", st.session_state.user.get('bimbo'))
            tg = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm"])
            loc = st.text_input("Locker InPost preferito", st.session_state.user.get('locker'))
            if st.form_submit_button("SALVA"):
                aggiorna_utente(st.session_state.user['email'], {"nome": n, "bimbo": nb, "taglia": tg, "locker": loc})
                st.session_state.user.update({"nome": n, "bimbo": nb, "taglia": tg, "locker": loc})
                st.success("Profilo aggiornato!")
        if st.button("Logout"): 
            st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra storia ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;"><b>Basta vestiti ammassati in soffitta.</b><br><br>Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia. Risparmi spazio, soldi e proteggi il pianeta.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE FISSA
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
