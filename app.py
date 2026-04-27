import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA (DATABASE JSON) ---
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except: pass
    return {
        "nome_genitore": "", "email": "", "telefono": "",
        "nome_bambino": "", "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm (0-3m)", "locker": ""
    }

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)

# --- 2. CONFIGURAZIONE ---
# Sidebar inizialmente chiusa per mostrare le 3 linette in alto
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

# --- 3. NAVIGAZIONE SIDEBAR (LE 3 LINETTE STILE FACEBOOK) ---
st.sidebar.markdown("## 🍼 LoopBaby Menu")
pagina = st.sidebar.radio("Vai a:", 
    ["Home", "Info", "Scegli la Box", "Shop Vetrina", "Il tuo Profilo", "Chi Siamo", "Contatti"])

def vai(nome_pag): 
    # Funzione per cambiare pagina dai bottoni interni se necessario
    st.session_state.pagina_diretta = nome_pag 

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 4. CSS TOTALE (BEIGE + HEADER PANORAMICO + LOOK BLINDATO) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* Pulsante 3 linette (Hamburger) personalizzato */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 8px !important;
        left: 10px !important;
        top: 10px !important;
    }}

    /* HEADER PANORAMICO */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; }}

    .home-grid {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; }}
    .ciao {{ font-size: 28px; font-weight: 800; color: #1e293b; }}
    .headline {{ font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 5. LOGICA PAGINE ---

if pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi in buono stato e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box <b>Standard</b> (usato ottimo stato), Box <b>Premium</b> (nuovi o seminuovi). Nella sezione <b>Vetrina</b>, ciò che acquisti rimane a te per sempre.<br><br>
            <b>2. Scegli e ricevi:</b> Seleziona lo stile e ricevi la Box nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi entro 48h dalla ricezione, per qualsiasi problema contattaci nel menu dedicato.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia: riceverai da noi un promemoria 10 giorni prima.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Regole importanti</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">La Box ha un costo di 19,90€ o 29,90€. Il ritiro è GRATUITO se rinnovi l'ordine. <br><br><b>📍 La Regola del 10:</b> Rendi 10 capi per riceverne 10. Se un capo manca, vale lo scambio <b>'Jeans x Jeans'</b> o penale di 5€.</div>""", unsafe_allow_html=True)

elif pagina == "Scegli la Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

elif pagina == "Shop Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding:0 20px; font-size:14px; color:#475569; margin-bottom:20px;">I capi acquistati in Vetrina rimarranno nell'armadio del tuo bimbo <b>per sempre</b>.<br>Spedizione GRATUITA sopra i 50€ o con Box.</div>""", unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif pagina == "Il tuo Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<br><hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br><hr>
            <b>📍 Locker scelto:</b><br><span style="color:#0d9488; font-weight:800;">{st.session_state.dati['locker'] if st.session_state.dati['locker'] else 'Da scegliere'}</span>
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit_f"):
            n = st.text_input("Nome e Cognome", st.session_state.dati['nome_genitore'])
            m = st.text_input("Email", st.session_state.dati['email'])
            t = st.text_input("Telefono", st.session_state.dati['telefono'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            nas = st.date_input("Nascita", st.session_state.dati['nascita'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"], index=0)
            if st.form_submit_button("🔍 Trova Locker vicini"): st.session_state.locker_lista = ["Locker Esselunga - Calolziocorte", "Locker InPost - Lecco FS"]
            lock = st.selectbox("Scegli Locker:", [st.session_state.dati['locker']] + st.session_state.locker_lista)
            if st.form_submit_button("SALVA E BLOCCA DATI"):
                st.session_state.dati = {"nome_genitore": n, "email": m, "telefono": t, "nome_bambino": nb, "nascita": nas, "taglia": tg, "locker": lock}
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif pagina == "Chi Siamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori che credono nel futuro.</b></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.7; text-align:center;">
            Sappiamo che ogni bambino è un miracolo e che vederlo crescere è l'emozione più bella del mondo.<br><br>
            Proprio perché i nostri piccoli crescono così in fretta, abbiamo creato <b>LoopBaby</b>: un modo per accompagnare i loro primi passi con capi di altissima qualità, riducendo gli sprechi e rispettando il pianeta che un giorno esploreranno.<br><br>
            Siamo una comunità di famiglie che sceglie la condivisione per offrire il meglio ai propri figli, con intelligenza e amore. Vogliamo che tu possa goderti ogni momento della crescita del tuo bebè, sapendo che al suo armadio e al suo domani ci pensiamo noi.
        </div>
        <div class="obiettivo-pink">
            <b style="color:#f43f5e; font-weight:800;">Il nostro obiettivo?</b><br>
            Offrirti vestiti di qualità, farti risparmiare più di 1000€ l'anno e lasciare un mondo migliore ai nostri figli.
        </div>
    """, unsafe_allow_html=True)

elif pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background:#FFF5F5; border-color:#FECDD3;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it<br>🕒 Lun-Ven 9:00 - 18:00</div>""", unsafe_allow_html=True)
