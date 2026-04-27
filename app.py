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
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# CARICAMENTO IMMAGINI (Come da Foto 4)
img_data = get_base64("bimbo.jpg")
logo_data = get_base64("logo.png") 

# --- 3. CSS TOTALE (Inclusa Foto 1 e Foto 2) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    /* CSS RICHIESTO DA FOTO 1: Logo Header */
    .header-box {{ padding: 20px; text-align: center; }}
    .header-box img {{ 
        max-width: 220px; 
        height: auto;
    }}
    .slogan {{ 
        font-size: 13px; 
        color: #64748b; 
        margin-top: 10px; 
        font-weight: 500;
    }}

    /* Stili Blindati */
    .home-grid {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }}
    .ciao {{ font-size: 28px; font-weight: 800; color: #1e293b; }}
    .headline {{ font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }}
    .item {{ display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; }}
    .baby-photo {{ width: 100%; border-radius: 25px; object-fit: cover; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; }}
    .box-luna {{ background-color: #f1f5f9 !important; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }}
    .promo-box {{ background-color: #FFF1F2 !important; border: 2px dashed #F43F5E !important; border-radius: 20px; padding: 15px; margin: 15px 20px; text-align: center; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}

    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 85% !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important; }}
    [data-testid="stHorizontalBlock"] {{ position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important; }}
    [data-testid="stHorizontalBlock"] button {{ background: transparent !important; color: #1e293b !important; border: none !important; font-size: 20px !important; font-weight: 700 !important; width: auto !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SOSTITUZIONE HEADER (Come da Foto 2 e 3) ---
st.markdown(f"""
    <div class="header-box">
        <img src="data:image/png;base64,{logo_data}">
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
""", unsafe_allow_html=True)

# --- 5. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    user_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else ""
    saluto = f"Ciao {user_nome}!" if user_nome else "Ciao!"
    st.markdown(f"""<div class="home-grid"><div><div class="ciao">{saluto} 👋</div><div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div><div style="margin-top:15px;"><div class="item">👶 Capi di qualità selezionati</div><div class="item">🔄 Cambi quando cresce</div><div class="item">💰 Risparmi più di 1000€ l’anno</div></div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="promo-box"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto ed etichetta a carico nostro.</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa e ricevi l'etichetta"): vai("PromoDettaglio")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:24px; text-align:center;">Diventa Fondatrice 🌸</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:14px; line-height:1.6;"><b>Preparare il pacco è semplicissimo:</b> mandaci almeno <b>10 capi</b> in buono stato, noi paghiamo il trasporto e ti regaliamo la tua <b>prima Box</b> da usare entro 3 mesi!</div>""", unsafe_allow_html=True)
    with st.form("promo_f"):
        st.text_input("Peso stimato (kg)")
        st.text_input("Dimensioni")
        if st.form_submit_button("RICHIEDI ETICHETTA"): st.success("Richiesta inviata!")
    if st.button("Torna in Home"): vai("Home")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown(f"""<div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;"><b>1. Le nostre opzioni:</b> Box <b>Standard</b> o <b>Premium</b>.<br><br><b>2. Scegli e ricevi:</b> Nel locker più vicino a te.<br><br><b>3. Controllo 48h:</b> Per problemi <b>contattaci</b> (nella sezione dedicata).<br><br><b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia.</div>""", unsafe_allow_html=True)
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Regole importanti</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">La Box ha un costo di 19,90€ o 29,90€. Il ritiro è GRATUITO se rinnovi l'ordine. <br><br><b>📍 La Regola del 10:</b> Rendi 10 capi per riceverne 10.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Scegli la tua Box 📦</div>', unsafe_allow_html=True)
    q = st.radio("Seleziona Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Grigio")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi nuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center; padding:0 20px; font-size:14px; color:#475569;">I capi acquistati in Vetrina rimarranno nell'armadio del tuo bimbo <b>per sempre</b>.</div>""", unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Profilo 👤</div>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;"><b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br><b>📧 Email:</b> {st.session_state.dati['email']}<br><b>📍 Locker:</b> {st.session_state.dati['locker']}</div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
    else:
        with st.form("edit"):
            n = st.text_input("Tuo Nome", st.session_state.dati['nome_genitore'])
            m = st.text_input("Email", st.session_state.dati['email'])
            lock = st.text_input("Locker", st.session_state.dati['locker'])
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "email": m, "locker": lock})
                salva_dati_su_file(st.session_state.dati); st.session_state.edit_mode = False; st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino. Per questo abbiamo creato LoopBaby.</div><div class="obiettivo-pink"><b style="color:#f43f5e;">Il nostro obiettivo?</b><br>Offrirti vestiti di qualità, farti risparmiare e lasciare un mondo migliore ai nostri figli.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center;">Contatti 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background:#FFF5F5; border-color:#FECDD3;">💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it</div>""", unsafe_allow_html=True)

# --- 6. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.button("🏠", on_click=vai, args=("Home",))
with c2: st.button("📖", on_click=vai, args=("Info",))
with c3: st.button("📦", on_click=vai, args=("Box",))
with c4: st.button("🛍️", on_click=vai, args=("Vetrina",))
with c5: st.button("👤", on_click=vai, args=("Profilo",))
with c6: st.button("🤝", on_click=vai, args=("ChiSiamo",))
