import streamlit as st

# --- 1. CONFIGURAZIONE (Elimina i margini di Streamlit) ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome):
    st.session_state.pagina = nome
    st.rerun()

# --- 2. CSS PROFESSIONALE (IDENTICO AL TUO DESIGN) ---
st.markdown("""
    <style>
    /* Nascondi header e menu Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo e Slogan */
    .header-box { padding: 10px 20px; text-align: left; }
    .logo-title { font-size: 32px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* Layout Home: Testo a Sinistra, Bimbo a Destra */
    .home-flex { display: flex; align-items: center; padding: 0 20px; gap: 15px; margin-top: 10px; }
    .col-left { flex: 1.6; }
    .col-right { flex: 1; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin: 0; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 8px; }
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

    /* CARD BOX COLORATE */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; border-color: #cbd5e1; } 
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; } 
    .box-nuvola { background-color: #f1f5f9; border-color: #e2e8f0; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa GIGANTE */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 18px !important;
        border: none !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
    }

    /* BARRA INFERIORE FISSA */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999; padding: 5px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 11px !important; height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA PAGINE ---

if st.session_state.pagina == "Home":
    st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="home-flex">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <div class="list-item">👕 Capi di qualità selezionati</div>
                <div class="list-item">🔄 Cambi quando cresce</div>
                <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
                <div class="list-item">📍 Scegli il locker più vicino</div>
            </div>
            <div class="col-right">
                <img src="https://unsplash.com" class="baby-img">
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

elif st.session_state.pagina == "Box":
    st.markdown('<h1 style="color:#0d9488; padding:20px;">Le nostre Box 📦</h1>', unsafe_allow_html=True)
    
    # 3 Standard
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro e Delicato (Usato)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli LUNA", key="l")
    
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Colori e Allegria (Usato)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli SOLE", key="s")
    
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Nuovi/Seminuovi)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p")

elif st.session_state.pagina == "Shop":
    st.markdown('<h1 style="color:#0d9488; padding:20px;">Vetrina 🛍️</h1>', unsafe_allow_html=True)
    st.info("I capi acquistati qui rimangono a te per sempre!")
    
    prodotti = [("Body Bio", "9,90€", "🌱"), ("Salopette", "19,90€", "👖")]
    for nome, prezzo, icona in prodotti:
        st.markdown(f'<div class="card">{icona}<br><b>{nome}</b><br><span class="prezzo-rosa">{prezzo}</span></div>', unsafe_allow_html=True)
        st.button(f"Compra {nome}")

elif st.session_state.pagina == "Profilo":
    st.markdown('<h1 style="color:#0d9488; padding:20px;">Il tuo Profilo 👤</h1>', unsafe_allow_html=True)
    st.text_input("Nome Mamma")
    st.text_input("Cellulare")
    st.button("SALVA PROFILO")

# --- 4. BARRA DI NAVIGAZIONE FISSA ---
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
