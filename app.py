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
        # Cache buster per caricare i dati istantaneamente senza ritardi
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                # Normalizziamo i nomi delle colonne per sicurezza
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except:
        return pd.DataFrame()

def registra_user(dati):
    # Salva i dati reali su Google Sheets via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    # Protezione delle password nell'Excel
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# ==========================================
# 3. CSS PROFESSIONALE (LOOK INTEGRALE 23:30)
# ==========================================
st.markdown(f"""
    <style>
    /* Rimozione elementi nativi Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    
    /* Font Lexend e Sfondo */
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}

    /* Header Custom con Logo */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 40px 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; text-shadow: 2px 2px 10px rgba(0,0,0,0.3); }}

    /* Bottoni Rosa LoopBaby */
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 22px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 52px; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
    }}

    /* Card Prodotto e Info */
    .card {{ border-radius: 30px; padding: 25px; margin: 10px 15px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 12px 35px rgba(0,0,0,0.04); }}
    .box-luna {{ background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; border: none !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 28px; font-weight: 900; margin-top: 10px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 20px; background: #FFFFFF; border-radius: 25px; margin-bottom: 15px; border-left: 8px solid #f43f5e; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 25px; border-radius: 25px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA DI ACCESSO BLOCCANTE
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("login_form"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password").strip()
            if st.form_submit_button("ENTRA"):
                db = carica_db()
                if not db.empty:
                    # Controllo incrociato email e password (con hashing)
                    match = db[(db['email'].str.lower() == e) & (db['password'] == hash_password(p))]
                    if not match.empty:
                        st.session_state.loggato = True
                        st.session_state.user_data = match.iloc[-1].to_dict()
                        st.rerun()
                    else: st.error("Email o Password errati")
                else: st.error("Database in caricamento... Riprova.")

    with t2:
        with st.form("reg_form"):
            re = st.text_input("La tua migliore Email")
            rp = st.text_input("Scegli Password", type="password")
            rn = st.text_input("Nome Genitore")
            rb = st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            rl = st.selectbox("Punto di ritiro preferito", ["Locker Milano", "Locker Roma", "Locker Torino", "InPost Locker"])
            if st.form_submit_button("CREA ACCOUNT"):
                if re and rp:
                    nuovo = {
                        "email": re.strip().lower(), "password": hash_password(rp),
                        "nome_genitore": rn, "nome_bambino": rb, "taglia": rt,
                        "data_inizio": str(date.today()), "scadenza": str(date.today() + timedelta(days=90)),
                        "locker": rl
                    }
                    registra_user(nuovo)
                    st.success("Registrato! Ora puoi fare il Login.")
                    st.balloons()
    st.stop()
    # ==========================================
# 5. APP DOPO IL LOGIN (THE FULL EXPERIENCE)
# ==========================================

# --- NAV BAR FISSA A 7 ICONE ---
st.markdown('<div style="margin-top:-30px;"></div>', unsafe_allow_html=True)
c_nav = st.columns(7)
menu_icons = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu_icons):
    with c_nav[i]:
        # Mostra il numero nel carrello se non è vuoto
        label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
        if st.button(label, key=f"nav_{pag}"): vai(pag)

st.divider()

# --- PAGINA: HOME (GRIGLIA AVANZATA CON TESTI PBA) ---
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma')
    
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 20px; padding: 0 10px; align-items: start;">
        <div>
            <div style="font-size:32px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {u_nome}! 👋</div>
            <div style="font-size:15px; color:#475569; margin-top:15px; font-weight:400; line-height:1.4;">
                L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.
            </div>
            <div style="margin-top:20px;">
                <div style="display:flex; align-items:center; gap:10px; font-size:12px; color:#64748b; margin-bottom:10px;">✨ Capi di qualità selezionati</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:12px; color:#64748b; margin-bottom:10px;">🔄 Cambi quando cresce</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:12px; color:#64748b;">🏠 Spedizione al tuo Locker</div>
            </div>
        </div>
        <div>{img_html}</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E; margin-top:30px;">
        <b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br>
        <p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p>
    </div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("Info")

# --- PAGINA: INFO (GUIDA E PATTO DEL 10) ---
elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli e Ricevi:</b> Scegli la tua Box e ricevila comodamente nel Locker scelto.<br><br>
            <b>2. Controllo Qualità:</b> Hai <b>48 ore</b> per controllare i capi. Se noti difetti, contattaci subito.<br><br>
            <b>3. Utilizzo:</b> Puoi tenere la Box per un massimo di <b>3 mesi</b>. Se cambia taglia prima, nessun problema!<br><br>
            <b>4. Rinnovo o Reso:</b> Decidi se scegliere una nuova Box o rendere quella attuale.<br><br>
            <b>🚚 Spedizioni:</b> Se decidi di continuare il ciclo, <b>paghiamo noi</b> andata e ritorno!
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">
        Il nostro è un patto di fiducia per l'ambiente:<br><br>
        <b>♻️ Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi della taglia successiva.<br><br>
        <b>👖 Sostituzione:</b> Se un capo si rovina, puoi sostituirlo con un tuo capo o pagare 5€.
    </div>""", unsafe_allow_html=True)

