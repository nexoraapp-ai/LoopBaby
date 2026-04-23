import streamlit as st
import os
import base64
from datetime import date

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per fissare la foto bimbo.jpg
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_base64("bimbo.jpg")

if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

# --- 2. CSS "IDENTICO ALLA FOTO" ---
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

    /* Layout Home */
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 10px; align-items: center; padding: 0 20px; margin-top: 10px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }
    .item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 25px; }

    /* Pulsante Rosa */
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 15px !important; width: 85% !important; height: 50px !important;
        font-size: 16px !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important;
    }

    /* Chi Siamo */
    .chi-siamo-title { font-size: 24px; font-weight: 800; color: #1e293b; text-align: center; margin-top: 20px; }
    .testo-emozionale { padding: 20px; font-size: 14px; color: #475569; line-height: 1.6; text-align: center; }
    .obiettivo-box { background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 0 20px; text-align: center; border: 1px solid #fecdd3; }
    .contatto-item { display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 14px; color: #475569; margin-bottom: 10px; }

    /* Barra Navigazione Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999; padding: 5px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER FISSO
st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    st.markdown(f'<div class="home-grid"><div class="col-left"><div class="ciao">Ciao Mamma! 👋</div><div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div><div class="item">👶 Capi di qualità selezionati</div><div class="item">🔄 Cambi quando cresce</div><div class="item">💰 Risparmi più di 1000€ l’anno</div><div class="item">🏠 Scegli il locker più vicino a te</div><div class="item">🧘 Zero stress per te</div></div><div class="col-right">{img_html}</div></div>', unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div class="chi-siamo-title">Chi siamo? <span style="color:#f43f5e;">❤️</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-weight:800; font-size:18px; color:#1e293b; margin-top:10px;">Siamo genitori, come te.</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="testo-emozionale">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che non basta mai.<br><br>
            Per questo abbiamo creato LoopBaby: per semplificarti la vita, farti risparmiare e ridurre gli sprechi, senza rinunciare alla qualità che merita il tuo bambino.
        </div>
        <div class="obiettivo-box">
            <b style="color:#f43f5e;">Il nostro obiettivo?</b><br>
            Offrirti vestiti di qualità, farti risparmiare di più di 1000€ l'anno e lasciare un mondo migliore ai nostri figli.
        </div>
        <div style="text-align:center; font-weight:800; font-size:20px; color:#1e293b; margin-top:30px;">Contatti</div>
        <div style="text-align:center; font-size:13px; color:#64748b; margin-bottom:15px;">Siamo sempre qui per te!</div>
        <div class="contatto-item">💬 WhatsApp: 333 1234567</div>
        <div class="contatto-item">📧 Email: hello@loopbaby.it</div>
        <div class="contatto-item">🕒 Orari: Lun - Ven 9:00 - 18:00</div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:0 20px; font-size:14px; color:#475569; line-height:1.8;">1. <b>Scegli la Box:</b> Stile e qualità.<br>2. <b>Ritira al locker:</b> Vicino a te.<br>3. <b>Controlla entro 48h:</b> Segnalaci problemi.<br>4. <b>Dopo 3 mesi scegli:</b> Cambia o rendi.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px;">Scegli la tua Box</div>', unsafe_allow_html=True)
    for stile in ["LUNA 🌙", "SOLE ☀️", "NUVOLA ☁️"]:
        st.markdown(f'<div style="background:#f8fafc; border-radius:20px; padding:20px; margin:10px; border:1px solid #eee; text-align:center;"><h3>{stile}</h3><p>19,90€</p></div>', unsafe_allow_html=True)
        st.button(f"Scegli {stile}", key=stile)

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px;">Vetrina</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:#f8fafc; border-radius:20px; padding:20px; margin:10px; border:1px solid #eee; text-align:center;">👕 Body Bio<br><b>9,90€</b></div>', unsafe_allow_html=True)
    st.button("Compra ora", key="buy")

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px;">Il tuo profilo</div>', unsafe_allow_html=True)
    st.text_input("Nome Mamma", "Giulia Rossi")
    st.text_input("Cellulare", "333 1234567")
    st.button("Salva Profilo")

# --- 4. BARRA NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📖\nInfo"): vai("Info")
with c3: 
    if st.button("📦\nBox"): vai("Box")
with c4: 
    if st.button("🛍️\nShop"): vai("Shop")
with c5: 
    if st.button("👋\nChi Siamo"): vai("ChiSiamo")
