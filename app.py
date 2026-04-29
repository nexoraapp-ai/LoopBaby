import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (IL TUO MOTORE EXCEL) ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        timestamp = datetime.now().timestamp()
        res = requests.get(f"{API_URL}?t={timestamp}")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                # Pulizia nomi colonne per evitare KeyError
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame()
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    requests.post(API_URL, json={"data": [nuovo]})

def aggiorna_utente(email, dati):
    # Aggiorna basandosi sulla colonna 'email'
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

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

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS TOTALE (Design Originale + Colori Box + Fix Nav) ---
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
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; text-align: center; margin: 15px; font-size: 13px; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db()

# --- 4.1 WELCOME, LOGIN E REGISTRAZIONE ---
if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("login_f"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty and 'email' in df_globale.columns:
                        match = df_globale[(df_globale['email'].str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not match.empty:
                            st.session_state.user = match.iloc[0].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.error("Database in caricamento, riprova.")
        with t2:
            with st.form("reg_f"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if not df_globale.empty and er.lower() in df_globale['email'].str.lower().values:
                        st.error("Esiste già!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er, "password": str(pr), "nome genitore": "Mamma", "nome bambino": "---", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                        aggiungi_utente(nuovo)
                        st.success("Creato! Ora fai l'accesso.")

# --- 4.2 APP DOPO IL LOGIN ---
else:
    # AVVISO SCADENZA (Sempre in alto)
    scad_str = str(st.session_state.user.get('scadenza', ''))
    if scad_str != 'nan' and scad_str != '':
        try:
            giorni = (datetime.strptime(scad_str, "%Y-%m-%d") - datetime.now()).days
            if 0 <= giorni <= 10:
                st.markdown(f'<div class="avviso-scadenza">⚠️ ATTENZIONE: Mancano {giorni} giorni al termine della tua Box!</div>', unsafe_allow_html=True)
        except: pass

    # HOME
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        nome_u = st.session_state.user.get('nome genitore', 'Mamma')
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
            <div>
                <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {nome_u}! 👋</div>
                <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div>
                <div style="margin-top:15px; font-size:11px; color:#475569;">👶 Capi selezionati<br>🔄 Cambi quando cresce<br>💰 Risparmio garantito</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa ora"): vai("PromoDettaglio")

    # PROMO DETTAGLIO
    elif st.session_state.pagina == "PromoDettaglio":
        st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
        with st.form("promo_f"):
            st.write("📦 **Dettagli del pacco:**")
            p = st.text_input("Peso stimato (kg)")
            d = st.text_input("Dimensioni pacco")
            if st.form_submit_button("INVIA RICHIESTA"): st.success("Richiesta inviata! Ti scriveremo.")
        if st.button("Torna in Home"): vai("Home")

    # INFO
    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
        st.markdown(f"""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli:</b> La tua Box preferita.<br>
            <b>2. Ricevi:</b> Nel Locker più vicino.<br>
            <b>3. Controlla:</b> Hai 48 ore per segnalazioni.<br>
            <b>4. Usa:</b> Per un massimo di 3 mesi.<br>
            <b>5. Decidi:</b> Prendi la taglia successiva o rendi.<br><br>
            <b>📍 Il Patto del 10:</b> Rendi 10 capi per riceverne 10.</div>""", unsafe_allow_html=True)

    # BOX
    elif st.session_state.pagina == "Box":
        st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
        tg_u = st.session_state.user.get('taglia', '---')
        st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
        col_q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
        if col_q == "Standard":
            for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
                st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
                if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", 19.90)
        else:
            st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:26px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
            if st.button("Scegli Premium"): aggiungi_al_carrello("Box Premium", 29.90)

    # VETRINA
    elif st.session_state.pagina == "Vetrina":
        st.markdown('<h2 style="text-align:center;">Shop 🛍️</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; font-size:13px; color:#475569;">I capi acquistati in Vetrina rimangono a te <b>per sempre</b>.</p>', unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

    # PROFILO
    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
                <b>👤 Nome:</b> {st.session_state.user.get('nome genitore')}<br>
                <b>👶 Bambino:</b> {st.session_state.user.get('nome bambino')}<br>
                <b>📏 Taglia:</b> {st.session_state.user.get('taglia')}<hr>
                <b>📅 Scadenza:</b> {st.session_state.user.get('scadenza')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
            if st.button("Esci"): st.session_state.user = None; vai("Welcome")
        else:
            with st.form("p"):
                n = st.text_input("Tuo Nome", st.session_state.user.get('nome genitore'))
                nb = st.text_input("Nome Bambino", st.session_state.user.get('nome bambino'))
                tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
                if st.form_submit_button("SALVA SU EXCEL"):
                    aggiorna_utente(st.session_state.user['email'], {"nome genitore": n, "nome bambino": nb, "taglia": tg})
                    st.session_state.user.update({"nome genitore": n, "nome bambino": nb, "taglia": tg})
                    st.session_state.edit_mode = False; st.rerun()

    # CARRELLO
    elif st.session_state.pagina == "Carrello":
        st.markdown('<h2 style="text-align:center;">Carrello 🛒</h2>', unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            tot = sum(i['prezzo'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            st.markdown(f"### Totale: {tot:.2f}€")
            if st.button("PROCEDI AL PAGAMENTO"): st.info("Link Stripe in arrivo...")

    # CHI SIAMO
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori come te.</b></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 20px; font-size:14px; color:#475569; text-align:center;">Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che non basta mai.<br><br>Per questo abbiamo creato LoopBaby: per semplificarti la vita e ridurre gli sprechi.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE FISSA (7 COLONNE)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
