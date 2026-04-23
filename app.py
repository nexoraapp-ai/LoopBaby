import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS PER COPIARE LA FOTO ALLA PERFEZIONE ---
st.markdown("""
    <style>
    /* Nascondi tutto lo sporco di Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font Professionale */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo in alto */
    .header-box { padding: 20px 20px 10px 20px; }
    .logo-title { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; font-size: 35px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout a due colonne (Testo e Bimbo) */
    .main-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .text-cell { width: 60%; vertical-align: top; padding-left: 20px; }
    .img-cell { width: 40%; vertical-align: top; padding-right: 15px; }
    
    .ciao-mamma { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }

    /* Lista con icone */
    .punti-elenco { font-size: 12px; color: #475569; line-height: 2.2; font-weight: 500; list-style: none; padding: 0; }

    /* Immagine Bimbo */
    .baby-img { width: 100%; border-radius: 30px; }

    /* Pulsante Rosa FULL WIDTH */
    div.stButton > button {
        background: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 20px auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Footer */
    .footer-note { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER (LOGO) ---
st.markdown("""
    <div class="header-box">
        <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. CORPO CENTRALE (TESTO + BIMBO AFFIANCATI) ---
st.markdown("""
    <table class="main-table">
        <tr>
            <td class="text-cell">
                <div class="ciao-mamma">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <ul class="punti-elenco">
                    <li>👕 Capi di qualità selezionati</li>
                    <li>🔄 Cambi quando cresce</li>
                    <li>💰 Risparmi più di 1000€ l'anno</li>
                    <li>📍 Scegli il locker più vicino a te</li>
                    <li>✨ Zero stress per te</li>
                </ul>
            </td>
            <td class="img-cell">
                <img src="https://unsplash.com" class="baby-img">
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# --- 5. PULSANTE ---
# Lo teniamo fuori dall'HTML per farlo funzionare al click
if st.button("Scegli la tua Box"):
    st.toast("Caricamento Box...")

# --- 6. FOOTER ---
st.markdown("""
    <div class="footer-note">
        <span style="color:#f43f5e;">❤️</span> Creato da genitori, per genitori.
    </div>
    """, unsafe_allow_html=True)
