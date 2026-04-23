import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS PROFESSIONALE (IDENTICO ALLA TUA MOODBOARD) ---
st.markdown("""
    <style>
    /* Nascondi header Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo */
    .header-box { padding: 20px 20px 10px 20px; }
    .logo-h { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .heart { color: #f43f5e; font-size: 35px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home (Testo SX, Bimbo DX) */
    .main-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 10px; align-items: center; padding: 0 20px; }
    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 10px; font-weight: 500; }
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

    /* Card Box Colorate */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 10px auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* Barra Bassa Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 11px !important; height: 50px !important;
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
    # FOTO SCELTA PER TE (Link sicuro Unsplash)
    foto_url = "https://unsplash.com"

    st.markdown(f"""
        <div class="main-grid">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <div class="list-item">👕 Capi di qualità selezionati</div>
                <div class="list-item">🔄 Cambi quando cresce</div>
                <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
                <div class="list-item">📍 Scegli il locker più vicino</div>
                <div class="list-item">✨ Zero stress per te</div>
            </div>
            <div class="col-right">
                <img src="{foto_url}" class="baby-img">
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:20px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

# -- ALTRE PAGINE --
elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Le nostre Box 📦</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli LUNA")
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori e Allegria</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli SOLE")
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Nuovi)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM")

elif st.session_state.pagina == "Shop":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">🧸<br>Completo Nascita<br><b class="prezzo-rosa">24,90€</b></div>', unsafe_allow_html=True)
    st.button("Aggiungi al carrello")

elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Il tuo Profilo 👤</h2>', unsafe_allow_html=True)
    st.text_input("Nome")
    st.button("Salva")

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Shop")
with c4: 
    if st.button("👤\nProfilo"): vai("Profilo")
