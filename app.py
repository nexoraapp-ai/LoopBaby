import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS TOTALE (COPIA FEDELE) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    .logo-area { padding: 15px 20px; }
    .logo-h { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .heart { color: #f43f5e; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* Layout a due colonne REALI */
    .row { display: flex; align-items: flex-start; padding: 0 20px; gap: 10px; }
    .col-left { flex: 1.6; }
    .col-right { flex: 1; }

    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .head { font-size: 14px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    
    .item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 8px; }
    .baby-frame { width: 100%; border-radius: 25px; background: #f1f5f9; }

    /* PULSANTE ROSA LARGO */
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

# --- 3. HEADER ---
st.markdown("""
    <div class="logo-area">
        <div class="logo-h"><span class="heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. CORPO (COLONNE HTML) ---
st.markdown("""
    <div class="row">
        <div class="col-left">
            <div class="ciao">Ciao Mamma! 👋</div>
            <div class="head">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
            <div class="item">👕 Capi di qualità selezionati</div>
            <div class="item">🔄 Cambi quando cresce</div>
            <div class="item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="item">📍 Scegli il locker più vicino</div>
            <div class="item">✨ Zero stress per te</div>
        </div>
        <div class="col-right">
            <img src="https://piccoliesploratori.com" class="baby-frame">
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PULSANTE ---
if st.button("Scegli la tua Box"):
    st.toast("Ecco le Box!")

st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:20px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)
