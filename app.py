import streamlit as st
import os

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. LOGICA DI NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai_a(nome_pagina):
    st.session_state.pagina = nome_pagina

# --- 3. CSS PER APP IDENTICA ---
st.markdown("""
    <style>
    /* Nascondi menu Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #FFFFFF !important; max-width: 450px; margin: 0 auto; }
    
    /* Colori e Font */
    h1, h2, h3, b { color: #0d9488 !important; font-family: 'Helvetica', sans-serif; }
    
    /* Card come da foto */
    .card-loop {
        background: #f9fafb;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .prezzo { color: #ec4899 !important; font-weight: bold; font-size: 1.4em; }

    /* Tasto Rosa Call to Action */
    .stButton>button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3.5em !important;
        border: none !important;
    }

    /* BARRA NAVIGAZIONE FISSA IN BASSO */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        border-top: 2px solid #f0fdfa;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO DELLE PAGINE ---

# --- HOME ---
if st.session_state.pagina == "Home":
    if os.path.exists("logo.png"): st.image("logo.png", width=140)
    st.title("Vestiamo il tuo bambino con amore e qualità.")
    st.write("Risparmia, riusa e rispetta il pianeta con LoopBaby.")
    if st.button("SCEGLI LA TUA BOX"): vai_a("Box")
    
    st.markdown("### Novità Shop")
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="card-loop">👕<br>Body Bio<br><span class="prezzo">9,90€</span></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card-loop">👖<br>Salopette<br><span class="prezzo">19,90€</span></div>', unsafe_allow_html=True)

# --- BOX (3 STANDARD + 1 PREMIUM) ---
elif st.session_state.pagina == "Box":
    st.title("Le nostre Box 📦")
    
    st.subheader("Box Standard")
    stili = [
        {"n": "LUNA", "d": "Colori neutri e delicati", "p": "19,90€"},
        {"n": "SOLE", "d": "Colori vivaci e stampe", "p": "19,90€"},
        {"n": "NUVOLA", "d": "Casual e denim Style", "p": "19,90€"}
    ]
    for s in stili:
        st.markdown(f'<div class="card-loop"><h3>{s["n"]}</h3><p>{s["d"]}</p><span class="prezzo">{s["p"]}</span></div>', unsafe_allow_html=True)
        st.button(f"Scegli {s['n']}", key=s['n'])

    st.subheader("Box Premium")
    st.markdown('<div class="card-loop" style="border: 2px solid #0d9488;"><h3>DIAMANTE 💎</h3><p>Grandi firme selezionate</p><span class="prezzo">29,90€</span></div>', unsafe_allow_html=True)
    st.button("Scegli Premium")

# --- SHOP (VETRINA) ---
elif st.session_state.pagina == "Shop":
    st.title("Vetrina Shop 🛍️")
    st.write("Spedizione gratis sopra i 50€")
    # Qui aggiungeremo i prodotti singoli

# --- CHI SIAMO ---
elif st.session_state.pagina == "ChiSiamo":
    st.title("Chi Siamo ❤️")
    st.write("Siamo genitori che credono nel futuro circolare.")

# --- 5. BARRA DI NAVIGAZIONE FUNZIONANTE ---
# Usiamo i widget di Streamlit dentro una riga fissa
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True) # Spazio per non coprire il contenuto
cols = st.columns(4)
with cols[0]: 
    if st.button("🏠\nHome"): vai_a("Home")
with cols[1]: 
    if st.button("📦\nBox"): vai_a("Box")
with cols[2]: 
    if st.button("🛍️\nShop"): vai_a("Shop")
with cols[3]: 
    if st.button("👋\nChi Siamo"): vai_a("ChiSiamo")

# CSS extra per posizionare i tasti in basso come una barra vera
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 10px;
        z-index: 1000;
        border-top: 1px solid #ddd;
    }
    [data-testid="stHorizontalBlock"] button {
        height: 50px !important;
        font-size: 10px !important;
        background: transparent !important;
        color: #0d9488 !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)
