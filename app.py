import streamlit as st
import os

# --- 1. CONFIGURAZIONE LAYOUT ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS PER SISTEMARE LE DIMENSIONI (IDENTICO ALLA MOODBOARD) ---
st.markdown("""
    <style>
    /* Forza la larghezza cellulare */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header e Logo */
    .header-box { padding: 25px 20px 10px 20px; }
    .logo-h { font-size: 36px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .heart { color: #f43f5e; font-size: 38px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home Bilanciato */
    .ciao { font-size: 30px; font-weight: 800; color: #1e293b; margin-bottom: 5px; padding: 0 20px; }
    .headline { font-size: 17px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; padding: 0 20px; }
    
    /* Lista icone grandi */
    .list-container { padding: 0 20px; }
    .list-item { display: flex; align-items: center; gap: 12px; font-size: 14px; color: #475569; margin-bottom: 12px; font-weight: 500; }

    /* Pulsante Rosa GIGANTE */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 90% !important;
        height: 65px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 30px auto !important;
        display: block !important;
        box-shadow: 0 5px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Barra Navigazione Inferiore con Icone Grandi */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999; 
        padding: 10px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 12px !important; height: auto !important;
        font-weight: bold !important;
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
    # Layout Proporzionato
    col_testo, col_bimbo = st.columns([1.2, 1])
    
    with col_testo:
        st.markdown('<div class="ciao">Ciao Mamma! 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="headline">Vestiamo il tuo bambino con amore e qualità.</div>', unsafe_allow_html=True)
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
        # Carica la foto locale bimbo.jpg con bordi arrotondati
        if os.path.exists("bimbo.jpg"):
            st.image("bimbo.jpg", use_container_width=True)
        else:
            st.warning("Carica bimbo.jpg")

    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

# -- PAGINA BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="padding:20px; color:#0d9488;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    st.markdown('<div style="background:#f8fafc; border-radius:20px; padding:20px; margin:10px; border:1px solid #ddd; text-align:center;"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><h2 style="color:#ec4899;">19,90€</h2></div>', unsafe_allow_html=True)
    st.button("SELEZIONA LUNA")

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
