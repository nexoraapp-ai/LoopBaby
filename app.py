import streamlit as st

# --- 1. CONFIGURAZIONE E AZZERAMENTO UI ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

# --- 2. CSS HARDCORE (IDENTICO ALLA FOTO E MOBILE-FRIENDLY) ---
st.markdown("""
    <style>
    /* Reset Totale */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}

    /* Immagine Bambino Hero */
    .hero-container {
        width: 100%;
        height: 350px;
        background-image: url('https://unsplash.com');
        background-size: cover;
        background-position: center;
        border-bottom-left-radius: 50px;
        border-bottom-right-radius: 50px;
        margin-bottom: -40px;
    }

    /* Titoli e Testi */
    .titolo-home { color: #0d9488; font-size: 32px; font-weight: 900; padding: 20px; line-height: 1.1; margin-top: 40px; }
    .testo-p { color: #64748b; padding: 0 20px; font-size: 16px; }

    /* CARD BOX COLORATE */
    .card { border-radius: 30px; padding: 25px; margin: 15px 20px; text-align: center; border: none; }
    .box-luna { background-color: #f1f5f9; color: #1e293b; border: 1px solid #cbd5e1; } /* Grigio/Bianco Luna */
    .box-sole { background-color: #fffbeb; color: #92400e; border: 1px solid #fef3c7; } /* Giallo Sole */
    .box-nuvola { background-color: #e0f2fe; color: #075985; border: 1px solid #bae6fd; } /* Azzurro/Grigio Nuvola */
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white; box-shadow: 0 10px 20px rgba(13,148,136,0.3); }

    .prezzo-rosa { color: #ec4899; font-size: 26px; font-weight: 900; margin-top: 10px; }
    .prezzo-bianco { color: white; font-size: 26px; font-weight: 900; margin-top: 10px; }

    /* Pulsanti Call to Action */
    div.stButton > button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 85% !important;
        height: 60px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        margin: 0 auto !important;
        display: block !important;
    }

    /* BARRA INFERIORE FISSA */
    .nav-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background: white;
        border-top: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 10000;
    }
    
    /* Overlay per simulare i click sulla barra */
    .nav-btn { background: none; border: none; color: #0d9488; font-size: 12px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTROLLO NAVIGAZIONE ---
def vai(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- 4. CONTENUTO PAGINE ---

if st.session_state.pagina == "Home":
    st.markdown('<div class="hero-container"></div>', unsafe_allow_html=True)
    st.markdown('<div class="titolo-home">Vestiamo il tuo bambino con amore e qualità.</div>', unsafe_allow_html=True)
    st.markdown('<p class="testo-p">Risparmia tempo e oltre 1.000€ l\'anno con il primo noleggio circolare per neonati.</p>', unsafe_allow_html=True)
    st.write("")
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 40px 20px 0 20px;"><h1>Le nostre Box</h1><p><b>Standard:</b> capi usati in ottimo stato.<br><b>Premium:</b> capi nuovi o seminuovi.</p></div>', unsafe_allow_html=True)
    
    # LUNA
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro, Bianco e Panna</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Prendi LUNA"): st.toast("Luna aggiunta!")
    
    # SOLE
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori vivaci e stampe</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Prendi SOLE"): st.toast("Sole aggiunta!")
    
    # NUVOLA
    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual, Denim e Comfort</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Prendi NUVOLA"): st.toast("Nuvola aggiunta!")
    
    # PREMIUM
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Nuovi/Seminuovi)</p><div class="prezzo-bianco">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("Prendi PREMIUM"): st.toast("Premium aggiunta!")

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding:40px 20px;"><h1>Vetrina Shop</h1><p><b>Nota:</b> Questi capi rimangono a te per sempre!</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card box-luna">🌱<br>Body Bio<br><b>9,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="c1")
    with col2:
        st.markdown('<div class="card box-luna">👖<br>Salopette<br><b>19,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="c2")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:40px 20px;"><h1>Come Funziona</h1></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card box-luna" style="text-align:left;">
    1. <b>Scegli:</b> Seleziona box o capi shop.<br>
    2. <b>Usa:</b> Goditi i capi per 90 giorni.<br>
    3. <b>Rendi:</b> Cambia taglia e restituisci la box.<br><br>
    ⚠️ <b>Regole:</b> Reso gratis con nuova box, altrimenti 7,90€.
    </div>
    """, unsafe_allow_html=True)

# --- 5. BARRA INFERIORE FISSA (SIMULATA CON COLONNE) ---
st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
nav_cols = st.columns(4)
with nav_cols[0]: 
    if st.button("🏠\nHome"): vai("Home")
with nav_cols[1]: 
    if st.button("📦\nBox"): vai("Box")
with nav_cols[2]: 
    if st.button("🛍️\nShop"): vai("Shop")
with nav_cols[3]: 
    if st.button("📖\nInfo"): vai("Info")

# Fix CSS per i bottoni di navigazione
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] {
    position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
    background: white !important; padding: 10px 0 !important; border-top: 1px solid #eee !important; z-index: 99999;
}
[data-testid="stHorizontalBlock"] button {
    background: transparent !important; color: #0d9488 !important; border: none !important;
    box-shadow: none !important; font-size: 12px !important; height: auto !important;
}
</style>
""", unsafe_allow_html=True)
