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

if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
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
    .slogan { font-size: 14px; color: #64748b; margin-top: -5px; }

    /* Card grafiche */
    .card { border-radius: 20px; padding: 15px; margin: 10px 20px; border: 1px solid #eee; text-align: center; }
    .prezzo-rosa { color: #ec4899; font-size: 22px; font-weight: 900; }
    .regola-10-box { background-color: #f0fdfa; border: 1px solid #5eead4; border-radius: 15px; padding: 15px; margin: 10px 20px; color: #0d9488; }

    /* Pulsante Rosa */
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 15px !important; width: 85% !important; height: 50px !important;
        font-size: 16px !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important;
    }

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

# HEADER COSTANTE
st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    st.markdown(f'<div style="display:grid; grid-template-columns:1.6fr 1fr; gap:10px; padding:20px;"><div><div style="font-size:26px; font-weight:800;">Ciao Mamma! 👋</div><div style="font-size:15px; color:#334155; margin-bottom:15px;">Il noleggio circolare che cresce con il tuo bambino.</div><div style="font-size:12px; color:#475569;">🏠 Capi selezionati<br>🔄 Cambi quando cresce<br>💰 Risparmi +1000€</div></div><div>{img_html}</div></div>', unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding: 20px; font-weight:800; font-size:24px; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="padding: 0 20px;">
            <div style="margin-bottom:15px;"><b>1. LoopBaby:</b> Ricevi 10 capi selezionati. Qualità <b>Standard</b> (usato in ottimo stato) o <b>Premium</b> (grandi firme, nuovi o seminuovi).</div>
            <div style="margin-bottom:15px;"><b>2. Scegli e ricevi:</b> Scegli lo stile e ricevi la Box nel locker più vicino a te.</div>
            <div style="margin-bottom:15px;"><b>3. Usa senza stress:</b> Goditi i capi per 90 giorni. Se si macchiano, non preoccuparti!</div>
            <div style="margin-bottom:15px;"><b>4. Regola del 10:</b> Il patto è semplice. Prendi 10 capi, rendi 10 capi.</div>
            <div style="margin-bottom:15px;"><b>5. Cambia taglia:</b> Rendi la vecchia box e ricevi la nuova della taglia corretta.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="regola-10-box"><b>💡 LA REGOLA DEL 10:</b><br>Per mantenere il cerchio perfetto, chiediamo di rendere lo stesso numero di capi ricevuti (10). Se un capo viene smarrito o distrutto, la penale è di soli 5€.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding:20px; text-align:center; font-weight:800; font-size:22px;">Le nostre Box</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>STANDARD 🌙</h3><p>Usato selezionato garantito</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli Standard", key="b1")
    st.markdown('<div class="card" style="background:#0d9488; color:white;"><h3>PREMIUM 💎</h3><p>Grandi firme - Nuovi/Seminuovi</p><div style="color:white; font-size:22px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli Premium", key="b2")

elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding:20px; text-align:center; font-weight:800; font-size:22px;">Vetrina Shop</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; color:#64748b; font-size:14px; margin-bottom:10px;">Ciò che acquisti in vetrina <b>rimane a te</b> per sempre.</div>', unsafe_allow_html=True)
    st.warning("🚚 Spedizione GRATUITA sopra i 50€ o se acquistata insieme a una Box!")
    
    st.markdown('<div class="card">👕 <b>Body Cotone Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    st.button("Aggiungi")

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px;">Il tuo profilo</div>', unsafe_allow_html=True)
    st.text_input("Nome Mamma")
    st.text_input("Email")
    
    st.markdown("---")
    st.markdown("<b>📍 Il tuo Locker di fiducia</b>", unsafe_allow_html=True)
    if st.button("🔍 Trova Locker vicino a me"):
        st.info("Richiesta posizione in corso... (Simulazione: Locker Piazza Duomo trovato)")
    st.text_input("Indirizzo Locker selezionato", placeholder="Es: Via Roma 10, Milano")
    
    st.button("SALVA PROFILO")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="padding:20px; text-align:center;"><h3>Siamo genitori, come te. ❤️</h3><p>Abbiamo creato LoopBaby per abbattere gli sprechi e i costi della crescita.</p></div>', unsafe_allow_html=True)

# --- 4. BARRA NAVIGAZIONE ---
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
    if st.button("👋\nChi Siamo"): vai("ChiSiamo")
