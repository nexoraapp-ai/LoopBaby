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

# Gestione navigazione da link HTML
if "nav" in st.query_params:
    st.session_state.pagina = st.query_params["nav"]
    st.query_params.clear()
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px;
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 18px !important;
        width: 100% !important;
        font-weight: 800 !important;
        margin: 10px auto !important;
        display: block !important;
        white-space: nowrap !important;
        border: none !important;
    }}

    .home-grid {{ display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; align-items: start; padding: 0 20px; }}
    .ciao {{ font-size: 28px; font-weight: 800; color: #1e293b; }}
    .headline {{ font-size: 14px; font-weight: 600; color: #334155; line-height: 1.3; }}
    .item {{ display: flex; align-items: center; gap: 10px; font-size: 11px; color: #475569; margin-bottom: 8px; font-weight: 500; }}
    .baby-photo {{ width: 100%; border-radius: 25px; object-fit: cover; }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-luna {{ background-color: #f1f5f9 !important; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}

    /* STILE PER IL LINK "CONTATTACI" IN LINEA */
    .link-inline {{
        color: #475569 !important;
        font-weight: 800 !important;
        text-decoration: underline !important;
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 4. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    u_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {u_nome}!" if u_nome else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div><div style="margin-top:15px;"><div class="item">🔥 Capi di qualità selezionati</div><div class="item">🔄 Cambi quando cresce</div><div class="item">💰 Risparmi più di 1000€ l’anno</div><div class="item">🏠 Scegli il locker più vicino a te</div><div class="item">🧘 Zero stress per te</div></div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio"); st.rerun()

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:14px;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua prima Box!</div>', unsafe_allow_html=True)
    with st.form("promo_f"):
        st.write("📦 **Dettagli del pacco:**")
        p = st.text_input("Peso stimato (kg)")
        d = st.text_input("Dimensioni pacco (es. 30x30x40)")
        st.write("📍 **Punto di ritiro:**")
        l_def = st.session_state.dati['locker'] if st.session_state.dati['locker'] else "Seleziona..."
        l_scelto = st.selectbox("Dove porterai il pacco?", [l_def, "Locker Esselunga", "InPost Point", "Poste Italiane"])
        if st.form_submit_button("INVIA E RICHIEDI ETICHETTA"): 
            st.success(f"Richiesta inviata! Ti invieremo l'etichetta per il {l_scelto} via email.")
    if st.button("Torna in Home"): vai("Home"); st.rerun()

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona</h2>', unsafe_allow_html=True)
    # MODIFICA: Il link "contattaci" è ora in linea, grassetto e sottolineato
    st.markdown(f"""
        <div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            1. <b>Le nostre opzioni:</b> Box Standard o Premium. In <b>Vetrina</b>, ciò che acquisti rimane a te.<br><br>
            2. <b>Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            3. <b>Controllo 48h:</b> Controlla i capi, per problemi <a href="/?nav=Contatti" target="_self" class="link-inline"><b>contattaci</b></a>.<br><br>
            4. <b>Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align:center;">Regole importanti</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">La Box ha un costo di 19,90€ o 29,90€. Il ritiro è GRATUITO se rinnovi l'ordine. <br><br><b>📍 La Regola del 10:</b> Rendi 10 capi per riceverne 10. Se un capo manca, vale lo scambio <b>'Jeans x Jeans'</b> o penale di 5€.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.success(f"{s} aggiunta!")
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Box Premium"): st.success("Premium aggiunta!")

elif st.session_state.pagina == "Vetrina":
    st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; padding:0 20px; font-size:13px;">I capi acquistati in Vetrina rimarranno a te <b>per sempre</b>.<br>Spedizione GRATUITA sopra i 50€ o con Box.</p>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<hr>
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
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            if st.form_submit_button("🔍 Trova Locker vicini"): st.session_state.locker_lista = ["Locker Esselunga - Calolziocorte", "Locker InPost - Lecco FS"]
            lock = st.selectbox("Scegli Locker:", [st.session_state.dati['locker']] + st.session_state.locker_lista)
            if st.form_submit_button("SALVA E BLOCCA DATI"):
                st.session_state.dati = {"nome_genitore": n, "email": m, "telefono": t, "nome_bambino": nb, "nascita": nas, "taglia": tg, "locker": lock}
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="text-align:center;">Chi siamo? ❤️</h2>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding:0 20px; font-size:14px; line-height:1.6;"><b>Siamo genitori, come te.</b><br><br>Abbiamo vissuto quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che manca.<br><br>Per questo è nata LoopBaby: per semplificarti la vita.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="background-color: #FFF1F2;"><b style="color:#f43f5e;">Il nostro obiettivo?</b><br>Offrirti qualità, farti risparmiare più di 1000€ l’anno e lasciare un mondo migliore ai nostri figli.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Contatti":
    st.markdown('<h2 style="text-align:center;">Contatti 💬</h2>', unsafe_allow_html=True)
    st.markdown(f"""<div class="card" style="background:#FFF5F5; border-color:#FECDD3; text-align:left;">
        <b>💬 WhatsApp:</b> <a href="https://wa.me" style="color:#f43f5e; text-decoration:none;">333 1234567</a><br><br>
        <b>📧 Email:</b> <a href="mailto:hello@loopbaby.it" style="color:#f43f5e; text-decoration:none;">hello@loopbaby.it</a>
    </div>""", unsafe_allow_html=True)
    if st.button("Torna in Home"): vai("Home"); st.rerun()

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c = st.columns(6)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c[i]:
        if st.button(icon, key=f"nav_{pag}"): vai(pag); st.rerun()
