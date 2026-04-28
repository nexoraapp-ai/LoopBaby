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
        "taglia": "50-56 cm", "locker": ""
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

# --- AGGIUNTA WELCOME LOGIC ---
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Welcome" if not st.session_state.dati["nome_genitore"] else "Home"

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []
if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto al carrello!")

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
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        display: block !important; white-space: nowrap !important; border: none !important;
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-luna {{ background-color: #f1f5f9 !important; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}

    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. PAGINE ---

# AGGIUNTA PAGINA WELCOME
if st.session_state.pagina == "Welcome":
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in LoopBaby! 🌸</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino. Iniziamo subito!</p>", unsafe_allow_html=True)
    with st.form("w_form"):
        nome = st.text_input("Come ti chiami?", placeholder="Inserisci il tuo nome")
        if st.form_submit_button("ENTRA NELL'APP"):
            if nome:
                st.session_state.dati["nome_genitore"] = nome
                salva_dati_su_file(st.session_state.dati)
                vai("Home"); st.rerun()
            else: st.error("Inserisci il tuo nome per continuare")

elif st.session_state.pagina == "Home":
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {u_nome}!" if u_nome else "Ciao!"
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; align-items: start; padding: 0 20px;"><div><div style="font-size:28px; font-weight:800;">{saluto} 👋</div><div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div><div style="margin-top:15px;"><div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">🔥 Capi di qualità selezionati</div><div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">🔄 Cambi quando cresce</div><div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">💰 Risparmi più di 1000€ l’anno</div><div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px; font-weight:500;">🏠 Scegli il locker più vicino a te</div></div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio"); st.rerun()

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:14px;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua prima Box!</div>', unsafe_allow_html=True)
    with st.form("promo_f"):
        st.write("📦 **Dettagli del pacco:**")
        p = st.text_input("Peso stimato (kg)")
        d = st.text_input("Dimensioni pacco (es. 30x30x40)")
        l_def = st.session_state.dati['locker'] if st.session_state.dati['locker'] else "Seleziona..."
        l_scelto = st.selectbox("Dove porterai il pacco?", [l_def, "Locker Esselunga", "InPost Point", "Poste Italiane"])
        if st.form_submit_button("INVIA E RICHIEDI ETICHETTA"): 
            st.success(f"Richiesta inviata! Ti invieremo l'etichetta via email.")
    if st.button("Torna in Home"): vai("Home"); st.rerun()

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona</h2>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            1. <b>Le nostre opzioni:</b> Box Standard o Premium. In <b>Vetrina</b>, ciò che acquisti rimane a te.<br><br>
            2. <b>Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            3. <b>Controllo 48h:</b> Controlla i capi, per problemi <a href="/?nav=Contatti" target="_self" class="link-inline"><b>contattaci</b></a>.<br><br>
            4. <b>Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.
        </div>""", unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">Regole importanti</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">La Box ha un costo di 19,90€ o 29,90€. Il ritiro è GRATUITO se rinnovi l'ordine. <br><br><b>📍 La Regola del 10:</b> Rendi 10 capi per riceverne 10.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    tg_u = st.session_state.dati['taglia']
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 CONFIGURATA PER TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s} ({tg_u})", key=s): aggiungi_al_carrello(f"Box {s} ({tg_u})", 19.90)
    else:
        st.markdown(f'<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli Box Premium ({tg_u})"): aggiungi_al_carrello(f"Box Premium ({tg_u})", 29.90)

elif st.session_state.pagina == "Vetrina":
    st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
    st.selectbox("Filtra per taglia (opzionale):", ["Tutte le taglie", "50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"], index=0)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    if st.button("Aggiungi al carrello 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

# AGGIUNTA PAGINA CARRELLO
elif st.session_state.pagina == "Carrello":
    st.markdown('<h2 style="text-align:center;">Il tuo Carrello 🛒</h2>', unsafe_allow_html=True)
    if not st.session_state.carrello:
        st.write("Il carrello è vuoto.")
    else:
        totale = 0
        for i, item in enumerate(st.session_state.carrello):
            st.markdown(f"<div style='display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #EEE;'><b>{item['nome']}</b> <span>{item['prezzo']:.2f}€</span></div>", unsafe_allow_html=True)
            totale += item['prezzo']
        st.markdown(f"<h3 style='text-align:right; margin-top:20px;'>Totale: {totale:.2f}€</h3>", unsafe_allow_html=True)
        if st.button("PROCEDI AL PAGAMENTO 💳"): st.warning("Reindirizzamento al pagamento sicuro..."); st.success("Pagamento completato!")
        if st.button("SVUOTA CARRELLO"): st.session_state.carrello = []; st.rerun()
    if st.button("Torna alla Home"): vai("Home"); st.rerun()

elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia attuale:</b> {st.session_state.dati['taglia']}<hr>
            <b>📍 Locker:</b> {st.session_state.dati['locker'] if st.session_state.dati['locker'] else 'Da scegliere'}
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
    st.markdown('<div style="text-align:center; padding:0 20px; font-size:14px; line-height:1.6;"><b>Siamo genitori, come te.</b><br><br>Abbiamo vissuto quanto sia impegnativo far crescere un bambino. Per questo è nata LoopBaby: per semplificarti la vita.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="background-color: #FFF1F2;"><b style="color:#f43f5e;">Il nostro obiettivo?</b><br>Offrirti qualità, farti risparmiare più di 1000€ l’anno e lasciare un mondo migliore ai nostri figli.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Contatti":
    st.markdown('<h2 style="text-align:center;">Contatti 💬</h2>', unsafe_allow_html=True)
    st.markdown(f"""<div class="card" style="background:#FFF5F5; border-color:#FECDD3; text-align:left;">
        <b>💬 WhatsApp:</b> <a href="https://wa.me" style="color:#f43f5e; text-decoration:none;">333 1234567</a><br><br>
        <b>📧 Email:</b> <a href="mailto:hello@loopbaby.it" style="color:#f43f5e; text-decoration:none;">hello@loopbaby.it</a>
    </div>""", unsafe_allow_html=True)
    if st.button("Torna in Home"): vai("Home"); st.rerun()

# --- 5. BARRA NAVIGAZIONE FISSA ---
if st.session_state.pagina != "Welcome":
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag); st.rerun()
