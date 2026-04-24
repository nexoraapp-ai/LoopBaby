import streamlit as st
import os
import base64
from datetime import date

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")

if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 2. CSS "SCHELETRO" + FIX DEFINITIVO LINK IN LINEA ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    
    .stApp {
        background-color: #FDFBF7 !important; 
        max-width: 450px !important; 
        margin: 0 auto !important;
    }
    
    .main .block-container {padding: 0 !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-h { font-size: 30px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .heart { color: #f43f5e; font-size: 34px; }
    .slogan { font-size: 13px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home */
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 25px; object-fit: cover; }

    /* CARD BIANCHE */
    .card { 
        border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; 
        text-align: center; background-color: #FFFFFF !important;
    }
    
    .box-luna { background-color: #f1f5f9 !important; } 
    .box-sole { background-color: #fffbeb !important; } 
    .box-nuvola { background-color: #e0f2fe !important; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%) !important; color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

    /* FIX DEFINITIVO: IL BOTTONE DIVENTA TESTO IN LINEA */
    /* Rimuove ogni stile dal bottone specifico */
    div.stButton > button[key*="inline"] {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        color: #475569 !important;
        text-decoration: underline !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        display: inline !important;
        margin: 0 !important;
        vertical-align: baseline !important;
        width: auto !important;
        height: auto !important;
    }

    /* Pulsante Rosa Standard per le altre pagine */
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 18px !important; width: 85% !important; height: 55px !important;
        font-size: 17px !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important;
    }

    /* Barra Navigazione */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: #FDFBF7 !important; border-top: 1px solid #EAE2D6 !important; z-index: 99999; padding: 8px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 9px !important; font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><div class="logo-h"><span class="heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    st.markdown(f"""
        <div class="home-grid">
            <div>
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
                <div style="margin-top:15px;">
                    <div class="item">👶 Capi di qualità selezionati</div>
                    <div class="item">🔄 Cambi quando cresce</div>
                    <div class="item">💰 Risparmi più di 1000€ l’anno</div>
                    <div class="item">🏠 Scegli il locker più vicino a te</div>
                    <div class="item">🧘 Zero stress per te</div>
                </div>
            </div>
            <div>{img_html}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Scegli la tua Box", key="btn_home"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center; color:#1e293b;">Come funziona</div>', unsafe_allow_html=True)
    
    # Punto 1 e 2
    st.markdown("""
        <div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box <b>Standard</b> (capi usati ancora in ottimo stato), Box <b>Premium</b> (nuovi o seminuovi). Nella sezione <b>Vetrina</b>, ciò che acquisti rimane a te per sempre.<br><br>
            <b>2. Scegli e ricevi:</b> Seleziona lo stile e ricevi la Box nel locker più vicino a te.
        </div>
    """, unsafe_allow_html=True)
    
    # PUNTO 3 CON BOTTONE "INCASTRELLO"
    col_testo, col_link = st.columns([0.83, 0.17])
    with col_testo:
        st.markdown('<div style="padding-left: 20px; font-size: 13px; color: #475569;"><b>3. Controllo 48h:</b> Controlla i capi entro 48h dalla ricezione, per qualsiasi problema</div>', unsafe_allow_html=True)
    with col_link:
        # Usiamo una chiave speciale per applicare il CSS che lo rende testo
        if st.button("contattaci", key="inline_contattaci"):
            vai("Contatti")

    # Punto 4
    st.markdown("""
        <div style="padding: 0 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <br><b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia: riceverai da noi un promemoria 10 giorni prima.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center; color:#1e293b;">Regole importanti</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">
            La Box LoopBaby ha un costo di 19,90€ (Standard) o 29,90€ (Premium). Se decidi di rinnovare il servizio prendendo una nuova Box, il ritiro della precedente e la consegna della nuova sono GRATUITI. Se invece desideri restituire la Box senza effettuare un nuovo ordine, il ritiro tramite Locker ha un costo di 7,90€.<br><br>
            <b>📍 La Regola del 10:</b> Per far continuare il ciclo, ti chiediamo di rendere lo stesso numero di capi ricevuti (10). Se un capo viene smarrito o si rovina irreparabilmente, vale lo scambio <b>'Jeans x Jeans'</b> (restituisci un capo simile di tua proprietà) oppure verrà applicata una penale di 5 euro a capo mancante.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Contatti":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center; color:#1e293b;">Contatti & Assistenza 💬</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF5F5 !important; border-color: #FECDD3;">
            <b style="color:#f43f5e; font-size:18px;">Siamo qui per te!</b><br><br>
            💬 <b>WhatsApp:</b> 333 1234567<br>
            📧 <b>Email:</b> hello@loopbaby.it<br><br>
            🕒 <b>Orari:</b> Lun - Ven 9:00 - 18:00</div>""", unsafe_allow_html=True)
    if st.button("Torna alle Info", key="btn_back"): vai("Info")

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 22px; text-align:center;">Le nostre Box</div>', unsafe_allow_html=True)
    # Card Box qui...

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    # Prodotti Shop qui...

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    # Form Profilo qui...

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:center; font-size:14px; color:#475569; line-height:1.6;">Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino. Per questo abbiamo creato LoopBaby: per semplificarti la vita e ridurre gli sprechi.</div>', unsafe_allow_html=True)

# --- 4. BARRA NAVIGAZIONE FISSA ---
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
    if st.button("👋\nContatti"): vai("Contatti")
