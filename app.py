import streamlit as st
import os
import base64
import json
import requests
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE (SHEETDB) ---
SHEETDB_URL = "https://sheetdb.io"

def registra_utente(email, password, nome, bimbo, taglia, locker):
    payload = {"data": [{
        "email": email.strip().lower(),
        "password": password,
        "nome_genitore": nome,
        "nome_bambino": bimbo,
        "taglia": taglia,
        "data_inizio": str(date.today()),
        "scadenza": str(date.today() + timedelta(days=90)),
        "locker": locker
    }]}
    r = requests.post(SHEETDB_URL, json=payload, headers={"Content-Type": "application/json"})
    return r.status_code

def login(email, password):
    try:
        t = datetime.now().microsecond
        r = requests.get(f"{SHEETDB_URL}?t={t}")
        utenti = r.json()
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == str(password):
                return u
    except: pass
    return None

# --- 2. STATO APP ---
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")
if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast(f"✅ {n} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS TOTALE (Full Design 23:30) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; height: 48px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN / REGISTER ---
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("l"):
            e, p = st.text_input("Email"), st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                u = login(e, p)
                if u: st.session_state.loggato, st.session_state.user_data = True, u; st.rerun()
                else: st.error("Dati errati")
    with t2:
        with st.form("r"):
            re, rp = st.text_input("Email"), st.text_input("Scegli Password")
            rn, rb = st.text_input("Tuo Nome"), st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
            if st.form_submit_button("CREA ACCOUNT"):
                if registra_utente(re, rp, rn, rb, rt, rl) == 201: st.success("Registrato! Accedi ora.")
    st.stop()
    # --- 5. LOGICA PAGINE (DOPO IL LOGIN) ---
st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div>
            <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
            <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
            <div style="margin-top:15px;">
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">👶 Capi di qualità selezionati</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">🔄 Cambi quando cresce</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">💰 Risparmi più di 1000€ l’anno</div>
            </div>
        </div>
        <div>{img_html}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio")

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
    with st.form("promo_f"):
        p = st.text_input("Peso stimato (kg)")
        d = st.text_input("Dimensioni pacco (es. 30x30x40)")
        lock = st.selectbox("Dove porterai il pacco?", ["Locker Esselunga", "InPost Point", "Poste Italiane"])
        if st.form_submit_button("INVIA E RICHIEDI ETICHETTA"): st.success("Richiesta inviata! Ti contatteremo presto.")
    if st.button("Torna in Home"): vai("Home")

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
        <b>1. Scegli e Ricevi:</b> Scegli la tua Box e ricevila comodamente nel Locker scelto.<br><br>
        <b>2. Controllo Qualità:</b> Hai 48 ore per controllare i capi. Se noti difetti, contattaci subito.<br><br>
        <b>3. Utilizzo:</b> Puoi tenere la Box per un massimo di 3 mesi.<br><br>
        <b>4. Rinnovo o Reso:</b> Decidi se scegliere una nuova Box o rendere quella attuale.<br><br>
        <b>🚚 Spedizioni:</b> Se continui il ciclo, <b>paghiamo noi</b> andata e ritorno!</div>""", unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">Il nostro è un patto di fiducia per l'ambiente:<br><br><b>♻️ Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi.<br><br><b>👖 Sostituzione:</b> Se un capo si rovina, puoi sostituirlo con un tuo capo o pagare 5€.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    tg_u = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 CONFIGURATA PER TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi(s, 19.90)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Premium"): aggiungi("Box Premium", 29.90)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
        <b>👤 Nome:</b> {u.get('nome_genitore')}<br><b>📧 Email:</b> {u.get('email')}<hr>
        <b>👶 Bambino:</b> {u.get('nome_bambino')}<br><b>📏 Taglia:</b> {u.get('taglia')}<br>
        <b>📍 Locker:</b> {u.get('locker')}</div>""", unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.loggato = False; st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
        Ma quanto è brutto quando quella tutina che ami già non entra più? 💸<br><br>
        LoopBaby nasce per trasformare l’armadio dei nostri bimbi in un <b>giro infinito</b>: un sistema dove i vestiti passano di famiglia in famiglia.
    </div><div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Risparmio e un futuro migliore per i nostri figli.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Carrello":
    st.markdown('<h2 style="text-align:center;">Carrello 🛒</h2>', unsafe_allow_html=True)
    if not st.session_state.carrello: st.write("Il carrello è vuoto.")
    else:
        totale = sum(i['prezzo'] for i in st.session_state.carrello)
        for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
        st.markdown(f"<h3 style='text-align:right;'>Totale: {totale:.2f}€</h3>", unsafe_allow_html=True)

# --- 6. NAV BAR FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c = st.columns(7)
m = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(m):
    with c[i]:
        lbl = f"{icon}({len(st.session_state.carrello)})" if pag=="Carrello" and st.session_state.carrello else icon
        if st.button(lbl, key=f"nav_{pag}"): vai(pag)

