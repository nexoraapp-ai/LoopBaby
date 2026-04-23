import streamlit as st

# --- 1. SETUP ---
st.set_page_config(page_title="LoopBaby App", page_icon="logo.png", layout="centered")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS TOTALE (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden !important; }
    .stApp { background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto; }
    
    /* Immagine Hero */
    .hero-bambino {
        width: 100%;
        height: 280px;
        background-image: url('https://unsplash.com');
        background-size: cover;
        background-position: center;
        border-bottom-left-radius: 40px;
        border-bottom-right-radius: 40px;
    }

    .titolo-verde { color: #0d9488 !important; font-size: 30px !important; font-weight: 900; padding: 20px; line-height: 1.1; }
    .sottotitolo { color: #64748b; padding: 0 20px; font-size: 16px; margin-top: -10px; }

    /* Card Box */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .prezzo-bianco { color: white !important; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa */
    div.stButton > button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 90% !important;
        height: 55px !important;
        font-weight: bold !important;
        margin: 0 auto !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# --- HOME ---
if st.session_state.pagina == "Home":
    st.markdown('<div class="hero-bambino"></div>', unsafe_allow_html=True)
    st.markdown('<div class="titolo-verde">Vestiamo il tuo bambino con amore e qualità.</div>', unsafe_allow_html=True)
    st.markdown('<p class="sottotitolo">Il noleggio circolare che cresce con lui. Risparmia tempo e denaro.</p>', unsafe_allow_html=True)
    st.write("")
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

# --- BOX ---
elif st.session_state.pagina == "Box":
    st.markdown('<h1 class="titolo-verde">Le nostre Box</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sottotitolo"><b>Standard:</b> capi usati garantiti.<br><b>Premium:</b> capi nuovi o seminuovi.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Stile neutro e delicato</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli LUNA"): st.toast("Luna selezionata")

    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori ed energia</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli SOLE"): st.toast("Sole selezionata")

    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual e Jeans</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli NUVOLA"): st.toast("Nuvola selezionata")

    st.markdown('<div class="card box-premium"><h3 style="color:white;">PREMIUM 💎</h3><p style="color:white;">Grandi Firme Nuove</p><div class="prezzo-bianco">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli PREMIUM"): st.toast("Premium selezionata")

# --- SHOP ---
elif st.session_state.pagina == "Shop":
    st.markdown('<h1 class="titolo-verde">Vetrina Shop</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sottotitolo">Questi capi rimangono a te per sempre!</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕<br>Body Bio<br><b class="prezzo-rosa">9,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh1")
    with col2:
        st.markdown('<div class="card">👖<br>Salopette<br><b class="prezzo-rosa">19,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh2")

# --- INFO ---
elif st.session_state.pagina == "Info":
    st.markdown('<h1 class="titolo-verde">Come Funziona</h1>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>1. Ricevi la Box</b><br><b>2. Usala per 90 giorni</b><br><b>3. Cambia taglia</b> e rendi.<br><br><i>Il reso è gratis se rinnovi!</i></div>', unsafe_allow_html=True)

# --- 5. BARRA NAVIGAZIONE ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
st.markdown("""<style>
    [data-testid="stHorizontalBlock"] { position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important; background: white !important; border-top: 1px solid #eee !important; z-index: 99999; }
    [data-testid="stHorizontalBlock"] button { background: transparent !important; color: #0d9488 !important; border: none !important; box-shadow: none !important; font-size: 11px !important; height: 50px !important; }
</style>""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Shop")
with c4: 
    if st.button("📖\nInfo"): vai("Info")
