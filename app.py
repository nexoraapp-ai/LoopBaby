import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STATO DELLA PAGINA ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def cambia_pag(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- 3. DESIGN IDENTICO (CSS CUSTOM) ---
st.markdown("""
    <style>
    /* Nascondi tutto ciò che è Streamlit */
    #MainMenu, header, footer { visibility: hidden !important; }
    .stApp { background-color: #FFFFFF !important; max-width: 450px; margin: 0 auto; }
    
    /* Font e Colori Moodboard */
    h1 { color: #0d9488 !important; font-family: 'Helvetica', sans-serif; font-size: 28px !important; font-weight: 800; line-height: 1.2; }
    h3 { color: #0d9488 !important; font-size: 20px; font-weight: 700; margin-bottom: 5px; }
    p { color: #64748b !important; font-size: 15px; }

    /* Immagine Bambino */
    .img-hero { width: 100%; border-radius: 25px; margin-bottom: 20px; }

    /* Card delle Box */
    .box-card {
        background: #f8fafc;
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .prezzo-rosa { color: #ec4899 !important; font-size: 24px; font-weight: 900; margin: 10px 0; }

    /* Tasto Rosa Identico alla Foto */
    div.stButton > button {
        background-color: #ec4899 !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    }

    /* BARRA DI NAVIGAZIONE IN BASSO FISSA */
    .footer-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #eee;
        padding: 10px 0;
        z-index: 1000;
        display: flex;
        justify-content: space-around;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO PAGINE ---

# -- PAGINA: HOME --
if st.session_state.pagina == "Home":
    st.image("logo.png", width=130)
    
    # Immagine Bambino (Hero)
    st.markdown('<img src="https://unsplash.com" class="img-hero">', unsafe_allow_html=True)
    
    st.markdown("<h1>Vestiamo il tuo bambino con amore e qualità.</h1>", unsafe_allow_html=True)
    st.write("Entra nel mondo di LoopBaby: il noleggio che cresce con il tuo bebè, facendoti risparmiare tempo e rispettando il pianeta.")
    
    if st.button("SCEGLI LA TUA BOX ➔"):
        cambia_pag("Box")

# -- PAGINA: BOX --
elif st.session_state.pagina == "Box":
    st.markdown("<h1 style='color:#0d9488;'>Le nostre Box</h1>", unsafe_allow_html=True)
    st.write("Scegli lo stile che preferisci per il tuo bebè.")

    # 3 BOX STANDARD
    st.markdown('<div class="box-card"><h3>LUNA 🌙</h3><p>Colori neutri e rilassanti</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli LUNA"): st.toast("Luna selezionata!")

    st.markdown('<div class="box-card"><h3>SOLE ☀️</h3><p>Energia, colori e allegria</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli SOLE"): st.toast("Sole selezionata!")

    st.markdown('<div class="box-card"><h3>NUVOLA ☁️</h3><p>Casual e Denim quotidiano</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli NUVOLA"): st.toast("Nuvola selezionata!")

    # 1 BOX PREMIUM
    st.markdown('<div class="box-card" style="border: 2px solid #0d9488;"><h3>DIAMANTE 💎</h3><p>Grandi firme e lusso</p><div class="prezzo-rosa">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli PREMIUM"): st.toast("Premium selezionata!")

# -- PAGINA: SHOP --
elif st.session_state.pagina == "Shop":
    st.markdown("<h1 style='color:#0d9488;'>Vetrina Shop</h1>", unsafe_allow_html=True)
    st.info("Spedizione GRATIS sopra i 50€")
    # Qui andranno i capi singoli come visti in foto

# -- PAGINA: PROFILO --
elif st.session_state.pagina == "Profilo":
    st.markdown("<h1 style='color:#0d9488;'>Il mio Profilo</h1>", unsafe_allow_html=True)
    st.write("Gestisci i tuoi ordini e i tuoi dati.")

# --- 5. BARRA DI NAVIGAZIONE IN BASSO FUNZIONANTE ---
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True) # Spazio per non coprire il contenuto

# Container fisso per i bottoni
st.markdown('<div class="footer-nav">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🏠\nHome", key="n1"): cambia_pag("Home")
with c2:
    if st.button("📦\nBox", key="n2"): cambia_pag("Box")
with c3:
    if st.button("🛍️\nShop", key="n3"): cambia_pag("Shop")
with c4:
    if st.button("👤\nProfilo", key="n4"): cambia_pag("Profilo")

# Stile extra per i bottoni della barra (trasparenti e piccoli)
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white !important;
        padding: 10px 0 !important;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important;
        color: #0d9488 !important;
        border: none !important;
        font-size: 11px !important;
        height: auto !important;
        box-shadow: none !important;
        text-transform: none !important;
    }
    </style>
""", unsafe_allow_html=True)
