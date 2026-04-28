import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA LOCALE (DATABASE JSON) ---
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
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (Design Originale) ---
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

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- 4. PAGINE ---

# --- HOME ---
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
        <div>
            <div style="font-size:28px; font-weight:800;">Ciao {u_nome}! 👋</div>
            <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div>
            <div style="margin-top:15px; font-size:11px;">🔥 Qualità garantita<br>🔄 Cambi infiniti<br>💰 Risparmio assicurato<br>🏠 Locker vicino a te</div>
        </div>
        <div>{img_html}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona 10 capi e ricevi una <b>BOX OMAGGIO</b>!</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa ora"): vai("PromoDettaglio"); st.rerun()

# --- PROMO ---
elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
    with st.form("promo_f"):
        p = st.text_input("Peso stimato (kg)")
        d = st.text_input("Dimensioni pacco")
        if st.form_submit_button("RICHIEDI ETICHETTA"): st.success("Richiesta inviata!")
    if st.button("Torna in Home"): vai("Home"); st.rerun()

# --- INFO ---
elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona</h2>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            1. <b>Le opzioni:</b> Box Standard o Premium.<br><br>
            2. <b>Scegli e ricevi:</b> Nel locker più vicino a te.<br><br>
            3. <b>Controllo 48h:</b> Per problemi <b>contattaci</b>.<br><br>
            4. <b>Dopo 3 mesi:</b> Rendi o ricevi la nuova taglia.
        </div>""", unsafe_allow_html=True)

# --- BOX ---
elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    tg_u = st.session_state.dati['taglia']
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700; color:#00796b;">📍 TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s in [("LUNA 🌙"), ("SOLE ☀️")]:
            st.markdown(f'<div class="card"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): 
                st.session_state.carrello.append(f"Box {s}")
                st.toast("Aggiunta!")

# --- SHOP/VETRINA ---
elif st.session_state.pagina == "Vetrina":
    st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    if st.button("Aggiungi 🎁"): 
        st.session_state.carrello.append("Body Bio")
        st.toast("Aggiunto!")

# --- PROFILO ---
elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<hr>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br>
            <b>📍 Locker:</b> {st.session_state.dati['locker']}
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit"):
            n = st.text_input("Tuo Nome", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            lock = st.selectbox("Locker", ["Locker Esselunga", "InPost Point"])
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "taglia": tg, "locker": lock})
                salva_dati_su_file(st.session_state.dati)
                st.session_state.edit_mode = False; st.rerun()

# --- CHI SIAMO ---
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="text-align:center;">Chi siamo? ❤️</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:14px; line-height:1.6;">'
                'Siamo genitori come te. Abbiamo vissuto la fatica di vedere vestiti bellissimi durare poche settimane.<br><br>'
                'LoopBaby nasce per eliminare lo spreco e lo stress: ti offriamo un armadio circolare, di qualità, che cresce con il tuo bambino.'
                '</div>', unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c = st.columns(6)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c[i]:
        if st.button(icon, key=f"n_{pag}"): vai(pag); st.rerun()
