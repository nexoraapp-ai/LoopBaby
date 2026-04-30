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
        # Cache buster estremo per caricare i dati istantaneamente
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
    # Funzione per salvare su Google Sheets via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
    # Per modificare il profilo
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
    st.toast(f"✅ {nome} aggiunto!")

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
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}

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
        border: none !important; height: 50px; font-size: 16px; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 18px; background: #FFFFFF; border-radius: 20px; margin-bottom: 15px; border-left: 6px solid #f43f5e; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
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
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_db.empty:
                        hp = hash_password(p)
                        df_db['p_clean'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        match = df_db[(df_db['email'].str.lower() == e) & (df_db['p_clean'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
                    else: st.warning("Nessun utente trovato nel database.")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Scegli Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
                if st.form_submit_button("CREA ACCOUNT"):
                    if re and rp:
                        nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "nome_bambino": rb, "taglia": rt, "data_inizio": str(date.today()), "scadenza": "", "locker": rl}
                        registra_user(nuovo)
                        st.success("Registrato! Ora fai l'Accedi.")
                        st.balloons()

# ==========================================
# 5. APP DOPO IL LOGIN (THE FULL EXPERIENCE)
# ==========================================
else:
    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    c_nav = st.columns(7)
    menu_icons = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu_icons):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- PAGINA: HOME (GRIGLIA AVANZATA PBA) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        u_nome = st.session_state.user.get('nome_genitore', 'Mamma').split()[0]
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
            <div>
                <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
                <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
                <div style="margin-top:15px;">
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">👶 Capi di qualità selezionati</div>
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">🔄 Cambi quando cresce</div>
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">💰 Risparmi più di 1000€ l’anno</div>
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">🏠 Scegli il locker più vicino a te</div>
                </div>
            </div>
            <div>{img_html}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
        if st.button("Partecipa e ricevi l'etichetta"): vai("Info")

    # --- PAGINA: INFO (IL TESTO INTEGRALE DI IERI) ---
    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
        st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli e Ricevi:</b> Scegli la tua Box e ricevila nel Locker scelto.<br><br>
            <b>2. Controllo Qualità:</b> Hai 48 ore per controllare i capi. Se noti difetti, contattaci subito.<br><br>
            <b>3. Utilizzo:</b> Puoi tenere la Box per un massimo di 3 mesi.<br><br>
            <b>4. Rinnovo o Reso:</b> Decidi se scegliere una nuova Box o rendere quella attuale.<br><br>
            <b>🚚 Spedizioni:</b> Se decidi di continuare il ciclo, paghiamo noi sia l'andata che il ritorno!</div>""", unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
        st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">Il nostro è un patto di fiducia per l'ambiente:<br><br><b>♻️ Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi. <br><br><b>👖 Sostituzione:</b> Se un capo viene smarrito o si rovina, puoi sostituirlo con un tuo capo oppure pagare una penale di 5€.</div>""", unsafe_allow_html=True)

    # --- PAGINA: BOX (COLORATE) ---
    elif st.session_state.pagina == "Box":
        st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
        tg_u = st.session_state.user.get('taglia', '---')
        st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 CONFIGURATA PER TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", 19.90)

    # --- PAGINA: SHOP VETRINA ---
    elif st.session_state.pagina == "Vetrina":
        st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi 🎁"): aggiungi_al_carrello("Body Bio LoopLove", 9.90)

    # --- PAGINA: PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {u.get('nome_genitore')}<br>
            <b>📧 Email:</b> {u.get('email')}<br>
            <b>👶 Bambino:</b> {u.get('nome_bambino')}<br>
            <b>📏 Taglia:</b> {u.get('taglia')}<br>
            <b>📍 Locker:</b> {u.get('locker')}
        </div>""", unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")

    # --- PAGINA: CHI SIAMO (TESTO PBA) ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano.<br><br>
            Per questo abbiamo creato LoopBaby.
        </div><div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Risparmi più di 1000€ l'anno e lasci un mondo migliore ai nostri figli.</div>""", unsafe_allow_html=True)

    # --- PAGINA: CARRELLO ---
    elif st.session_state.pagina == "Carrello":
        st.markdown('<h2 style="text-align:center;">Il tuo Carrello 🛒</h2>', unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Il carrello è vuoto.")
        else:
            totale = sum(item['prezzo'] for item in st.session_state.carrello)
            for item in st.session_state.carrello:
                st.write(f"✅ {item['nome']} - {item['prezzo']:.2f}€")
            st.markdown(f"<h3 style='text-align:right;'>Totale: {totale:.2f}€</h3>", unsafe_allow_html=True)
            if st.button("PROCEDI AL PAGAMENTO"): st.success("Pagamento sicuro..."); st.session_state.carrello = []
