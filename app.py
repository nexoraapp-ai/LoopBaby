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

# --- 2. CSS TOTALE (ZERO RIQUADRI STREAMLIT, STILE APP) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 34px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; font-size: 38px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* Card Stile App */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; } .box-sole { background-color: #fffbeb; } .box-nuvola { background-color: #f1f5f9; }
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; }
    .prezzo-rosa { color: #ec4899; font-size: 26px; font-weight: 900; }

    /* Riquadri "Come Funziona" */
    .info-step { background: #f0fdfa; border-radius: 15px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #0d9488; }
    
    /* Box Regole Importanti */
    .regole-alert { background-color: #fff1f2; border: 1px solid #fecdd3; border-radius: 20px; padding: 20px; margin: 20px; }

    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 18px !important; width: 85% !important; height: 55px !important;
        font-size: 17px !important; font-weight: 800 !important; margin: 10px auto !important; display: block !important;
    }

    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999; padding: 8px 0 !important;
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
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px;">' if img_data else ""
    st.markdown(f'<div style="display:grid; grid-template-columns:1.6fr 1fr; gap:10px; padding:20px;"><div><div style="font-size:26px; font-weight:800;">Ciao Mamma! 👋</div><div style="font-size:15px; color:#334155; margin-bottom:15px;">Il noleggio circolare che cresce con lui.</div><div style="font-size:12px; color:#475569;">🏠 Capi selezionati<br>🔄 Cambi quando cresce<br>💰 Risparmi +1000€</div></div><div>{img_html}</div></div>', unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Come funziona 📖</h2></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px;">
            <div class="info-step"><b>1. Scegli la Box:</b> Seleziona lo stile e la taglia ideale per il tuo bambino.</div>
            <div class="info-step"><b>2. Ricevi al Locker:</b> Ritira la tua box igienizzata nel punto di ritiro più vicino.</div>
            <div class="info-step"><b>3. Goditi i capi:</b> Usa i vestiti per 90 giorni senza lo stress di doverli acquistare.</div>
            <div class="info-step"><b>4. Rendi o Rinnova:</b> Al cambio taglia, rendi i capi e ricevi subito la nuova box!</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="regole-alert"><b>⚠️ REGOLE IMPORTANTI</b><br><br>• <b>Controllo:</b> Hai 48h per segnalare eventuali difetti.<br>• <b>Reso:</b> Gratis se ordini la box successiva, altrimenti ticket da 7,90€.<br>• <b>Patto del 10:</b> Rendi 10 capi per riceverne 10. Ogni capo mancante ha una penale di 5€.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Le nostre Box 📦</h2></div>', unsafe_allow_html=True)
    for stile, classe, desc in [("LUNA 🌙", "box-luna", "Neutro e Delicato"), ("SOLE ☀️", "box-sole", "Vivace e Allegro"), ("NUVOLA ☁️", "box-nuvola", "Casual e Denim")]:
        st.markdown(f'<div class="card {classe}"><h3>{stile}</h3><p>{desc} (Usato garantito)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        st.button(f"Scegli {stile}", key=stile)
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Capi nuovi o seminuovi)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p_box")

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Vetrina Shop 🛍️</h2><p style="color:#64748b;">Questi capi rimangono a te per sempre!</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕<br><b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh1")
    with col2:
        st.markdown('<div class="card">👖<br><b>Salopette</b><br><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh2")

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Il tuo Profilo 👤</h2></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.text_input("Nome Mamma")
        st.text_input("Email")
        st.text_input("Cellulare")
        st.text_input("Nome Bambino")
        st.date_input("Data di nascita", date(2025, 1, 1))
        st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.5)
        st.button("SALVA DATI PROFILO")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="padding: 20px;"><h2 style="color:#0d9488;">Chi Siamo ❤️</h2></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; color:#475569; font-size:15px; line-height:1.6;">
            <b>Siamo genitori, proprio come te.</b><br>
            Abbiamo creato LoopBaby per risolvere il problema dei vestiti che durano troppo poco e costano troppo. Crediamo in un futuro circolare dove la qualità sia accessibile a tutti, senza sprechi per il pianeta.<br><br>
            📍 <b>Sede:</b> Italia<br>
            📧 <b>Email:</b> info@loopbaby.it<br>
            💬 <b>WhatsApp:</b> 333 1234567
        </div>
    """, unsafe_allow_html=True)

# --- 4. NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    if st.button("🏠\nHome"): vai("Home")
with c2: 
    if st.button("📖\nInfo"): vai("Info")
with c3: 
    if st.button("📦\nBox"): vai("Box")
with c4: 
    if st.button("🛍️\nShop"): vai("Shop")
with c5: 
    if st.button("👤\nProfilo"): vai("Profilo")
with c6: 
    if st.button("👋\nChi"): vai("ChiSiamo")
