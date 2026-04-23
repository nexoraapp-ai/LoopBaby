import streamlit as st
import os
import base64
from datetime import date

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Funzione per fissare la foto bimbo.jpg (Base64)
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

# --- 2. CSS "SCHELETRO" CON COLORI BOX ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header Logo */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-title { font-size: 30px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .logo-heart { color: #f43f5e; font-size: 32px; }
    .slogan { font-size: 13px; color: #64748b; margin-top: -5px; }

    /* Layout Home */
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }
    .item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 25px; object-fit: cover; }

    /* CARD COLORATE BOX */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .box-luna { background-color: #f1f5f9; border-color: #cbd5e1; color: #1e293b; } /* Grigio Luna */
    .box-sole { background-color: #fffbeb; border-color: #fef3c7; color: #92400e; } /* Giallo Sole */
    .box-nuvola { background-color: #e0f2fe; border-color: #bae6fd; color: #075985; } /* Azzurro Nuvola */
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; border: none; }
    
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .prezzo-bianco { color: white; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa Identico */
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 15px !important; width: 85% !important; height: 55px !important;
        font-size: 16px !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important;
    }

    /* Barra Navigazione Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999; padding: 8px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER COSTANTE
st.markdown('<div class="header-box"><div class="logo-title"><span class="logo-heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

# -- HOME --
if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    st.markdown(f"""
        <div class="home-grid">
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                <div class="item">👶 Capi di qualità selezionati</div>
                <div class="item">🔄 Cambi quando cresce</div>
                <div class="item">💰 Risparmi più di 1000€ l’anno</div>
                <div class="item">🏠 Scegli il locker più vicino a te</div>
                <div class="item">🧘 Zero stress per te</div>
            </div>
            <div class="col-right">{img_html}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

# -- INFO (REGOLE E CAMBIO ANTICIPATO) --
elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; color: #1e293b; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6;">
            <div style="margin-bottom:15px;"><b>1. LoopBaby:</b> Ricevi 10 capi selezionati. Qualità <b>Standard</b> (usato in ottimo stato) o <b>Premium</b> (capi nuovi o seminuovi).</div>
            <div style="margin-bottom:15px;"><b>2. Scegli e ricevi:</b> Scegli lo stile e ricevi la Box nel locker più vicino a te.</div>
            <div style="margin-bottom:15px;"><b>3. Controlla entro 48h:</b> Segnalaci qualsiasi problema appena ricevi i capi.</div>
            <div style="margin-bottom:15px;"><b>4. Regola del 10:</b> Il patto è semplice. Prendi 10 capi, rendi 10 capi.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 20px; color: #1e293b; text-align:center;">Vuoi cambiare prima?</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding: 0 20px; font-size: 14px; color: #475569;">Se il tuo bambino cresce prima dei 3 mesi, contattaci! Scegli la nuova Box e il ritiro + consegna sono a carico nostro!</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 20px; color: #1e293b; text-align:center;">Regole importanti</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:15px 20px; font-size:13px; color:#475569; line-height:1.6; background:#fff1f2; border-radius:20px; margin:0 20px;">• Se rinnovi la Box, ritiro e consegna sono <b>GRATUITI</b>.<br>• Se restituisci senza cambiare, il costo è di 7,90€.<br>• Regola del 10 o 5 euro a capo mancante.<br>• Controlla tutto entro 48 ore dal ritiro.</div>', unsafe_allow_html=True)

# -- BOX (COLORATE) --
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 22px; text-align:center;">Scegli la tua Box</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro (Bianco, Panna, Grigio)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli LUNA", key="l")
    
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Vivace (Colori e Fantasie)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli SOLE", key="s")
    
    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual (Denim e Sportivo)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli NUVOLA", key="n")

    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p_box")

# -- SHOP --
elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding: 0 20px; color:#475569; font-size:14px; margin-bottom:15px;">Ciò che acquisti in vetrina <b>rimane a te</b> per sempre.</div>', unsafe_allow_html=True)
    st.warning("🚚 Spedizione GRATUITA sopra i 50€ o associata ad una Box!")
    
    st.markdown('<div class="card">👕 <b>Body Cotone Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    st.button("Compra ora")

# -- PROFILO (DATI MAMMA + BIMBO + LOCKER) --
elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    
    st.subheader("Dati Mamma")
    st.text_input("Nome Mamma", "Giulia Rossi")
    st.text_input("Cellulare", "333 1234567")
    st.text_input("Email", "giulia@email.it")
    
    st.subheader("Dati del Bambino")
    st.text_input("Nome del bambino", "Leonardo")
    st.date_input("Data di nascita", date(2024, 5, 12))
    st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.5)
    
    st.markdown("---")
    st.markdown("<b>📍 Il tuo Locker</b>", unsafe_allow_html=True)
    if st.button("🔍 Trova Locker vicino a me"):
        st.info("Ricerca in corso sulla tua posizione...")
    st.text_input("Indirizzo Locker preferito")
    
    st.button("SALVA PROFILO")

# -- CHI SIAMO --
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b style="font-size:18px;">Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino. 
            Per questo abbiamo creato LoopBaby: per semplificarti la vita e ridurre gli sprechi.
        </div>
        <div style="background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3;">
            <b style="color:#f43f5e;">Il nostro obiettivo?</b><br>
            Offrirti qualità, farti risparmiare e lasciare un mondo migliore ai nostri figli.
        </div>
    """, unsafe_allow_html=True)

# --- 4. BARRA NAVIGAZIONE FISSA ---
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
