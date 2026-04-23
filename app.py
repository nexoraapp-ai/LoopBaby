import streamlit as st
import os
import base64

# --- 1. CONFIGURAZIONE LAYOUT ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per caricare la foto in modo che non sparisca mai
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_base64 = get_base64("bimbo.jpg")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
def vai(nome): 
    st.session_state.pagina = nome
    st.rerun()

# --- 3. CSS PER DIMENSIONI FISSE (IDENTICO ALLA FOTO) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Container Home a due colonne bloccate */
    .home-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 15px;
        align-items: center;
        padding: 0 20px;
        margin-top: 20px;
    }

    .ciao { font-size: 26px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-img { width: 100%; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }

    /* Pulsante Rosa Identico */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        width: 90% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin: 20px auto !important;
        display: block !important;
    }

    /* Barra Bassa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# Logo Fisso
st.markdown('<div style="padding: 20px 20px 0 20px;"><h1 style="font-size:32px; font-weight:800; color:#1e293b;">💗 LoopBaby</h1><p style="color:#64748b; margin-top:-10px;">Vestiamo il tuo bambino, rispettiamo il futuro.</p></div>', unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    # Layout con Immagine e Testo insieme per non farli sparire
    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="baby-img">' if img_base64 else '<div style="width:100%; height:150px; background:#eee; border-radius:25px;"></div>'
    
    st.markdown(f"""
        <div class="home-grid">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi.</div>
                <div class="list-item">👕 Capi selezionati</div>
                <div class="list-item">🔄 Cambi quando cresce</div>
                <div class="list-item">💰 Risparmi +1000€</div>
                <div class="list-item">📍 Locker vicino a te</div>
            </div>
            <div class="col-right">
                {img_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")

elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="padding:20px; color:#0d9488;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
    # Card Box qui...

# --- 5. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Home")
with c4: 
    if st.button("👤\nProfilo"): vai("Home")
