import streamlit as st
import os
import base64
from datetime import date

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")

if "pagina" not in st.session_state: st.session_state.pagina = "Home"
def vai(nome): 
    st.session_state.pagina = nome
    st.rerun()

# --- 2. CSS IDENTICO ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 30px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .logo-heart { color: #f43f5e; font-size: 32px; }
    .slogan { font-size: 13px; color: #64748b; margin-top: -5px; }

    /* Sezioni Chi Siamo */
    .chi-siamo-title { font-size: 24px; font-weight: 800; color: #1e293b; text-align: center; margin-top: 20px; }
    .chi-siamo-heart { color: #f43f5e; font-size: 26px; }
    .testo-emozionale { padding: 20px; font-size: 14px; color: #475569; line-height: 1.6; text-align: center; }
    .obiettivo-box { background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 0 20px; text-align: center; border: 1px solid #fecdd3; }
    
    /* Contatti */
    .contatti-titolo { font-size: 20px; font-weight: 800; color: #1e293b; text-align: center; margin-top: 30px; }
    .contatto-item { display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 14px; color: #475569; margin-bottom: 10px; }

    /* Barra Navigazione */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999; padding: 5px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER FISSO
st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    st.markdown(f'<div style="display:grid; grid-template-columns:1.6fr 1fr; gap:10px; padding:20px;"><div><div style="font-size:26px; font-weight:800;">Ciao Mamma! 👋</div><div style="font-size:15px; color:#334155; margin-bottom:15px;">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div><div style="font-size:12px; color:#475569;">👶 Capi selezionati<br>🔄 Cambi quando cresce<br>💰 Risparmi +1000€</div></div><div>{img_html}</div></div>', unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div class="chi-siamo-title">Chi siamo? <span class="chi-siamo-heart">❤️</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-weight:800; font-size:18px; color:#1e293b; margin-top:10px;">Siamo genitori, come te.</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="testo-emozionale">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che non basta mai.<br><br>
            Per questo abbiamo creato LoopBaby: per semplificarti la vita, farti risparmiare e ridurre gli sprechi, senza rinunciare alla qualità che merita il tuo bambino.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="obiettivo-box">
            <b style="color:#f43f5e;">Il nostro obiettivo?</b><br>
            Offrirti vestiti di qualità, farti risparmiare di più di 1000€ l'anno e lasciare un mondo migliore ai nostri figli.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="contatti-titolo">Contatti</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-size:13px; color:#64748b; margin-bottom:15px;">Siamo sempre qui per te!</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="contatto-item">💬 WhatsApp: 333 1234567</div>
        <div class="contatto-item">📧 Email: hello@loopbaby.it</div>
        <div class="contatto-item">🕒 Orari: Lun - Ven 9:00 - 18:00</div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding:20px;"><h2 style="color:#0d9488;">Le nostre Box 📦</h2></div>', unsafe_allow_html=True)
    # Codice Box Luna, Sole, Nuvola...

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding:20px;"><h2 style="color:#0d9488;">Vetrina 🛍️</h2></div>', unsafe_allow_html=True)
    # Codice Vetrina...

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding:20px;"><h2 style="color:#0d9488;">Il tuo Profilo 👤</h2></div>', unsafe_allow_html=True)
    # Codice Profilo...

# --- 4. NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📦\nBox"): vai("Box")
with c3: 
    if st.button("🛍️\nShop"): vai("Shop")
with c4: 
    if st.button("👤\nProfilo"): vai("Profilo")
with c5: 
    if st.button("👋\nChi"): vai("ChiSiamo")
