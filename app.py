import streamlit as st

# --- 1. CONFIGURAZIONE HARDCORE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. LOGICA DI NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def cambia_pagina(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- 3. CSS TOTALE (IDENTICO ALLA FOTO) ---
st.markdown(f"""
    <style>
    /* Nascondi elementi Streamlit */
    #MainMenu, header, footer {{ visibility: hidden !important; }}
    .block-container {{ padding-top: 1rem !important; padding-bottom: 10rem !important; }}
    
    /* Background App */
    .stApp {{ background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto; }}

    /* Colori e Testi */
    h1, h2, h3, .verde {{ color: #0d9488 !important; font-family: 'Inter', sans-serif; font-weight: 800; }}
    p {{ color: #475569 !important; font-size: 15px; line-height: 1.4; }}

    /* Card Prodotti/Box */
    .card-loop {{
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }}
    .prezzo-rosa {{ 
        color: #ec4899 !important; 
        font-size: 24px !important; 
        font-weight: 900 !important; 
        margin: 10px 0; 
    }}

    /* Pulsante Rosa Call to Action */
    div.stButton > button {{
        background-color: #ec4899 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        transition: 0.3s;
    }}
    
    /* Barra di Navigazione Inferiore */
    .nav-fisso {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #E2E8F0;
        padding: 10px 0;
        z-index: 9999;
        display: flex;
        justify-content: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO PAGINE ---

# -- PAGINA: HOME --
if st.session_state.pagina == "Home":
    st.image("logo.png", width=150)
    st.markdown("<h1>Vestiamo il tuo bambino con amore e qualità.</h1>", unsafe_allow_html=True)
    st.write("Il primo noleggio circolare che cresce con il tuo bebè. Risparmia spazio, tempo e oltre 1.000€ l'anno.")
    
    if st.button("SCEGLI LA TUA BOX ➔"):
        cambia_pagina("Box")

    st.markdown("<br><h3 class='verde'>I preferiti dalle mamme</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card-loop">👕<br><b>Body Bio</b><br><div class="prezzo-rosa">9,90€</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card-loop">👖<br><b>Salopette</b><br><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)

# -- PAGINA: BOX --
elif st.session_state.pagina == "Box":
    st.markdown("<h1 class='verde'>Le nostre Box 📦</h1>", unsafe_allow_html=True)
    st.write("Scegli lo stile della tua Box da 10 capi. Valida per 90 giorni.")

    # BOX STANDARD: LUNA
    st.markdown('<div class="card-loop"><h3>LUNA 🌙</h3><p>Stile neutro: bianco, panna e grigio melange.</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI LUNA", key="luna"): st.success("Luna selezionata!")

    # BOX STANDARD: SOLE
    st.markdown('<div class="card-loop"><h3>SOLE ☀️</h3><p>Colori vivaci, giallo, azzurro e fantasie allegre.</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI SOLE", key="sole"): st.success("Sole selezionata!")

    # BOX STANDARD: NUVOLA
    st.markdown('<div class="card-loop"><h3>NUVOLA ☁️</h3><p>Casual Style: denim comodo e cotone sportivo.</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI NUVOLA", key="nuvola"): st.success("Nuvola selezionata!")

    # BOX PREMIUM
    st.markdown('<div class="card-loop" style="border: 2px solid #0d9488;"><h3>DIAMANTE 💎</h3><p>Selezione esclusiva dei migliori brand Luxury.</p><div class="prezzo-rosa">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI PREMIUM", key="diamante"): st.success("Premium selezionata!")

# -- PAGINA: SHOP --
elif st.session_state.pagina == "Shop":
    st.markdown("<h1 class='verde'>Vetrina Shop 🛍️</h1>", unsafe_allow_html=True)
    st.write("Capi singoli da acquistare e tenere per sempre.")
    st.info("Spedizione GRATUITA per ordini superiori a 50€")
    
    st.markdown('<div class="card-loop">🧸<br><b>Set Regalo Nascita</b><br><div class="prezzo-rosa">34,90€</div></div>', unsafe_allow_html=True)
    st.button("AGGIUNGI AL CARRELLO")

# -- PAGINA: CHI SIAMO --
elif st.session_state.pagina == "ChiSiamo":
    st.markdown("<h1 class='verde'>Chi Siamo ❤️</h1>", unsafe_allow_html=True)
    st.write("Siamo un team di genitori che crede nella moda circolare per un futuro più sostenibile.")
    st.markdown("""
    <div class="card-loop">
        <b>Contatti SOS</b><br>
        Email: hello@loopbaby.it<br>
        WhatsApp: 333 4455667
    </div>
    """, unsafe_allow_html=True)

# --- 5. BARRA DI NAVIGAZIONE FISSA (LOGICA BOTTONI) ---
# Creiamo una riga fissa in basso con i bottoni Streamlit
st.markdown('<div class="nav-fisso">', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]:
    if st.button("🏠\nHome", key="nav_h"): cambia_pagina("Home")
with cols[1]:
    if st.button("📦\nBox", key="nav_b"): cambia_pagina("Box")
with cols[2]:
    if st.button("🛍️\nShop", key="nav_s"): cambia_pagina("Shop")
with cols[3]:
    if st.button("👋\nChi Siamo", key="nav_c"): cambia_pagina("ChiSiamo")
st.markdown('</div>', unsafe_allow_html=True)

# --- FIX ESTETICO BARRA NAVIGAZIONE ---
st.markdown("""
    <style>
    /* Rendi i bottoni della nav bar piccoli e senza sfondo */
    [data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white !important;
        padding: 5px !important;
        border-top: 1px solid #E2E8F0;
        z-index: 99999;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important;
        color: #0d9488 !important;
        border: none !important;
        font-size: 12px !important;
        height: 50px !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)
