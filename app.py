import streamlit as st

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- DATABASE TEMPORANEO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# --- LOGICA DI NAVIGAZIONE ---
query_params = st.query_params
if "p" in query_params:
    st.session_state.pagina = query_params["p"]

# --- STILE CSS TOTALE (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    /* Reset totale per sembrare un'app */
    [data-testid="stAppViewContainer"] { background-color: #FFFFFF; }
    [data-testid="stHeader"], [data-testid="stToolbar"] { visibility: hidden !important; }
    .main .block-container { padding: 20px; max-width: 450px; }

    /* Font e Titoli */
    h1, h2, h3, .titolo-verde { color: #0d9488 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    p { color: #475569; font-size: 14px; }

    /* CARD DELLE BOX (3 STANDARD + 1 PREMIUM) */
    .card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .prezzo-rosa { color: #ec4899 !important; font-size: 22px; font-weight: 900; margin: 10px 0; }
    
    /* BOTTONE ROSA IDENTICO */
    .stButton > button {
        background-color: #ec4899 !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* BARRA DI NAVIGAZIONE IN BASSO (FISSA E CLICCABILE) */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 75px;
        background: white;
        border-top: 1px solid #E2E8F0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 9999;
    }
    .nav-item {
        text-align: center;
        color: #0d9488;
        text-decoration: none;
        font-size: 12px;
        font-weight: bold;
        flex: 1;
    }
    .nav-icon { font-size: 22px; display: block; margin-bottom: 2px; }
    
    /* FIX PER NON FAR COPRIRE IL CONTENUTO DALLA BARRA */
    .spacer { height: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENUTO PAGINE ---

# 1. HOME
if st.session_state.pagina == "Home":
    st.image("logo.png", width=140) if st.session_state.pagina == "Home" else None
    st.markdown("<h1 style='font-size: 32px;'>Vestiamo il tuo bambino con amore e qualità.</h1>", unsafe_allow_html=True)
    st.write("Scegli il noleggio circolare: risparmi tempo, spazio e aiuti l'ambiente.")
    if st.button("SCEGLI LA TUA BOX ➔"):
        st.session_state.pagina = "Box"
        st.rerun()

# 2. BOX (IDENTICHE A FOTO)
elif st.session_state.pagina == "Box":
    st.markdown("<h2 class='titolo-verde'>Le nostre Box</h2>", unsafe_allow_html=True)
    st.write("10 capi per 90 giorni. Scegli lo stile che preferisci.")

    # BOX STANDARD - LUNA
    st.markdown('<div class="card"><h3>LUNA 🌙</h3><p>Colori neutri, panna e grigio</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI LUNA"): st.success("Luna aggiunta!")

    # BOX STANDARD - SOLE
    st.markdown('<div class="card"><h3>SOLE ☀️</h3><p>Colori vivaci e fantasie</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI SOLE"): st.success("Sole aggiunta!")

    # BOX STANDARD - NUVOLA
    st.markdown('<div class="card"><h3>NUVOLA ☁️</h3><p>Casual e Denim style</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI NUVOLA"): st.success("Nuvola aggiunta!")

    # BOX PREMIUM
    st.markdown('<div class="card" style="border: 2px solid #0d9488;"><h3>PREMIUM 💎</h3><p>Grandi firme selezionate</p><div class="prezzo-rosa">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI PREMIUM"): st.success("Premium aggiunta!")

# 3. SHOP
elif st.session_state.pagina == "Shop":
    st.markdown("<h2 class='titolo-verde'>Vetrina Shop</h2>", unsafe_allow_html=True)
    st.info("Spedizione GRATIS sopra i 50€")
    # Qui andranno i capi singoli come nel codice precedente

# 4. CHI SIAMO
elif st.session_state.pagina == "ChiSiamo":
    st.markdown("<h2 class='titolo-verde'>Chi Siamo</h2>", unsafe_allow_html=True)
    st.write("Siamo genitori che hanno creato LoopBaby per semplificare la vita alle famiglie.")

# Spaziatore finale per la barra
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# --- BARRA DI NAVIGAZIONE IN BASSO (HTML PURO) ---
# Usiamo i link con parametri per far funzionare i click
st.markdown(f"""
    <div class="nav-bar">
        <a class="nav-item" href="/?p=Home" target="_self"><span class="nav-icon">🏠</span>Home</a>
        <a class="nav-item" href="/?p=Box" target="_self"><span class="nav-icon">📦</span>Box</a>
        <a class="nav-item" href="/?p=Shop" target="_self"><span class="nav-icon">🛍️</span>Shop</a>
        <a class="nav-item" href="/?p=ChiSiamo" target="_self"><span class="nav-icon">👋</span>Chi Siamo</a>
    </div>
    """, unsafe_allow_html=True)
