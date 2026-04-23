import streamlit as st
import os

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS TOTALE (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    /* Nascondi elementi Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font e Titoli */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    .logo-h { font-size: 32px; font-weight: 800; color: #1e293b; margin: 0; padding-left: 20px; }
    .heart { color: #f43f5e; }
    .slogan { color: #64748b; padding-left: 25px; font-size: 14px; margin-top: -5px; }

    /* Layout Home (Testo + Bimbo) */
    .home-flex { display: flex; align-items: center; padding: 20px; gap: 15px; }
    .col-testo { flex: 1.5; }
    .col-bimbo { flex: 1; }
    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-top: 10px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-top: 8px; }
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

    /* CARD DELLE BOX COLORATE */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .prezzo-bianco { color: white !important; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa FULL WIDTH */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 10px auto !important;
        display: block !important;
    }

    /* BARRA NAVIGAZIONE FISSA */
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

# --- 4. CONTENUTO DELLE PAGINE ---

# -- PAGINA HOME --
if st.session_state.pagina == "Home":
    st.markdown('<h1 class="logo-h"><span class="heart">💗</span> LoopBaby</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</p>', unsafe_allow_html=True)
    
    # Se esiste bimbo.jpg lo carica, altrimenti mette il segnaposto
    img_path = "bimbo.jpg"
    img_html = f'<img src="{img_path}" class="baby-img">' if os.path.exists(img_path) else '<div style="width:100%; height:150px; background:#f1f5f9; border-radius:25px; display:flex; align-items:center; justify-content:center; color:#94a3b8; font-size:10px; text-align:center; border:2px dashed #ccc;">Metti<br>bimbo.jpg<br>qui</div>'

    st.markdown(f"""
    <div class="home-flex">
        <div class="col-testo">
            <div class="ciao">Ciao Mamma! 👋</div>
            <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
            <div class="list-item">👕 Capi di qualità selezionati</div>
            <div class="list-item">🔄 Cambi quando cresce</div>
            <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
            <div class="list-item">📍 Scegli il locker più vicino</div>
            <div class="list-item">✨ Zero stress per te</div>
        </div>
        <div class="col-bimbo">
            {img_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:20px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

# -- PAGINA BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<h1 class="logo-h"><span class="heart">💗</span> LoopBaby</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Le nostre Box</h2>', unsafe_allow_html=True)
    st.markdown('<p style="padding-left:20px; font-size:14px; color:#64748b;">Standard: Usato garantito | Premium: Nuovi</p>', unsafe_allow_html=True)

    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Seleziona LUNA"): st.toast("Luna scelta!")

    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori e Allegria</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Seleziona SOLE"): st.toast("Sole scelta!")

    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual e Jeans</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Seleziona NUVOLA"): st.toast("Nuvola scelta!")

    st.markdown('<div class="card box-premium"><h3 style="color:white;">PREMIUM 💎</h3><p style="color:white;">Grandi Firme Nuove</p><div class="prezzo-bianco">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("Seleziona PREMIUM"): st.toast("Premium scelta!")

# -- PAGINA SHOP --
elif st.session_state.pagina == "Shop":
    st.markdown('<h1 class="logo-h">🛍️ Vetrina Shop</h1>', unsafe_allow_html=True)
    st.info("I capi in vetrina rimangono a te!")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕<br>Body Bio<br><b class="prezzo-rosa">9,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="s1")
    with col2:
        st.markdown('<div class="card">👖<br>Salopette<br><b class="prezzo-rosa">19,90€</b></div>', unsafe_allow_html=True)
        st.button("Compra", key="s2")

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
    if st.button("👤\nProfilo"): vai("Home")
