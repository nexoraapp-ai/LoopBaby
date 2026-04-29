import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE & SICUREZZA
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except:
        return pd.DataFrame()

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
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
    st.session_state.carrello.append({"n": nome, "p": prezzo})
    st.toast(f"✅ {nome} aggiunto al carrello!")

# ==========================================
# 3. IMMAGINI E DESIGN CSS (FULL LOOK 23:30)
# ==========================================
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 100px !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 35px 35px; box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 34px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; text-shadow: 2px 2px 10px rgba(0,0,0,0.3); }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 22px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 52px; font-size: 16px; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 28px; padding: 22px; margin: 10px 15px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.03); }}
    .box-luna {{ background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; border: none !important; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 26px; font-weight: 900; margin-top: 10px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 18px; background: #FFFFFF; border-radius: 20px; margin-bottom: 15px; border-left: 6px solid #f43f5e; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA ACCESSO (LOGIN / REGISTRAZIONE)
# ==========================================
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px; color:#64748b;'>L'armadio circolare che cresce con il tuo bambino, senza sprechi di soldi e spazio.</p>", unsafe_allow_html=True)
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
                        df_db['p_clean'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        match = df_db[(df_db['email'].str.lower() == e) & (df_db['p_clean'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.warning("Nessun utente trovato.")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Scegli Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
                if st.form_submit_button("CREA ACCOUNT"):
                    nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "nome_bambino": rb, "taglia": rt, "data_inizio": str(date.today()), "scadenza": str(date.today() + timedelta(days=90)), "locker": rl}
                    registra_user(nuovo)
                    st.success("Registrato! Ora fai l'Accedi.")
                    st.balloons()

# ==========================================
# 5. APP DOPO IL LOGIN (THE FULL EXPERIENCE)
# ==========================================
else:
    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    c_nav = st.columns(7)
    menu_icons = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu_icons):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- PAGINA: HOME (GRIGLIA AVANZATA) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_m = st.session_state.user.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 15px; padding: 0 10px; align-items: center;">
            <div>
                <div style="font-size:32px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {nome_m}! 👋</div>
                <div style="font-size:15px; color:#475569; margin-top:10px; font-weight:400;">Il tuo armadio circolare è pronto. Quale box scegliamo oggi?</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e; margin-top:25px;">'
                    '<span style="font-size:20px;">✨</span> <b>Promo Mamme Fondatrici</b><br>'
                    'Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa alla Promo"): vai("Info")

    # --- PAGINA: INFO LOGISTICA ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida LoopBaby 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA LOCKER</span><br>Riceverai la tua Box entro 3-5 giorni lavorativi nel Locker InPost scelto. Ritira quando vuoi, 24/7.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Quando i vestiti stringono, ordina la taglia nuova. Ti spediamo la nuova Box e rendi la vecchia nello stesso momento.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE PROFESSIONALE</span><br>Ogni capo viene sanificato ad alte temperature con prodotti certificati per neonati prima di ogni viaggio.</div>
        <div class="info-box"><span class="accent">📦 RESO GRATUITO</span><br>Se passi alla taglia successiva, il reso è sempre incluso. Zero pensieri, zero sprechi.</div>
        """, unsafe_allow_html=True)

    # --- PAGINA: BOX (COLORATE) ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la tua Box 📦</h2>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f'<div class="card box-luna"><h3>BOX LUNA 🌙</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button("Scegli Luna"): aggiungi_al_carrello("Box Luna 🌙", 19.90)
        with col_b:
            st.markdown(f'<div class="card box-sole"><h3>BOX SOLE ☀️</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button("Scegli Sole"): aggiungi_al_carrello("Box Sole ☀️", 19.90)

    # --- PAGINA: SHOP VETRINA ---
    elif st.session_state.pagina == "Shop":
        st.markdown("<h2 style='text-align:center;'>Vetrina Extra 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove (3 pezzi)</b><br><div class="prezzo-rosa">12,90€</div></div>', unsafe_allow_html=True)
        if st.button("Aggiungi Body 🎁"): aggiungi_al_carrello("Body Bio Loop", 12.90)

    # --- PAGINA: PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Tuo Profilo 👤</h2>", unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Genitore:</b> {u.get('nome_genitore')}<br>
            <b>👶 Bambino:</b> {u.get('nome_bambino')}<br>
            <b>📏 Taglia Attiva:</b> {u.get('taglia')}<br>
            <b>📍 Locker:</b> {u.get('locker')}<hr>
            <b>📅 Data Inizio:</b> {u.get('data_inizio')}<br>
            <b>📅 Prossimo Cambio:</b> {u.get('scadenza', 'Da definire')}
        </div>""", unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")

    # --- PAGINA: CARRELLO ---
    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Il tuo Ordine 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello:
            st.warning("Il carrello è vuoto. Scegli una Box!")
        else:
            totale = sum(item['p'] for item in st.session_state.carrello)
            for item in st.session_state.carrello:
                st.write(f"✅ {item['n']} — {item['p']}€")
            st.divider()
            st.markdown(f"<div style='text-align:right; font-size:24px; font-weight:800; color:#f43f5e;'>TOTALE: {totale:.2f}€</div>", unsafe_allow_html=True)
            if st.button("PROCEDI AL PAGAMENTO SICURO"):
                st.success("Reindirizzamento a Stripe...")

    # --- PAGINA: CHI SIAMO (EMOZIONALE) ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="text-align:left; line-height:1.7; font-size:15px;">
            <b>Basta sacchi di vestiti ammassati in soffitta o soldi sprecati per capi messi due volte.</b><br><br>
            Siamo un team di genitori che ha deciso di rivoluzionare l'armadio dei più piccoli. Abbiamo vissuto sulla nostra pelle lo stress di dover ricomprare tutto ogni tre mesi.<br><br>
            <b>LoopBaby</b> nasce per questo: creare un "giro infinito" di abbigliamento di alta qualità. I capi viaggiano di famiglia in famiglia, seguendo la crescita dei bimbi senza pesare sul portafoglio dei genitori e sull'ambiente.<br><br>
            <i>Insieme, rendiamo la crescita dei nostri figli più leggera e sostenibile.</i> 🌿
        </div>
        """, unsafe_allow_html=True)
