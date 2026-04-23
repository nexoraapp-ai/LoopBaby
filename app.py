import streamlit as st
import os
import base64

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per fissare la foto bimbo.jpg senza che sparisca
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS "MOODBOARD" (COPIA ESATTA) ---
st.markdown("""
    <style>
    /* Reset Totale */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo Area */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 34px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; margin: 0; }
    .logo-heart { color: #f43f5e; font-size: 38px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home: Testo SX, Bimbo DX */
    .home-grid {
        display: grid;
        grid-template-columns: 1.6fr 1fr;
        gap: 15px;
        align-items: center;
        padding: 0 20px;
        margin-top: 20px;
    }

    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }
    
    /* Lista con icone identica alla foto */
    .item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #475569; margin-bottom: 12px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 30px; object-fit: cover; }

    /* Pulsante Rosa Originale */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin: 25px auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.25) !important;
    }

    /* CARD BOX (Colori specifici) */
    .card { border-radius: 25px; padding: 25px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 26px; font-weight: 900; }

    /* Barra Inferiore Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999;
        padding: 8px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        font-size: 11px !important; font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# Logo Fisso
st.markdown("""
    <div class="header-box">
        <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

# PAGINA HOME
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    
    st.markdown(f"""
        <div class="home-grid">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <div class="item">🏠 Capi di qualità selezionati</div>
                <div class="item">🔄 Cambi quando cresce</div>
                <div class="item">💰 Risparmi più di 1000€ l'anno</div>
                <div class="item">📍 Scegli il locker più vicino a te</div>
                <div class="item">✨ Zero stress per te</div>
            </div>
            <div class="col-right">{img_html}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Scegli la tua Box"): vai("Box")
    
    st.markdown("""
        <div style="padding: 20px;">
            <h3 style="color:#0d9488;">📖 Come Funziona</h3>
            <p style="font-size:14px; color:#64748b;">
                1. <b>Scegli la Box:</b> Lo stile e la taglia che preferisci.<br>
                2. <b>Ritira al Locker:</b> Ricevi la box vicino a te.<br>
                3. <b>Dopo 3 mesi:</b> Decidi se cambiare o tenere.
            </p>
        </div>
    """, unsafe_allow_html=True)

# PAGINA BOX (IDENTICA)
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Le nostre Box 📦</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli LUNA", key="l")
    
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori e Allegria</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli SOLE", key="s")
    
    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual e Jeans</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli NUVOLA", key="n")

    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Nuovi)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p")

# PAGINA SHOP
elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Vetrina Shop 🛍️</h2><p style="color:#64748b;">Questi capi rimangono a te!</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕<br><b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="c1")
    with col2:
        st.markdown('<div class="card">👖<br><b>Salopette</b><br><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="c2")

# PAGINA PROFILO
elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Il tuo Profilo 👤</h2></div>', unsafe_allow_html=True)
    st.text_input("Nome Mamma")
    st.text_input("Email")
    st.date_input("Data di nascita bimbo")
    st.button("SALVA DATI")

# --- 5. NAVIGAZIONE FISSA ---
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
