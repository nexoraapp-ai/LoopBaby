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
    /* Nascondi sporco Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    /* Font */
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header */
    .header-box { padding: 20px 20px 10px 20px; }
    .logo-title { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; font-size: 35px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* LAYOUT A DUE COLONNE REALI */
    .main-row { display: flex; align-items: flex-start; padding: 0 20px; gap: 10px; margin-top: 20px; }
    .col-left { flex: 1.5; }
    .col-right { flex: 1; text-align: right; }

    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }

    /* Immagine Bimbo */
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

    /* PULSANTE ROSA LARGO (IDENTICO) */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* CARD PER LE BOX COLORATE */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

    /* Barra navigazione fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999; padding-top: 5px;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 11px !important; height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. PAGINA HOME ---
if st.session_state.pagina == "Home":
    # Logo
    st.markdown("""
        <div class="header-box">
            <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
            <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
        </div>
    """, unsafe_allow_html=True)

    # Verifica se l'immagine esiste, altrimenti usa un link segnaposto
    img_src = "bimbo.jpg" if os.path.exists("bimbo.jpg") else "https://unsplash.com"

    # Layout Corpo
    st.markdown(f"""
        <div class="main-row">
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
                <img src="{img_src}" class="baby-img">
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:20px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

# --- 5. PAGINA BOX ---
elif st.session_state.pagina == "Box":
    st.markdown('<h1 style="padding-left:20px; color:#0d9488;">Le nostre Box 📦</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli LUNA"): st.toast("Luna scelta")

    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori ed energia</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli SOLE"): st.toast("Sole scelta")

    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual e Jeans</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli NUVOLA"): st.toast("Nuvola scelta")

    st.markdown('<div class="card box-premium"><h3 style="color:white;">PREMIUM 💎</h3><p style="color:white;">Grandi Firme Nuove</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    if st.button("Scegli PREMIUM"): st.toast("Premium scelta")

# --- 6. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Home") # Da implementare
with c4: 
    if st.button("👤\nProfilo"): vai("Home") # Da implementare
