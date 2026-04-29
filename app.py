import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE & SICUREZZA
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Cache buster per evitare di leggere dati vecchi
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome','bimbo','taglia','inizio','scadenza','locker'])
    except:
        return pd.DataFrame()

def registra_user(dati):
    # Salvataggio su Google Sheets via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
    # Aggiornamento riga esistente tramite email
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto al carrello!")

# ==========================================
# 3. IMMAGINI E DESIGN CSS (FINALE IERI)
# ==========================================
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    /* Rimozione elementi Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    
    /* Font e Sfondo */
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 100px !important; }}

    /* Header LoopBaby */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 30px; border-radius: 0 0 35px 35px; box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }}
    .header-text {{ color: white; font-size: 34px; font-weight: 800; letter-spacing: 4px; text-shadow: 2px 2px 10px rgba(0,0,0,0.4); text-transform: uppercase; }}

    /* Pulsanti */
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 22px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 50px; font-size: 16px; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.25);
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(244, 63, 94, 0.35); }}

    /* Card Prodotto e Info */
    .card {{ border-radius: 28px; padding: 22px; margin-bottom: 18px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }}
    .box-luna {{ background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; }} 
    .prezzo-rosa {{ color: #f43f5e; font-size: 26px; font-weight: 900; margin-top: 10px; }}
    
    /* Info Box con Bordo */
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 18px; background: #FFFFFF; border-radius: 20px; margin-bottom: 15px; border-left: 6px solid #f43f5e; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA DI ACCESSO & NAVIGAZIONE
# ==========================================
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>L'armadio infinito 🔄</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px; color:#64748b;'>Abbigliamento di qualità che cresce con il tuo bambino, senza sprechi.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    
    elif st.session_state.pagina == "Login":
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        with tab1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_db.empty:
                        hp = hash_password(p)
                        # Fix per interpretazione numeri in Excel (togliamo il .0)
                        df_db['p_clean'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        m = df_db[(df_db['email'].str.lower() == e) & (df_db['p_clean'] == hp)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati.")
                    else: st.warning("Nessun utente trovato. Registrati!")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Locker Preferito", ["InPost", "Esselunga", "Poste Italiane"])
                if st.form_submit_button("CREA ACCOUNT"):
                    if re and rp:
                        nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome": rn, "bimbo": rb, "taglia": rt, "inizio": str(date.today()), "scadenza": str(date.today()+timedelta(days=90)), "locker": rl}
                        registra_user(nuovo)
                        st.success("Registrato! Ora fai l'Accedi.")
                        st.balloons()

# ==========================================
# 5. APP DOPO LOGIN
# ==========================================
else:
    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    c_nav = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- PAGINA: HOME ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_m = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 15px; padding: 0 10px; align-items: center;">
            <div>
                <div style="font-size:30px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {nome_m}! 👋</div>
                <div style="font-size:15px; color:#475569; margin-top:10px; font-weight:400;">Il tuo armadio circolare è pronto per essere esplorato.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e; margin-top:25px;">'
                    '<span style="font-size:20px;">✨</span> <b>Promo Mamme Fondatrici</b><br>'
                    'Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Scopri di più sulla Promo"): vai("Info")

    # --- PAGINA: INFO ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida LoopBaby 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Riceverai la Box entro 3-5 giorni nel Locker InPost scelto. Il ritiro è disponibile 24/7.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Quando i vestiti stringono, ordina la taglia nuova. Consegniamo la nuova e ritiriamo la vecchia nello stesso momento.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE GARANTITA</span><br>Ogni capo viene sanificato professionalmente ad alte temperature con prodotti certificati.</div>
        <div class="info-box"><span class="accent">📦 RESO FACILE</span><br>Vuoi fermarti? Metti tutto nella scatola originale e prenota il ritiro. Se continui, è GRATIS.</div>
        """, unsafe_allow_html=True)

    # --- PAGINA: BOX ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la tua Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("BOX LUNA 🌙", "box-luna", 19.90), ("BOX SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div style="font-size:14px; opacity:0.8;">10-12 Capi di Qualità</div><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Seleziona {s}", key=s): aggiungi_al_carrello(s, p)

    # --- PAGINA: VETRINA ---
    elif st.session_state.pagina == "Vetrina":
        st.markdown("<h2 style='text-align:center;'>Shop LoopBaby 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove</b><br><div class="prezzo-rosa">9,90€</div></div>', unsafe_allow_html=True)
        if st.button("Aggiungi al carrello 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

    # --- PAGINA: PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Il tuo Profilo 👤</h2>", unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome Genitore:</b> {u.get('nome')}<br>
            <b>👶 Nome Bambino:</b> {u.get('bimbo')}<br>
            <b>📏 Taglia Attiva:</b> {u.get('taglia')}<br>
            <b>📍 Locker:</b> {u.get('locker')}<hr>
            <b>📅 Inizio:</b> {u.get('inizio')}<br>
            <b>📅 Prossimo Cambio:</b> {u.get('scadenza')}
        </div>""", unsafe_allow_html=True)
        if st.button("LOGOUT"): st.session_state.user = None; vai("Welcome")

    # --- PAGINA: CARRELLO ---
    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Il tuo Ordine 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Il carrello è ancora vuoto.")
        else:
            totale = sum(i['prezzo'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            st.markdown(f"<div class='prezzo-rosa' style='text-align:right;'>TOTALE: {totale:.2f}€</div>", unsafe_allow_html=True)
            if st.button("PROCEDI AL PAGAMENTO SICURO"): st.success("Link Stripe in arrivo!")

    # --- PAGINA: CHI SIAMO ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown("""<div class="card" style="text-align:left; line-height:1.7; font-size:15px;">
            <b>Basta sacchi di vestiti ammassati in soffitta.</b><br><br>
            Siamo genitori che hanno deciso di dire basta allo spreco di soldi e spazio. 
            Abbiamo creato <b>LoopBaby</b> per far viaggiare la qualità di famiglia in famiglia, 
            seguendo la crescita dei piccoli senza che nulla venga buttato.<br><br>
            <i>Insieme proteggiamo il pianeta per i nostri figli.</i> 🌿</div>""", unsafe_allow_html=True)
