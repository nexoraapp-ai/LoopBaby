import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS TOTALE (FORZA IL LAYOUT AFFIANCATO) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Layout a due colonne che non crolla */
    .home-flex {
        display: flex;
        align-items: center;
        padding: 20px;
        gap: 15px;
    }
    .col-testo { flex: 1.5; }
    .col-bimbo { flex: 1; }

    /* Stile Testi */
    .logo-h { font-size: 32px; font-weight: 800; color: #1e293b; margin: 0; }
    .heart { color: #f43f5e; }
    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-top: 10px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    
    /* Lista icone */
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-top: 8px; }

    /* SEGNAPOSTO IMMAGINE (Questo apparirà sicuramente) */
    .baby-placeholder {
        width: 100%;
        height: 180px;
        background-color: #f1f5f9;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        border: 2px dashed #cbd5e1;
    }

    /* Pulsante Rosa FULL WIDTH */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 20px auto !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTENUTO ---

# Logo
st.markdown('<h1 class="logo-h"><span class="heart">💗</span> LoopBaby</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b; padding-left:25px;">Vestiamo il tuo bambino, rispettiamo il futuro.</p>', unsafe_allow_html=True)

# Layout Affiancato
st.markdown(f"""
    <div class="home-flex">
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
            <div class="baby-placeholder">FOTO <br> BIMBO</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Pulsante
if st.button("Scegli la tua Box"):
    st.toast("Aprendo...")

st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:20px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)
