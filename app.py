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
# Sidebar inizialmente chiusa, ma pulsante visibile
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "pagina_attiva" not in st.session_state:
    st.session_state.pagina_attiva = "Home"

# --- 3. NAVIGAZIONE SIDEBAR (LE 3 LINETTE) ---
st.sidebar.markdown("## 🍼 Menu LoopBaby")
# Sincronizziamo la sidebar con lo stato della pagina
lista_pagine = ["Home", "Info", "Mamme Fondatrici", "Scegli la Box", "Shop Vetrina", "Il tuo Profilo", "Chi Siamo", "Contatti"]
scelta_sidebar = st.sidebar.radio("Vai a:", lista_pagine, index=lista_pagine.index(st.session_state.pagina_attiva))

# Aggiorna la pagina se l'utente usa la sidebar
if scelta_sidebar != st.session_state.pagina_attiva:
    st.session_state.pagina_attiva = scelta_sidebar
    st.rerun()

def vai(nome_pag): 
    st.session_state.pagina_attiva = nome_pag
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 4. CSS TOTALE (RIPRISTINO 3 LINETTE + BEIGE) ---
st.markdown(f"""
    <style>
    /* Nasconde la barra Streamlit ma NON il pulsante menu (3 linette) */
    [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    header {{background-color: transparent !important;}}
    
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* Pulsante 3 linette (Hamburger) ben visibile */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 50% !important;
        padding: 5px !important;
        left: 15px !important;
        top: 15px !important;
    }}

    /* HEADER PANORAMICO */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; border-radius: 0 0 30px 30px;
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 5. LOGICA PAGINE ---

if st.session_state.pagina_attiva == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px; padding: 0 20px;">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f'<div style="padding: 0 20px;"><div style="font-size: 28px; font-weight: 800;">{saluto} 👋</div><div style="font-size: 15px; margin-bottom: 10px;">L\'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div></div>', unsafe_allow_html=True)
    st.markdown(f"{img_html}", unsafe_allow_html=True)
    
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>!</p></div>""", unsafe_allow_html=True)
    # TASTO CHE PORTA ALL'ISCRIZIONE PROMO
    if st.button("Partecipa e richiedi etichetta"):
        vai("Mamme Fondatrici")

elif st.session_state.pagina_attiva == "Mamme Fondatrici":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:24px; text-align:center;">Diventa Fondatrice 🌸</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:14px; line-height:1.6;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua <b>prima Box</b> da usare entro 3 mesi!</div>""", unsafe_allow_html=True)
    with st.form("promo_f"):
        st.text_input("Peso stimato (kg)")
        st.text_input("Dimensioni pacco (es. 30x30x40)")
        if st.form_submit_button("INVIA E RICHIEDI ETICHETTA"):
            st.success("Richiesta ricevuta! Ti contatteremo su WhatsApp.")
    if st.button("Torna in Home"): vai("Home")

elif st.session_state.pagina_attiva == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size: 13px; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box Standard o Premium. <br><br>
            <b>2. Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi, per problemi contattaci nel menu.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:13px;"><b>📍 Regola del 10:</b> Rendi 10 capi per riceverne 10.</div>', unsafe_allow_html=True)

elif st.session_state.pagina_attiva == "Scegli la Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s in ["LUNA 🌙", "SOLE ☀️", "NUVOLA ☁️"]:
            st.markdown(f'<div class="card"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

elif st.session_state.pagina_attiva == "Shop Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding:0 20px; font-size:14px;">I capi acquistati in Vetrina rimarranno a te <b>per sempre</b>.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif st.session_state.pagina_attiva == "Il tuo Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br>
            <b>📍 Locker:</b> {st.session_state.dati['locker']}
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit"):
            n = st.text_input("Nome", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Bambino", st.session_state.dati['nome_bambino'])
            lock = st.text_input("Locker", st.session_state.dati['locker'])
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "locker": lock})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif st.session_state.pagina_attiva == "Chi Siamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori che credono nel futuro.</b></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; line-height:1.7; text-align:center;">
            Sappiamo che ogni bambino è un miracolo e che vederlo crescere è l'emozione più bella del mondo.<br><br>
            Proprio perché i nostri piccoli crescono così in fretta, abbiamo creato <b>LoopBaby</b>: un modo per accompagnare i loro primi passi con capi di altissima qualità, riducendo gli sprechi e rispettando il pianeta.<br><br>
            Siamo una comunità di famiglie che sceglie la condivisione per offrire il meglio ai propri figli, con intelligenza e amore.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Garantire il meglio al tuo bebè e lasciare un mondo migliore ai nostri figli.</div>', unsafe_allow_html=True)

elif st.session_state.pagina_attiva == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="background:#FFF5F5;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it</div>', unsafe_allow_html=True)
