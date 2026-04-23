import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. IL TRUCCO CSS (Questo non fallisce mai) ---
st.markdown("""
    <style>
    /* Nascondi sporco Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Forziamo le colonne a stare vicine anche su cellulare */
    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 150px !important;
    }

    /* Testi */
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .list-item { font-size: 13px; color: #475569; margin-bottom: 8px; font-weight: 500; }

    /* Pulsante Rosa GIGANTE */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        height: 65px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }
    
    /* Arrotonda l'immagine del bambino */
    [data-testid="stImage"] img {
        border-radius: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTENUTO (Usiamo i blocchi Streamlit) ---

# Logo e Slogan
st.markdown('<h1 style="color:#1e293b; font-weight:800; font-size:35px; margin-bottom:0;">💗 LoopBaby</h1>', unsafe_allow_html=True)
st.write("Vestiamo il tuo bambino, rispettiamo il futuro.")

st.write("") # Spazio

# Layout a due colonne: Testo a sinistra, Bimbo a destra
col_testo, col_bimbo = st.columns([1.5, 1])

with col_testo:
    st.markdown('<div class="ciao">Ciao Mamma! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="list-item">👕 Capi di qualità selezionati</div>', unsafe_allow_html=True)
    st.markdown('<div class="list-item">🔄 Cambi quando cresce</div>', unsafe_allow_html=True)
    st.markdown('<div class="list-item">💰 Risparmi più di 1000€ l\'anno</div>', unsafe_allow_html=True)
    st.markdown('<div class="list-item">📍 Scegli il locker più vicino</div>', unsafe_allow_html=True)
    st.markdown('<div class="list-item">✨ Zero stress per te</div>', unsafe_allow_html=True)

with col_bimbo:
    # Questa foto caricherà sempre perché è un componente nativo
    st.image("https://unsplash.com")

# Pulsante Rosa Largo
st.write("")
if st.button("Scegli la tua Box"):
    st.balloons() # Animazione per festeggiare il funzionamento!

# Footer
st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:40px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)
