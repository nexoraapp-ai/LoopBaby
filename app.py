import streamlit as st
import os
import base64

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per convertire l'immagine in Base64 (evita che la foto sparisca)
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

img_data = get_base64("bimbo.jpg")

# --- 2. LOGICA NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def vai(nome_pag):
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 3. CSS "ZERO-FRAME" (COPIA ESATTA DEL DESIGN) ---
st.markdown("""
    <style>
    /* Pulizia totale interfaccia Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}

    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Logo e Intestazione */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 34px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; margin: 0; }
    .logo-heart { color: #f43f5e; font-size: 38px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home: Testo SX, Bimbo DX (Grid bloccata) */
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
    
    /* Lista con icone del tuo design */
    .item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #475569; margin-bottom: 12px; font-weight: 500; }
    
    /* Immagine Bimbo orsetto pulita */
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

    /* Barra Inferiore Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999;
        padding: 8px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important;
        box-shadow: none !important; font-size: 11px !important; height: auto !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# Logo LoopBaby sempre visibile
st.markdown("""
    <div class="header-box">
        <div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    # Preparazione Immagine
    if img_data:
        img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">'
    else:
        img_html = '<div style="width:100%; height:150px; background:#f8fafc; border-radius:30px; display:flex; align-items:center; justify-content:center; font-size:10px; color:#94a3b8; border:1px dashed #ccc; text-align:center;">Metti bimbo.jpg<br>nella cartella</div>'

    # Schermata Home Identica alla moodboard
    st.markdown(f"""
        <div class="home-grid">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <div class="item">👕 Capi di qualità selezionati</div>
                <div class="item">🔄 Cambi quando cresce</div>
                <div class="item">💰 Risparmi più di 1000€ l'anno</div>
                <div class="item">📍 Scegli il locker più vicino</div>
                <div class="item">✨ Zero stress per te</div>
            </div>
            <div class="col-right">
                {img_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Scegli la tua Box"):
        vai("Box")
    
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Le nostre Box 📦</h2></div>', unsafe_allow_html=True)
    # Seguiranno qui Luna, Sole, Nuvola e Premium con i colori che abbiamo stabilito

# --- 5. NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 90px;"></div>', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]: 
    if st.button("🏠\nHome"): vai("Home")
with cols[1]: 
    if st.button("📦\nBox"): vai("Box")
with cols[2]: 
    if st.button("🛍️\nShop"): vai("Home")
with cols[3]: 
    if st.button("👤\nProfilo"): vai("Home")
