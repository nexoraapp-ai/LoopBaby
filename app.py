import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (SHEETDB) ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        res = requests.get(f"{API_URL}?t={datetime.now().timestamp()}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome genitore', 'nome bambino', 'taglia', 'data inizio', 'scadenza', 'locker'])
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    return requests.post(API_URL, json={"data": [nuovo]}, timeout=15).status_code

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
                    if not df_globale.empty:
                        m = df_globale[(df_globale['email'].str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
        with t2:
            with st.form("r_f"):
                er = st.text_input("La tua migliore Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if not df_globale.empty and er.lower() in df_globale['email'].str.lower().values:
                        st.error("Esiste già!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er, "password": str(pr), "nome genitore": "Mamma", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Non impostato"}
                        if aggiungi_utente(nuovo) == 201:
                            st.success("Creato! Ora fai l'accesso.")

# --- APP DOPO LOGIN ---
else:
    # --- HOME ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Scopri di più"): vai("Info")

    # --- INFO LOGISTICA ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida al Servizio 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
            <span class="accent">🚚 Consegna Locker InPost</span><br>
            Riceverai la tua Box entro <b>3-5 giorni lavorativi</b>. Utilizziamo i Locker InPost per darti massima libertà: ritira il pacco quando vuoi, 24/7, senza dover aspettare il corriere a casa.
        </div>
        <div class="info-box">
            <span class="accent">🔄 Il Cambio Taglia</span><br>
            Quando i vestiti iniziano a stare stretti, ordina la taglia successiva dall'app. Ti spediremo la nuova Box e potrai consegnare quella vecchia nello stesso momento. <b>Circolarità pura.</b>
        </div>
        <div class="info-box">
            <span class="accent">📦 Reso e Lavaggio</span><br>
            Il reso è sempre <b>GRATIS</b> se passi alla taglia successiva. Ogni capo che rientra viene sanificato professionalmente ad alte temperature per garantire igiene totale al prossimo bambino.
        </div>
        """, unsafe_allow_html=True)

    # --- CHI SIAMO EMOZIONALE ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="text-align:left; line-height:1.6; font-size:15px;">
            <b>Basta sacchi di vestiti ammassati in soffitta o soldi sprecati per tutine messe due volte.</b><br><br>
            Siamo un team di genitori che ha deciso di rivoluzionare l'armadio dei più piccoli. Abbiamo vissuto la frustrazione di dover ricomprare tutto ogni tre mesi e lo stress di non sapere dove stipare i vestiti diventati piccoli.<br><br>
            <b>LoopBaby</b> nasce per questo: creare un "giro infinito" di abbigliamento di alta qualità. I capi viaggiano di famiglia in famiglia, seguendo la crescita dei bimbi senza pesare sul portafoglio dei genitori e sull'ambiente.<br><br>
            <i>Insieme, rendiamo la crescita dei nostri figli più leggera e sostenibile.</i> 🌿
        </div>
        """, unsafe_allow_html=True)

    # --- PROFILO (FIX TASTO SALVA E LOCKER) ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.user.get('nome bambino', ''))
            tg = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm"])
            loc = st.text_input("Locker InPost di riferimento (Città/Indirizzo)", st.session_state.user.get('locker', ''))
            if st.form_submit_button("SALVA"):
                aggiorna_utente(st.session_state.user['email'], {"nome genitore": n, "nome bambino": nb, "taglia": tg, "locker": loc})
                st.session_state.user.update({"nome genitore": n, "nome bambino": nb, "taglia": tg, "locker": loc})
                st.success("Profilo aggiornato!")
        if st.button("Logout"): 
            st.session_state.user = None; vai("Welcome")

    # --- BOX ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", p)

    # BARRA NAVIGAZIONE FISSA (7 ICONE)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
