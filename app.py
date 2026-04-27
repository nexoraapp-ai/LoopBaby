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

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

# Gestione link "contattaci" nelle Info
if "nav" in st.query_params:
    st.session_state.pagina = "Contatti"
    st.query_params.clear()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (BEIGE + HEADER PANORAMICO + LOOK BLINDATO) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* HEADER PANORAMICO */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px; border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); text-transform: uppercase; }}

    /* Layout Home */
    .home-grid {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; }}
    .ciao {{ font-size: 28px; font-weight: 800; color: #1e293b; }}
    .headline {{ font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }}
    .item {{ display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }}
    .baby-photo {{ width: 100%; border-radius: 25px; object-fit: cover; }}

    /* Card Box e Promo */
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}

    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }}

    [data-testid="stHorizontalBlock"] {{ position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important; }}
    [data-testid="stHorizontalBlock"] button {{ background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important; }}
    </style>
    """, unsafe_allow_html=True)

# HEADER SUPERIORE FISSO
st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 4. PAGINE ---

# -- HOME --
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div><div style="margin-top:15px;"><div class="item">👶 Capi di qualità selezionati</div><div class="item">🔄 Cambi quando cresce</div><div class="item">💰 Risparmi più di 1000€ l’anno</div><div class="item">🏠 Scegli il locker più vicino a te</div></div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio"); st.rerun()

# -- PROMO DETTAGLIO --
elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:24px; text-align:center;">Diventa Fondatrice 🌸</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:14px; line-height:1.6;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua <b>prima Box</b> da usare entro 3 mesi!</div>""", unsafe_allow_html=True)
    with st.form("promo_f"):
        st.text_input("Peso stimato (kg)")
        st.text_input("Dimensioni pacco")
        if st.form_submit_button("RICHIEDI ETICHETTA"): st.success("Richiesta inviata!")
    if st.button("Torna in Home"): vai("Home"); st.rerun()

# -- INFO --
elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box <b>Standard</b> (usato ottimo) o <b>Premium</b> (nuovi). In <b>Vetrina</b>, ciò che acquisti rimane a te.<br><br>
            <b>2. Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi, per problemi <a href="/?nav=Contatti" target="_self" class="link-inline">contattaci</a>.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.
        </div>""", unsafe_allow_html=True)

# -- BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

# -- SHOP VETRINA --
elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding:0 20px; font-size:14px; color:#475569; margin-bottom:20px;">I capi acquistati in Vetrina rimarranno nell'armadio del tuo bimbo <b>per sempre</b>. Spedizione GRATUITA sopra i 50€ o con Box.</div>""", unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

# -- PROFILO --
elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<br><hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br><hr>
            <b>📍 Locker:</b> {st.session_state.dati['locker']}
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit"):
            n = st.text_input("Tuo Nome", st.session_state.dati['nome_genitore'])
            m = st.text_input("Email", st.session_state.dati['email'])
            t = st.text_input("Telefono", st.session_state.dati['telefono'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            nas = st.date_input("Nascita", st.session_state.dati['nascita'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"], index=0)
            if st.form_submit_button("🔍 Trova Locker"): st.session_state.locker_lista = ["Locker Esselunga - Calolziocorte", "Locker InPost - Lecco FS"]
            lock = st.selectbox("Scegli Locker:", [st.session_state.dati['locker']] + st.session_state.locker_lista)
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "email": m, "telefono": t, "nome_bambino": nb, "nascita": nas, "taglia": tg, "locker": lock})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

# -- CHI SIAMO (DA FOTO) --
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori che credono nel futuro.</b></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.7; text-align:center;">
            Sappiamo che ogni bambino è un miracolo e che vederlo crescere è l'emozione più bella del mondo.<br><br>
            Proprio perché i nostri piccoli crescono così in fretta, abbiamo creato <b>LoopBaby</b>: un modo per accompagnare i loro primi passi con capi di altissima qualità, riducendo gli sprechi e rispettando il pianeta che un giorno esploreranno.<br><br>
            Siamo una comunità di famiglie che sceglie la condivisione per offrire il meglio ai propri figli, con intelligenza e amore. Vogliamo che tu possa goderti ogni momento della crescita del tuo bebè, sapendo che al suo armadio e al suo domani ci pensiamo noi.
        </div>
    """, unsafe_allow_html=True)

# -- CONTATTI --
elif st.session_state.pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background:#FFF5F5;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it</div>""", unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.button("🏠\nHome", on_click=vai, args=("Home",))
with c2: st.button("📖\nInfo", on_click=vai, args=("Info",))
with c3: st.button("📦\nBox", on_click=vai, args=("Box",))
with c4: st.button("🛍️\nShop", on_click=vai, args=("Vetrina",))
with c5: st.button("👤\nProfilo", on_click=vai, args=("Profilo",))
with c6: st.button("👋\nChi Siamo", on_click=vai, args=("ChiSiamo",))
