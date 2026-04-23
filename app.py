import streamlit as st
import os

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. CSS PER BARRA IN BASSO E COLORI MOODBOARD ---
st.markdown("""
    <style>
    /* Sfondo e Font */
    .stApp { background-color: #FFFFFF !important; max-width: 450px; margin: 0 auto; padding-bottom: 80px; }
    
    /* Colori Titoli e Testi */
    h1, h2, h3, b { color: #0d9488 !important; }
    p { color: #64748b !important; }

    /* Card Box e Prodotti */
    .product-card {
        background: #f8fafc;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .price-tag { color: #ec4899 !important; font-weight: 900; font-size: 1.3em; margin: 10px 0; }

    /* Pulsante Rosa Identico alla foto */
    .stButton>button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* BARRA DI NAVIGAZIONE IN BASSO */
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 1000;
        text-align: center;
    }
    .footer-item { color: #0d9488; font-size: 0.7em; text-decoration: none; font-weight: bold; }
    .footer-icon { font-size: 1.8em; display: block; }
    </style>
    
    <!-- HTML Barra Inferiore -->
    <div class="fixed-footer">
        <div class="footer-item"> <span class="footer-icon">🏠</span>Home </div>
        <div class="footer-item"> <span class="footer-icon">📦</span>Box </div>
        <div class="footer-item"> <span class="footer-icon">🛍️</span>Shop </div>
        <div class="footer-item"> <span class="footer-icon">👤</span>Profilo </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOGICA PAGINE ---
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
def vai(nome): st.session_state.pagina = nome

# --- 4. CONTENUTO ---

# PAGINA HOME
if st.session_state.pagina == "Home":
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.title("Vestiamo il tuo bambino con amore. ❤️")
    st.write("Qualità, risparmio e sostenibilità in un unico Loop.")
    
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")
    
    st.markdown("---")
    st.subheader("Novità in Vetrina")
    # Anteprima rapida shop
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="product-card">🌱<br>Body Bio<br><span class="price-tag">9,90€</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="product-card">👖<br>Salopette<br><span class="price-tag">19,90€</span></div>', unsafe_allow_html=True)

# PAGINA BOX (3 STANDARD + 1 PREMIUM)
elif st.session_state.pagina == "Box":
    st.title("Scegli il tuo Stile 📦")
    st.write("Ogni Box contiene 10 capi per 90 giorni.")

    # Loop per le 3 Box Standard
    st.subheader("Box Standard - 19,90€")
    stili = [
        {"nome": "LUNA 🌙", "desc": "Colori neutri, bianco, panna e grigio."},
        {"nome": "SOLE ☀️", "desc": "Colori vivaci, fantasie e allegria."},
        {"nome": "NUVOLA ☁️", "desc": "Casual, jeans e comodità quotidiana."}
    ]
    
    for stile in stili:
        with st.container():
            st.markdown(f"""
            <div class="product-card">
                <h3>{stile['nome']}</h3>
                <p>{stile['desc']}</p>
                <div class="price-tag">19,90 €</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"SCEGLI {stile['nome']}", key=stile['nome'])

    st.divider()
    
    # Box Premium
    st.subheader("Box Premium - 29,90€")
    st.markdown("""
    <div class="product-card" style="border: 2px solid #0d9488;">
        <h3>DIAMANTE 💎</h3>
        <p>I migliori brand e tessuti pregiati.</p>
        <div class="price-tag">29,90 €</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("SCEGLI PREMIUM", key="premium")

# --- FINE CODICE ---
