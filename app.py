import streamlit as st

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- CSS DEFINITIVO (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    /* Nascondi tutto lo sporco di Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 500px !important; margin: 0 auto !important;}
    
    /* Font */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header Logo */
    .header-logo { display: flex; align-items: center; padding: 20px; gap: 10px; }
    .logo-text { font-size: 24px; font-weight: 800; color: #1e293b; }
    .logo-sub { font-size: 12px; color: #64748b; margin-top: -5px; }

    /* Layout Home: Testo a Sinistra, Bimbo a Destra */
    .home-container { display: flex; align-items: center; padding: 0 20px; gap: 10px; }
    .home-text { flex: 1.2; }
    .home-img-container { flex: 1; }
    .home-img { width: 100%; border-radius: 20px; }

    /* Titoli */
    .ciao-mamma { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
    .headline { font-size: 16px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }

    /* Lista Punti Elenco con Icone */
    .list-item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #475569; margin-bottom: 12px; font-weight: 500; }
    .icon { color: #0d9488; font-size: 18px; }

    /* Pulsante Rosa Originale */
    div.stButton > button {
        background: #f43f5e !important; /* Rosa caldo della foto */
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
        margin-top: 20px;
    }

    /* Footer */
    .footer-text { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 30px; display: flex; align-items: center; justify-content: center; gap: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENUTO ---

# 1. HEADER LOGO
st.markdown("""
    <div class="header-logo">
        <img src="https://flaticon.com" width="40">
        <div>
            <div class="logo-text">LoopBaby</div>
            <div class="logo-sub">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. SEZIONE PRINCIPALE (TESTO + IMMAGINE)
st.markdown("""
    <div class="home-container">
        <div class="home-text">
            <div class="ciao-mamma">Ciao Mamma! 👋</div>
            <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
            
            <div class="list-item"><span class="icon">👕</span> Capi di qualità selezionati</div>
            <div class="list-item"><span class="icon">🔄</span> Cambi quando cresce</div>
            <div class="list-item"><span class="icon">💰</span> Risparmi più di 1000€ l'anno</div>
            <div class="list-item"><span class="icon">📍</span> Scegli il locker più vicino a te</div>
            <div class="list-item"><span class="icon">🧘</span> Zero stress per te</div>
        </div>
        <div class="home-img-container">
            <img src="https://unsplash.com" class="home-img">
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. PULSANTE AZIONE
if st.button("Scegli la tua Box"):
    st.toast("Caricamento Box...")

# 4. FOOTER
st.markdown("""
    <div class="footer-text">
        <span style="color:#f43f5e;">❤️</span> Creato da genitori, per genitori.
    </div>
    """, unsafe_allow_html=True)
