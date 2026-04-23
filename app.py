import streamlit as st
import os
import base64

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per fissare la foto "bimbo.jpg" ed evitare che sparisca o si sposti
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

# --- 3. CSS "ZERO-FRAME" (IDENTICO ALLA TUA FOTO) ---
st.markdown("""
    <style>
    /* Rimuove tutto lo stile standard di Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}

    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header Logo */
    .header-box { padding: 30px 20px 10px 20px; text-align: left; }
    .logo-h { font-size: 34px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; margin: 0; }
    .heart { color: #f43f5e; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home: Testo SX, Bimbo DX (senza riquadri) */
    .home-layout {
        display: grid;
        grid-template-columns: 1.6fr 1fr;
        gap: 10px;
        align-items: center;
        padding: 20px;
        margin-top: 10px;
    }

    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }
    
    /* Lista icone come da tua foto */
    .item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #475569; margin-bottom: 12px; font-weight: 500; }
    
    /* Immagine Bimbo "Nuda" (senza cornici pesanti) */
    .baby-img { width: 100%; border-radius: 30px; object-fit: cover; }

    /* Pulsante Rosa Identico */
    div.stButton > button {
        background-color: #f43f5e !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        width: 85% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin: 20px auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.2) !important;
        text-transform: none !important;
    }

    /* Barra Navigazione Bassa */
    .nav-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 99999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CONTENUTO ---

# Logo Fisso in alto
st.markdown("""
    <div class="header-box">
        <div class="logo-h"><span class="heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    # Layout con Immagine e Testo Affiancati
    img_html = f'<img src="data:image/jpeg;base64,{img_base64}" class="baby-img">' if img_base64 else '<div style="width:100%; height:150px; background:#f8fafc; border-radius:30px;"></div>'
    
    st.markdown(f"""
        <div class="home-layout">
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

    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:12px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Scegli la tua Box 📦</h2></div>', unsafe_allow_html=True)
    # Seguiranno Luna, Sole, Nuvola...

# --- 5. BARRA NAVIGAZIONE FISSA (LOGICA) ---
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
cols = st.columns(4)
with cols[0]: 
    if st.button("🏠\nHome", key="h"): vai("Home")
with cols[1]: 
    if st.button("📦\nBox", key="b"): vai("Box")
with cols[2]: 
    if st.button("🛍️\nShop", key="s"): vai("Home")
with cols[3]: 
    if st.button("👤\nProfilo", key="p"): vai("Home")

# Style finale per i bottoni della barra
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] {
    position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
    background: white !important; border-top: 1px solid #eee !important; z-index: 99999;
}
[data-testid="stHorizontalBlock"] button {
    background: transparent !important; color: #0d9488 !important; border: none !important;
    box-shadow: none !important; font-size: 11px !important; height: auto !important;
}
</style>
""", unsafe_allow_html=True)
