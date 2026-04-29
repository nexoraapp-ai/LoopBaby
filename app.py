import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (IL TUO NUOVO LINK) ---
API_URL = "https://sheetdb.io/api/v1/v102s6nrioq0q"

def carica_db():
    try:
        timestamp = datetime.now().timestamp()
        res = requests.get(f"{API_URL}?t={timestamp}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                # Pulizia automatica: toglie spazi e uniforma i nomi delle colonne
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome genitore', 'nome bambino', 'taglia', 'data inizio', 'scadenza'])
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    headers = {"Content-Type": "application/json"}
    res = requests.post(API_URL, json={"data": [nuovo]}, headers=headers, timeout=15)
    return res.status_code

def aggiorna_utente(email, dati):
    headers = {"Content-Type": "application/json"}
    # Cerchiamo la colonna 'email' per aggiornare il rigo giusto
    res = requests.patch(f"{API_URL}/email/{email}", json={"data": dati}, headers=headers)
    return res.status_code

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
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important;
        box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; text-align: center; margin: 15px; font-size: 13px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db()

# --- LOGIN E REGISTRAZIONE ---
if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l_f"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty and 'email' in df_globale.columns:
                        match = df_globale[(df_globale['email'].str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
                    else: st.error("Database in aggiornamento, riprova.")
        with t2:
            with st.form("r_f"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if not df_globale.empty and er.lower() in df_globale['email'].str.lower().values:
                        st.error("Esiste già!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er, "password": str(pr), "nome genitore": "Mamma", "nome bambino": "---", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                        if aggiungi_utente(nuovo) == 201:
                            st.success("Creato! Ora fai l'accesso.")
                        else: st.error("Errore Excel. Controlla le impostazioni su SheetDB.")

# --- APP DOPO LOGIN ---
else:
    # AVVISO SCADENZA (Sempre in alto)
    scad_v = str(st.session_state.user.get('scadenza', ''))
    if scad_v != 'nan' and scad_v != '':
        try:
            gg = (datetime.strptime(scad_v, "%Y-%m-%d") - datetime.now()).days
            if 0 <= gg <= 10:
                st.markdown(f'<div class="avviso-scadenza">⚠️ ATTENZIONE: Mancano {gg} giorni al termine della Box! Prepariamo la nuova taglia?</div>', unsafe_allow_html=True)
        except: pass

    # --- HOME ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_u = st.session_state.user.get('nome genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {nome_u}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa"): vai("Info")

    # --- INFO ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida al Servizio 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Riceverai la tua Box entro 3-5 giorni lavorativi direttamente nel Locker scelto.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Quando i vestiti stringono, ordina la nuova taglia. Scambiamo il vecchio col nuovo insieme.</div>
        <div class="info-box"><span class="accent">📦 RESO FACILE</span><br>Prenota il ritiro dall'area profilo. Se passi alla taglia successiva, il reso è GRATIS.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Ogni capo viene sanificato professionalmente ad ogni rientro.</div>
        """, unsafe_allow_html=True)

    # --- CHI SIAMO ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    '<b>Basta sacchi di vestiti ammassati in soffitta.</b><br><br>'
                    'Siamo genitori stanchi di comprare vestiti che i nostri figli useranno solo per poche settimane. '
                    'Abbiamo creato LoopBaby per far viaggiare i vestiti di famiglia in famiglia, '
                    'seguendo la crescita dei piccoli senza sprechi di soldi e spazio.<br><br>'
                    '<i>Insieme rendiamo la crescita più leggera e sostenibile.</i> 🌿</div>', unsafe_allow_html=True)

    # --- BOX ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", p)

    # --- PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.user.get('nome bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SU EXCEL"):
                aggiorna_utente(st.session_state.user['email'], {"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.session_state.user.update({"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.success("Sincronizzato!")
        if st.button("Logout"): 
            st.session_state.user = None; vai("Welcome")

    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
