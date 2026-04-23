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

# --- 2. CSS TOTALE ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 34px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; }
    .logo-heart { color: #f43f5e; font-size: 38px; }
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    .card { border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #eee; }
    .box-luna { background-color: #f8fafc; } 
    .box-sole { background-color: #fffbeb; } 
    .box-nuvola { background-color: #f1f5f9; } 
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; }
    
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .regola-box { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 15px; margin: 10px 20px; border-radius: 10px; }

    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 15px !important; width: 100% !important; height: 55px !important;
        font-weight: 800 !important; margin-top: 10px !important;
    }

    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #eee !important; z-index: 99999;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 11px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER
st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    st.markdown(f'<div style="display:grid; grid-template-columns:1.6fr 1fr; gap:10px; padding:20px;"><div><div style="font-size:26px; font-weight:800;">Ciao Mamma! 👋</div><div style="font-size:15px; color:#334155; margin-bottom:15px;">Il noleggio circolare che cresce con lui.</div><div style="font-size:12px; color:#475569;">👕 Capi selezionati<br>🔄 Cambi quando cresce<br>💰 Risparmi +1000€</div></div><div>{img_html}</div></div>', unsafe_allow_html=True)
    if st.button("SCEGLI LA TUA BOX ➔"): vai("Box")
    
    st.markdown('<div style="padding:20px;"><h3>📖 Come Funziona</h3><p style="font-size:14px; color:#64748b;">1. <b>Scegli la Box:</b> 10 capi per 90 giorni.<br>2. <b>Ritiro al Locker:</b> Comodo e veloce.<br>3. <b>Cambio Taglia:</b> Rendi i vecchi e prendi i nuovi!</p></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Le nostre Box 📦</h2>', unsafe_allow_html=True)
    for b in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace"), ("NUVOLA ☁️", "box-nuvola", "Casual")]:
        st.markdown(f'<div class="card {b[1]}"><h3>{b[0]}</h3><p>{b[2]} (Usato garantito)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        st.button(f"Scegli {b[0]}", key=b[0])
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Grandi Firme (Nuovi)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="prem")

    st.markdown('<div class="regola-box"><b>⚠️ REGOLE IMPORTANTI:</b><br>• Controlla i capi entro 48h.<br>• Reso GRATIS se rinnovi la box.<br>• Penale 5€ per ogni capo mancante.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Shop":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Vetrina 🛍️</h2>', unsafe_allow_html=True)
    st.info("I capi acquistati qui rimangono a te!")
    st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    st.button("Compra Body")

elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Il tuo Profilo 👤</h2>', unsafe_allow_html=True)
    with st.container(border=True):
        st.text_input("Nome Mamma", "Chiara")
        st.text_input("Email", "mamma@esempio.it")
        st.text_input("Cellulare", "333 1234567")
        st.text_input("Nome Bambino", "Luca")
        st.date_input("Data di nascita", date(2025, 1, 1))
        st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.5)
        if st.button("SALVA PROFILO"): st.success("Profilo aggiornato!")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="padding-left:20px; color:#0d9488;">Chi Siamo ❤️</h2>', unsafe_allow_html=True)
    st.markdown('<div style="padding:20px; font-size:15px; color:#475569;">LoopBaby nasce da genitori per i genitori. Crediamo in un futuro dove vestire i nostri figli non sia uno spreco, ma un gesto d\'amore per loro e per il pianeta. 🌍<br><br><b>Contatti:</b><br>📧 info@loopbaby.it<br>💬 WhatsApp: 333 9988776</div>', unsafe_allow_html=True)

# BARRA NAVIGAZIONE
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
