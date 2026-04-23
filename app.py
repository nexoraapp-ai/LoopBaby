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

# --- 2. CSS "SCHELETRO" (IDENTICO ALLA TUA FOTO) ---
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

    /* Layout Home (Bimbo a destra bloccato) */
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 20px; }
    .item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 25px; object-fit: cover; }

    /* Card grafiche */
    .card { border-radius: 25px; padding: 20px; margin: 15px 20px; text-align: center; border: 1px solid #eee; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }
    .regola-box { background-color: #f0fdfa; border: 1px solid #0d9488; border-radius: 20px; padding: 20px; margin: 20px; }

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
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important;
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

# -- INFO (5 PUNTI + REGOLA DEL 10) --
elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; color: #1e293b; text-align:center;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6;">
            <div style="margin-bottom:15px;"><b>1. LoopBaby:</b> Ricevi 10 capi selezionati. Qualità <b>Standard</b> (usato in ottimo stato) o <b>Premium</b> (grandi firme, capi nuovi o seminuovi).</div>
            <div style="margin-bottom:15px;"><b>2. Scegli e ricevi:</b> Seleziona lo stile e ricevi la Box nel locker più vicino a te.</div>
            <div style="margin-bottom:15px;"><b>3. Controlla entro 48h:</b> Segnalaci qualsiasi problema appena ricevi i capi.</div>
            <div style="margin-bottom:15px;"><b>4. Regola del 10:</b> Il patto è semplice. Prendi 10 capi, rendi 10 capi.</div>
            <div style="margin-bottom:15px;"><b>5. Cambia taglia:</b> Quando cresce, rendi la vecchia box e ricevi la nuova!</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="regola-box">
            <b style="color:#0d9488; font-size:18px;">💡 LA REGOLA DEL 10</b><br>
            Per far girare l'armadio di LoopBaby, chiediamo di rendere lo stesso numero di capi ricevuti (10). 
            Se un capo manca o è danneggiato irreparabilmente, la penale è di soli <b>5€</b>.
        </div>
    """, unsafe_allow_html=True)

# -- BOX --
elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 22px; text-align:center;">Scegli la tua Box</div>', unsafe_allow_html=True)
    for stile in ["LUNA 🌙 (Neutro)", "SOLE ☀️ (Vivace)", "NUVOLA ☁️ (Casual)"]:
        st.markdown(f'<div class="card"><h3>{stile}</h3><p>Qualità Standard (Usato)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        st.button(f"Scegli {stile}", key=stile)
    st.markdown('<div class="card" style="background:#0d9488; color:white;"><h3>PREMIUM 💎</h3><p>Grandi firme (Nuovo/Seminuovo)</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p_box")

# -- SHOP (REGOLE VETRINA) --
elif st.session_state.pagina == "Shop":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding: 0 20px; color:#475569; font-size:14px; margin-bottom:15px;">Ciò che acquisti in vetrina <b>rimane a te</b> per sempre.</div>', unsafe_allow_html=True)
    st.warning("🚚 Spedizione GRATUITA sopra i 50€ o associata ad una Box!")
    
    st.markdown('<div class="card">👕 <b>Body Cotone Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    st.button("Compra ora")

# -- PROFILO (LOCKER RICERCA) --
elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    st.text_input("Nome Mamma", "Giulia Rossi")
    st.text_input("Email", "giulia@email.it")
    
    st.markdown("---")
    st.markdown("<b>📍 Trova il tuo Locker</b>", unsafe_allow_html=True)
    st.write("Usa la tua posizione per trovare il punto di ritiro più vicino a te.")
    if st.button("🔍 Apri posizione e trova Locker"):
        st.info("Ricerca Locker in corso... Punto trovato: Locker Esselunga Via Roma")
    st.text_input("Indirizzo Locker preferito", placeholder="Inserisci o seleziona l'indirizzo")
    
    st.button("SALVA PROFILO")

# -- CHI SIAMO (TESTO EMOZIONALE COMPLETO) --
elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b style="font-size:18px;">Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che non basta mai.<br><br>
            Per questo abbiamo creato LoopBaby: per semplificarti la vita, farti risparmiare e ridurre gli sprechi, senza rinunciare alla qualità che merita il tuo bambino.
        </div>
        <div style="background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3;">
            <b style="color:#f43f5e;">Il nostro obiettivo?</b><br>
            Offrirti vestiti di qualità, farti risparmiare di più di 1000€ l'anno e lasciare un mondo migliore ai nostri figli.
        </div>
        <div style="text-align:center; font-size:14px; color:#475569;">
            💬 WhatsApp: 333 1234567<br>
            📧 Email: hello@loopbaby.it<br>
            🕒 Lun - Ven 9:00 - 18:00
        </div>
    """, unsafe_allow_html=True)

# --- 4. BARRA NAVIGAZIONE FISSA (6 TASTI) ---
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
