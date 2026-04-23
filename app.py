import streamlit as st

# --- 1. CONFIGURAZIONE ZERO-UI (Elimina tutto lo stile Streamlit) ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def nav(target):
    st.session_state.pagina = target
    st.rerun()

# --- 2. CSS TOTALE (IDENTICO AL DESIGN) ---
st.markdown("""
    <style>
    /* Reset radicale */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .main .block-container {padding: 0 !important; max-width: 420px !important; margin: 0 auto;}
    .stApp {background-color: #FFFFFF !important;}

    /* Font e Titoli Moodboard */
    @import url('https://googleapis.com');
    * {font-family: 'Outfit', sans-serif !important;}
    
    .titolo-grande {
        color: #0d9488;
        font-size: 34px;
        font-weight: 900;
        line-height: 1.1;
        padding: 20px;
        margin-top: -10px;
    }

    /* Immagine Bambino Full Width */
    .hero-img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-bottom-left-radius: 40px;
        border-bottom-right-radius: 40px;
    }

    /* Card Box Pulite */
    .card-box {
        background: #F1F5F9;
        border-radius: 30px;
        padding: 25px;
        margin: 15px 20px;
        text-align: center;
        border: none;
    }
    .box-title { color: #0d9488; font-size: 22px; font-weight: 800; margin-bottom: 5px; }
    .box-price { color: #ec4899; font-size: 26px; font-weight: 900; }

    /* Pulsanti Call-to-Action Rosa */
    div.stButton > button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 85% !important;
        height: 65px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        display: block;
        margin: 0 auto !important;
        box-shadow: 0 10px 20px rgba(236, 72, 153, 0.2) !important;
    }

    /* BARRA NAVIGAZIONE INFERIORE (STILE APP NATIVA) */
    .nav-bar-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        max-width: 420px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid #E2E8F0;
        padding: 15px 0;
        z-index: 9999;
        display: flex;
        justify-content: space-around;
    }
    
    /* Spazio finale per non coprire i contenuti */
    .footer-spacer { height: 120px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA PAGINE ---

# -- HOME --
if st.session_state.pagina == "Home":
    st.markdown('<img src="https://unsplash.com" class="hero-img">', unsafe_allow_html=True)
    st.markdown('<div style="padding: 20px;"><img src="https://vostro-sito.com" width="120"></div>', unsafe_allow_html=True)
    st.markdown('<div class="titolo-grande">Vestiamo il tuo bambino con amore e qualità.</div>', unsafe_allow_html=True)
    st.markdown('<p style="padding: 0 20px; color: #64748b;">Il noleggio circolare intelligente: capi bio, grandi firme e cambio taglia senza stress.</p>', unsafe_allow_html=True)
    st.write("")
    if st.button("SCEGLI LA TUA BOX ➔"):
        nav("Box")

# -- BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 40px 20px 10px 20px;"><h2 style="color:#0d9488; font-weight:900; font-size:32px;">Le nostre Box</h2><p>10 capi selezionati per 90 giorni.</p></div>', unsafe_allow_html=True)
    
    # 3 STANDARD
    for stile, icona, desc in [("LUNA", "🌙", "Neutro e Panna"), ("SOLE", "☀️", "Colori e Allegria"), ("NUVOLA", "☁️", "Casual e Jeans")]:
        st.markdown(f'''
            <div class="card-box">
                <div class="box-title">{stile} {icona}</div>
                <p style="margin-bottom:10px;">{desc}</p>
                <div class="box-price">19,90€</div>
            </div>
        ''', unsafe_allow_html=True)
        st.button(f"PRENDI {stile}", key=stile)

    # 1 PREMIUM
    st.markdown('''
        <div class="card-box" style="background: #0d9488; color: white;">
            <div class="box-title" style="color:white;">PREMIUM 💎</div>
            <p style="color:white; opacity:0.8;">Capi Grandi Firme</p>
            <div class="box-price" style="color:white;">29,90€</div>
        </div>
    ''', unsafe_allow_html=True)
    st.button("PRENDI PREMIUM", key="premium")

# -- SHOP --
elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding: 40px 20px;"><h2 style="color:#0d9488; font-weight:900;">Vetrina Shop</h2><p>Spedizione gratis sopra i 50€</p></div>', unsafe_allow_html=True)
    # Esempio prodotto
    st.markdown('<div class="card-box"><div class="box-title">Body Bio 🌱</div><div class="box-price">9,90€</div></div>', unsafe_allow_html=True)
    st.button("COMPRA ORA")

# --- 4. BARRA DI NAVIGAZIONE FISSA (LOGICA STREAMLIT) ---
st.markdown('<div class="footer-spacer"></div>', unsafe_allow_html=True)

# Iniezione dei bottoni della barra
st.markdown("""<style>
    [data-testid="stHorizontalBlock"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background: white !important;
        padding: 10px !important;
        z-index: 10000 !important;
        border-top: 1px solid #eee !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important;
        color: #0d9488 !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 12px !important;
        height: auto !important;
    }
</style>""", unsafe_allow_html=True)

cols = st.columns(4)
with cols[0]:
    if st.button("🏠\nHome"): nav("Home")
with cols[1]:
    if st.button("📦\nBox"): nav("Box")
with cols[2]:
    if st.button("🛍️\nShop"): nav("Shop")
with cols[3]:
    if st.button("👤\nProfilo"): nav("Home") # Placeholder per ora