# Scrivimi "PARTE 3" per le Box, lo Shop e il Profilo!
# --- PAGINA: BOX (SCELTA TAGLIA E QUALITÀ) ---
elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    tg_u = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 CONFIGURATA PER TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
    
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Colori Neutri (Panna, Beige)"), 
                        ("SOLE ☀️", "box-sole", "Colori Vivaci e Fantasie"), 
                        ("NUVOLA ☁️", "box-nuvola", "Toni del Grigio e Bianco")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p style="font-size:13px; opacity:0.8;">{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=f"btn_{s}"): 
                st.session_state.carrello.append({"n": f"Box {s} ({tg_u})", "p": 19.90})
                st.toast(f"✅ {s} aggiunta!")
    else:
        st.markdown(f"""<div class="card box-premium">
            <h3>BOX PREMIUM 💎</h3>
            <p style="font-size:13px; opacity:0.9;">Capi nuovi o seminuovi dei migliori brand (Petit Bateau, Chicco, ecc.)</p>
            <div style="font-size:32px; font-weight:900; margin:10px 0;">29,90€</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Scegli Box Premium ({tg_u})"): 
            st.session_state.carrello.append({"n": f"Box Premium ({tg_u})", "p": 29.90})
            st.toast("✅ Box Premium aggiunta!")

# --- PAGINA: VETRINA SHOP (CAPI DA TENERE) ---
elif st.session_state.pagina == "Shop":
    st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:13px; color:#475569; padding:0 20px;">I capi acquistati qui <b>rimarranno a te per sempre</b>.</p>', unsafe_allow_html=True)
    
    st.selectbox("Filtra per taglia:", ["Tutte", "50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown('<div class="card">👕<br><b>Body Bio Loop</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi Body"): 
            st.session_state.carrello.append({"n": "Body Bio", "p": 9.90}); st.toast("Aggiunto!")
    with col_v2:
        st.markdown('<div class="card">🧤<br><b>Set Muffole</b><br><span class="prezzo-rosa">5,50€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi Set"): 
            st.session_state.carrello.append({"n": "Set Muffole", "p": 5.50}); st.toast("Aggiunto!")

# --- PAGINA: PROFILO (DATI REALI EXCEL) ---
elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Tuo Profilo 👤</h2>', unsafe_allow_html=True)
    u = st.session_state.user_data
    st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
        <b>👤 Nome Genitore:</b> {u.get('nome_genitore', '---')}<br>
        <b>📧 Email:</b> {u.get('email', '---')}<hr>
        <b>👶 Nome Bambino:</b> {u.get('nome_bambino', '---')}<br>
        <b>📏 Taglia Attiva:</b> {u.get('taglia', '---')}<hr>
        <b>📅 Data Iscrizione:</b> {u.get('data_inizio', '---')}<br>
        <b>📍 Punto Ritiro:</b> {u.get('locker', 'InPost Locker')}
    </div>""", unsafe_allow_html=True)
    
    if st.button("LOGOUT (ESCI)"): 
        st.session_state.loggato = False
        st.session_state.user_data = {}
        st.rerun()

# Scrivimi "PARTE 4" per il Carrello finale e il Chi Siamo emozionale!
# --- PAGINA: CARRELLO (CALCOLO DINAMICO) ---
elif st.session_state.pagina == "Carrello":
    st.markdown('<h2 style="text-align:center;">Il tuo Carrello 🛒</h2>', unsafe_allow_html=True)
    
    if not st.session_state.carrello:
        st.write("Il carrello è ancora vuoto. Inizia a comporre la tua Box!")
    else:
        totale = sum(item['p'] for item in st.session_state.carrello)
        for i, item in enumerate(st.session_state.carrello):
            st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; padding:15px; border-bottom:1px solid #EEE;'>
                    <div><b>{item['n']}</b></div>
                    <div style='color:#f43f5e; font-weight:800;'>{item['p']:.2f}€</div>
                </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='text-align:right; margin-top:20px; padding:20px;'>
                <span style='font-size:16px; color:#475569;'>TOTALE ORDINE:</span><br>
                <span style='font-size:32px; font-weight:900; color:#f43f5e;'>{totale:.2f}€</span>
            </div>""", unsafe_allow_html=True)
        
        if st.button("PROCEDI AL PAGAMENTO SICURO"):
            st.success("Reindirizzamento a Stripe in corso... 💳")
            # Qui andrà il tuo link Stripe ufficiale
            
        if st.button("SVUOTA CARRELLO", type="secondary"):
            st.session_state.carrello = []
            st.rerun()

# --- PAGINA: CHI SIAMO (TESTO PBA INTEGRALE) ---
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="text-align:center;">La nostra Storia ❤️</h2>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card" style="text-align:left; line-height:1.7; font-size:15px;">
            <b>Ma quanto è brutto quando quella tutina che ami già non entra più?</b> 💸<br><br>
            È una scena che si ripete in tutte le case: compri un capo bellissimo, glielo metti due volte e poi tocca già metterlo via perché è diventato piccolo. 
            Il risultato? Scatole che si accumulano, armadi che scoppiano e un sacco di soldi buttati.<br><br>
            <b>LoopBaby nasce proprio per dire basta a tutto questo.</b> 🛑<br><br>
            Vogliamo trasformare l’armadio dei nostri bimbi in un <b>giro infinito</b>: un sistema dove i vestiti non si fermano a prendere polvere, 
            ma passano di famiglia in famiglia, seguendo la crescita dei piccoli passo dopo passo. 🔄🌿<br><br>
            <i>Niente più sprechi, solo vestiti di qualità che continuano a vivere e a raccontare storie.</i>
        </div>
        <div class="obiettivo-pink">
            <b>Il nostro obiettivo?</b><br>
            Farti risparmiare più di 1000€ l'anno e lasciare un mondo più pulito ai nostri figli.
        </div>
    """, unsafe_allow_html=True)

# --- CHIUSURA LOGICA E NAVIGAZIONE ---
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

