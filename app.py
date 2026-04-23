import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. STILE CSS (TUTTO IN UN UNICO BLOCCO) ---
st.markdown("""
    <style>
    /* Nascondi elementi Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header Logo */
    .header-container { padding: 20px; }
    .logo-text { font-size: 28px; font-weight: 800; color: #1e293b; margin: 0; }
    .logo-sub { font-size: 13px; color: #64748b; margin-top: -5px; }

    /* Layout Home: Flexbox per affiancare */
    .home-flex { 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        padding: 0 20px; 
        gap: 15px; 
    }
    .home-text { flex: 1.5; }
    .home-img-container { flex: 1; text-align: right; }
    .home-img { width: 100%; border-radius: 30px; object-fit: cover; }

    /* Titoli e Elenco */
    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }

    /* Pulsante Rosa */
    div.stButton > button {
        background: #f43f5e !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 20px;
    }

    /* Footer */
    .footer-custom { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 40px; padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO E HEADER ---
st.markdown("""
    <div class="header-container">
        <h1 class="logo-text">💗 LoopBaby</h1>
        <p class="logo-sub">Vestiamo il tuo bambino, rispettiamo il futuro.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SEZIONE CENTRALE (FLEX) ---
# Usiamo il Flexbox HTML per forzare il layout affiancato
st.markdown("""
    <div class="home-flex">
        <div class="home-text">
            <div class="ciao">Ciao Mamma! 👋</div>
            <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
            <div class="list-item">👕 Capi di qualità selezionati</div>
            <div class="list-item">🔄 Cambi quando cresce</div>
            <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="list-item">📍 Scegli il locker più vicino a te</div>
            <div class="list-item">✨ Zero stress per te</div>
        </div>
        <div class="home-img-container">
            <img src="https://unsplash.com" class="home-img">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PULSANTE E FOOTER ---
# Il pulsante lo teniamo fuori dal blocco HTML per farlo funzionare con Streamlit
if st.button("Scegli la tua Box"):
    st.switch_page("pages/box.py") # O la tua logica di cambio pagina

st.markdown("""
    <div class="footer-custom">
        ❤️ Creato da genitori, per genitori.
    </div>
    """, unsafe_allow_html=True)
