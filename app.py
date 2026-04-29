import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
from datetime import date, datetime, timedelta

# --- 1. MOTORE DATABASE & SICUREZZA ---
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
        return pd.DataFrame(columns=['email','password','nome','bimbo','taglia','inizio','scadenza','locker'])
    except:
        return pd.DataFrame()

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

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

# --- 3. IMMAGINI E STILE CSS (IL DESIGN DI IERI) ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 100px !important; }}
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
        box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); height: 45px;
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>L'armadio infinito 🔄</h2>", unsafe_allow_html=True)
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
                        m = df_db[(df_db['email'].str.lower() == e) & (df_db['password'] == hp)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
                rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
                if st.form_submit_button("CREA ACCOUNT"):
                    nuovo = {"email": re, "password": hash_password(rp), "nome": rn, "bimbo": rb, "taglia": rt, "inizio": str(date.today()), "scadenza": "", "locker": rl}
                    registra_user(nuovo)
                    st.success("Registrato! Ora fai l'Accedi.")
                    st.balloons()

# --- 5. APP DOPO LOGIN ---
else:
    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    st.markdown('<div style="margin-top:-20px;"></div>', unsafe_allow_html=True)
    c_nav = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    
    st.divider()

    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        n = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div>
                <div style="font-size:28px; font-weight:800;">Ciao {n}! 👋</div>
                <div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa"): vai("Info")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida LoopBaby 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Riceverai la Box entro 3-5 giorni nel Locker InPost scelto.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Ordina la taglia nuova, ti spediamo la nuova e rendi la vecchia insieme.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Capi sanificati ad alte temperature per ogni bambino.</div>
        """, unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", p)

    elif st.session_state.pagina == "Vetrina":
        st.markdown("<h2 style='text-align:center;'>Shop 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio Loop</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Profilo 👤</h2>", unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome:</b> {u.get('nome')}<br>
            <b>👶 Bambino:</b> {u.get('bimbo')}<br>
            <b>📏 Taglia:</b> {u.get('taglia')}<br>
            <b>📍 Locker:</b> {u.get('locker')}
        </div>""", unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Carrello 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            tot = sum(i['prezzo'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            st.markdown(f"### Totale: {tot:.2f}€")
            if st.button("PAGA ORA"): st.success("Link Stripe in arrivo!")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    'Siamo genitori che hanno deciso di dire basta allo spreco. '
                    'Abbiamo creato <b>LoopBaby</b> per far viaggiare la qualità di famiglia in famiglia, '
                    'seguendo la crescita dei piccoli senza sprechi di soldi e spazio.🌿</div>', unsafe_allow_html=True)
