import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS TOTALE (COPIA ESATTA DEL DESIGN) ---
st.markdown("""
    <style>
    /* Nascondi tutto lo sporco di Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo e Slogan */
    .header-box { padding: 10px 20px; text-align: left; }
    .logo-title { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* Titoli */
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin-top: 10px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }

    /* Lista Punti Elenco */
    .list-container { margin-top: 15px; }
    .list-item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #475569; margin-bottom: 10px; font-weight: 500; }

    /* Pulsante Rosa FULL WIDTH */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Footer */
    .footer-note { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 30px; }
    
    /* Arrotondamento Immagine */
    [data-testid="stImage"] img { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("""
    <div class="header-box">
        <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. LAYOUT A DUE COLONNE (TESTO E BIMBO) ---
col_testo, col_bimbo = st.columns([1.5, 1])

with col_testo:
    st.markdown('<div class="ciao">Ciao Mamma! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="list-container">
            <div class="list-item">👕 Capi di qualità selezionati</div>
            <div class="list-item">🔄 Cambi quando cresce</div>
            <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="list-item">📍 Scegli il locker più vicino</div>
            <div class="list-item">✨ Zero stress per te</div>
        </div>
    """, unsafe_allow_html=True)

with col_bimbo:
    # Immagine bambino (placeholder affidabile)
    st.image("https://piccoliesploratori.com")

# --- 5. PULSANTE ---
# Ora il pulsante prenderà tutta la larghezza grazie al CSS sopra
if st.button("Scegli la tua Box"):
    st.toast("Caricamento...")

# --- 6. FOOTER ---
st.markdown("""
    <div class="footer-note">
        <span style="color:#f43f5e;">❤️</span> Creato da genitori, per genitori.
    </div>
    """, unsafe_allow_html=True)
