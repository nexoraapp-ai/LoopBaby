import streamlit as st

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- LOGICA DI NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- CSS TOTALE (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    /* Reset Totale */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}

    /* Immagine Hero Bambino (Piena larghezza) */
    .hero-img {
        width: 100%;
        height: 320px;
        background-image: url('https://unsplash.com');
        background-size: cover;
        background-position: center;
        border-bottom-left-radius: 40px;
        border-bottom-right-radius: 40px;
        margin-bottom: 20px;
    }

    /* Titoli e Testi */
    .titolo { color: #0d9488; font-size: 32px; font-weight: 900; padding: 0 20px; line-height: 1.1; margin-bottom: 10px; }
    .paragrafo { color: #64748b; padding: 0 20px; font-size: 16px; margin-bottom: 20px; }

    /* CARD DELLE BOX */
    .card { border-radius: 25px; padding: 25px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .luna { background-color: #f8fafc; color: #1e293b; }
    .sole { background-color: #fffbeb; color: #92400e; }
    .nuvola { background-color: #f1f5f9; color: #334155; }
    .premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }

    .prezzo-rosa { color: #ec4899; font-size: 26px; font-weight: 900; display: block; margin-top: 10px; }
    .prezzo-bianco { color: white !important; font-size: 26px; font-weight: 900; display: block; margin-top: 10px; }

    /* Pulsante Rosa Cliccabile */
    div.stButton > button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        width: 85% !important;
        height: 60px !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 12px rgba(236,72,153,0.3) !important;
    }

    /* BARRA NAVIGAZIONE IN BASSO FISSA */
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #f1f5f9;
        z-index: 99999;
        display: flex;
        justify-content: center;
        padding: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENUTI ---

if st.session_state.pagina == "Home":
    st.markdown('<div class="hero-img"></div>', unsafe_allow_html=True)
    st.markdown('<div class="titolo">Vestiamo il tuo bambino con amore e qualità.</div>', unsafe_allow_html=True)
    st.markdown('<div class="paragrafo">Il noleggio circolare che cresce con lui. Risparmia tempo, spazio e denaro.</div>', unsafe_allow_html=True)
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding-top:40px;" class="titolo">Le nostre Box</div>', unsafe_allow_html=True)
    st.markdown('<div class="paragrafo"><b>Standard:</b> capi usati garantiti.<br><b>Premium:</b> capi nuovi o seminuovi.</div>', unsafe_allow_html=True)
    
    # LUNA
    st.markdown('<div class="card luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
    if st.button("Prendi LUNA"): st.toast("Luna selezionata")

    # SOLE
    st.markdown('<div class="card sole"><h3>SOLE ☀️</h3><p>Colori e Allegria</p><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
    if st.button("Prendi SOLE"): st.toast("Sole selezionata")

    # NUVOLA
    st.markdown('<div class="card nuvola"><h3>NUVOLA ☁️</h3><p>Casual e Denim Style</p><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
    if st.button("Prendi NUVOLA"): st.toast("Nuvola selezionata")

    # PREMIUM
    st.markdown('<div class="card premium"><h3 style="color:white;">PREMIUM 💎</h3><p style="color:white;">Grandi Firme Nuove</p><span class="prezzo-bianco">29,90€</span></div>', unsafe_allow_html=True)
    if st.button("Prendi PREMIUM"): st.toast("Premium selezionata")

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding-top:40px;" class="titolo">Vetrina Shop</div>', unsafe_allow_html=True)
    st.markdown('<div class="paragrafo">Questi capi rimangono a te per sempre!</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕<br>Body Bio<br><b class="prezzo-rosa">9,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="s1")
    with col2:
        st.markdown('<div class="card">👖<br>Salopette<br><b class="prezzo-rosa">19,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="s2")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding-top:40px;" class="titolo">Come Funziona</div>', unsafe_allow_html=True)
    st.markdown('<div class="card luna"><b>1. Ricevi la Box</b><br><b>2. Usala 90 giorni</b><br><b>3. Rendi e cambia taglia</b><br><br><i>Il reso è GRATIS se rinnovi!</i></div>', unsafe_allow_html=True)

# --- NAVBAR FISSA ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]: 
    if st.button("🏠\nHome"): vai("Home")
with cols[1]: 
    if st.button("📦\nBox"): vai("Box")
with cols[2]: 
    if st.button("🛍️\nShop"): vai("Shop")
with cols[3]: 
    if st.button("📖\nInfo"): vai("Info")
st.markdown('</div>', unsafe_allow_html=True)

# Fix finale per i bottoni della barra
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] {
    position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
    background: white !important; border-top: 1px solid #eee !important; z-index: 999999 !important;
    display: flex !important; justify-content: center !important;
}
[data-testid="stHorizontalBlock"] [data-testid="column"] { width: 25% !important; flex: none !important; }
[data-testid="stHorizontalBlock"] button {
    background: transparent !important; color: #0d9488 !important; border: none !important;
    box-shadow: none !important; font-size: 11px !important; font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)
