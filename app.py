import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS PER COPIARE LA FOTO IDENTICA ---
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

    /* Layout Home: Testo e Bimbo affiancati */
    .container-home { 
        display: flex; 
        align-items: center; 
        padding: 0 20px; 
        gap: 15px; 
        margin-top: 10px; 
    }
    .col-testo { flex: 1.6; }
    .col-bimbo { flex: 1; }

    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin: 0; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-top: 10px; margin-bottom: 15px; }

    /* Lista con icone */
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); object-fit: cover; }

    /* Pulsante Rosa FULL WIDTH */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Footer */
    .footer-note { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 30px; padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTENUTO ---

# Logo e Header
st.markdown("""
    <div class="header-box">
        <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# Corpo Centrale con Immagine che CARICA SICURAMENTE
st.markdown("""
    <div class="container-home">
        <div class="col-testo">
            <div class="ciao">Ciao Mamma! 👋</div>
            <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
            <div class="list-item">👕 Capi di qualità selezionati</div>
            <div class="list-item">🔄 Cambi quando cresce</div>
            <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="list-item">📍 Scegli il locker più vicino</div>
            <div class="list-item">✨ Zero stress per te</div>
        </div>
        <div class="col-bimbo">
            <img src="https://unsplash.com" class="baby-img">
        </div>
    </div>
    """, unsafe_allow_html=True)

# Pulsante (Sopra il footer)
if st.button("Scegli la tua Box"):
    st.toast("Caricamento Box...")

# Footer
st.markdown("""
    <div class="footer-note">
        ❤️ Creato da genitori, per genitori.
    </div>
    """, unsafe_allow_html=True)
