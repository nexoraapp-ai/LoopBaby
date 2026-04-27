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

# Gestione navigazione link "contattaci"
if "nav" in st.query_params:
    st.session_state.pagina = st.query_params["nav"]
    st.query_params.clear()

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.jpg") # SFONDO PER L'HEADER

# --- 3. CSS TOTALE (BEIGE + HEADER PANORAMICO + LOOK APP) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* HEADER PANORAMICO CON LOGO SFONDO */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url("data:image/jpeg;base64,{logo_bg}");
        background-size: cover;
        background-position: center;
        height: 130px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    .header-text {{
        color: white;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: 3px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }}

    /* Layout Home */
    .home-grid {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; }}
    .ciao {{ font-size: 28px; font-weight: 800; color: #1e293b; }}
    .headline {{ font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }}
    .item {{ display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }}
    .baby-photo {{ width: 100%; border-radius: 25px; object-fit: cover; }}

    /* Card e Colori Box */
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

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
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div><div style="margin-top:15px;"><div class="item">👶 Capi di qualità selezionati</div><div class="item">🔄 Cambi quando cresce</div><div class="item">💰 Risparmi più di 1000€ l’anno</div><div class="item">🏠 Scegli il locker più vicino a te</div><div class="item">🧘 Zero stress per te</div></div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi in buono stato e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

# -- DETTAGLIO PROMO --
elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:24px; text-align:center;">Diventa Fondatrice 🌸</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:14px; line-height:1.6;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua <b>prima Box</b> da usare entro 3 mesi!</div>""", unsafe_allow_html=True)
    with st.form("promo_form"):
        p = st.text_input("Peso stimato (kg)")
        d = st.text_input("Dimensioni (es. 30x30x40 cm)")
        if st.form_submit_button("INVIA E RICHIEDI ETICHETTA"): st.success("Richiesta inviata! Ti contatteremo su WhatsApp.")
    if st.button("Torna in Home"): vai("Home")

# -- INFO --
elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box <b>Standard</b> (usato ottimo stato), Box <b>Premium</b> (nuovi o seminuovi). Nella sezione <b>Vetrina</b>, ciò che acquisti rimane a te per sempre.<br><br>
            <b>2. Scegli e ricevi:</b> Seleziona lo stile e ricevi la Box nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi entro 48h dalla ricezione, per qualsiasi problema <a href="/?nav=Contatti" target="_self" class="link-inline"><b>contattaci</b></a>.<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia: riceverai da noi un promemoria 10 giorni prima.
        </div>""", unsafe_allow_html=True)
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Regole importanti</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">La Box ha un costo di 19,90€ o 29,90€. Il ritiro è GRATUITO se rinnovi l'ordine. <br><br><b>📍 La Regola del 10:</b> Rendi 10 capi per riceverne 10. Se un capo manca, vale lo scambio <b>'Jeans x Jeans'</b> o penale di 5€.</div>""", unsafe_allow_html=True)

# -- BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.success(f"{s} scelta!")
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Box Premium"): st.success("Premium aggiunta!")

# -- VETRINA --
elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding: 0 20px; color:#475569; font-size:14px; margin-bottom:20px;">I capi acquistati in Vetrina rimarranno nell'armadio del tuo bimbo <b>per sempre</b>.<br>Spedizione GRATUITA sopra i 50€ o con Box.</div>""", unsafe_allow_html=True)
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
            nb = st.text_input("Bambino", st.session_state.dati['nome_bambino'])
            nas = st.date_input("Nascita", st.session_state.dati['nascita'])
            if st.form_submit_button("🔍 Trova Locker vicini"): st.session_state.locker_lista = ["Locker Esselunga - Calolziocorte", "Locker InPost - Lecco FS"]
            lock = st.selectbox("Scegli Locker:", [st.session_state.dati['locker']] + st.session_state.locker_lista)
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "nascita": nas, "locker": lock})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

# -- CONTATTI --
elif st.session_state.pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background:#FFF5F5;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it<br>🕒 Lun-Ven 9:00 - 18:00</div>""", unsafe_allow_html=True)
    if st.button("Indietro"): vai("Home")

# -- CHI SIAMO --
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino. Per questo abbiamo creato LoopBaby.</div><div class="obiettivo-pink"><b style="color:#f43f5e;">Il nostro obiettivo?</b><br>Risparmio, qualità e meno sprechi per il futuro dei nostri figli.</div>""", unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("🏠\nHome"): vai("Home")
with c2:
    if st.button("📖\nInfo"): vai("Info")
with c3:
    if st.button("📦\nBox"): vai("Box")
with c4:
    if st.button("🛍️\nVetrina"): vai("Vetrina")
with c5:
    if st.button("👤\nProfilo"): vai("Profilo")
with c6:
    if st.button("👋\nChi Siamo"): vai("ChiSiamo")
