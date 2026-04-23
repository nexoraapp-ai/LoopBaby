import streamlit as st
import os

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS PROFESSIONALE ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    .header-box { padding: 20px 20px 10px 20px; }
    .logo-h { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .heart { color: #f43f5e; font-size: 35px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout che NON CROLLA */
    .main-grid { display: flex; align-items: center; padding: 0 20px; gap: 10px; }
    .col-left { flex: 1.6; }
    .col-right { flex: 1; }

    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 10px; font-weight: 500; }

    /* Pulsante Rosa */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 10px auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Barra Bassa Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 11px !important; height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# Logo Fisso
st.markdown("""
    <div class="header-box">
        <div class="logo-h"><span class="heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# -- PAGINA HOME --
if st.session_state.pagina == "Home":
    # Layout con Colonne Streamlit (più stabili per le foto locali)
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        st.markdown('<div class="ciao">Ciao Mamma! 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="list-item">👕 Capi di qualità selezionati</div>
            <div class="list-item">🔄 Cambi quando cresce</div>
            <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="list-item">📍 Scegli il locker più vicino</div>
            <div class="list-item">✨ Zero stress per te</div>
        """, unsafe_allow_html=True)

    with col2:
        # Carica la foto bimbo.jpg se presente
        if os.path.exists("bimbo.jpg"):
            st.image("bimbo.jpg")
        else:
            st.markdown('<div style="width:100%; height:150px; background:#f1f5f9; border-radius:20px; display:flex; align-items:center; justify-content:center; color:#94a3b8; font-size:10px; text-align:center; border:2px dashed #ccc;">Metti la foto<br>bimbo.jpg<br>nella cartella</div>', unsafe_allow_html=True)

    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Home")
with c4: 
    if st.button("👤\nProfilo"): vai("Home")
