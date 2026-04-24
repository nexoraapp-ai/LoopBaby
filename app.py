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

# --- 2. CSS "SCHELETRO IDENTICO" (COPIA ESATTA FOTO) ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    .main .block-container {padding: 0 !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Header */
    .header-box { padding: 30px 20px 10px 20px; }
    .logo-h { font-size: 30px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .heart { color: #f43f5e; font-size: 34px; }
    .slogan { font-size: 13px; color: #64748b; margin-top: -5px; padding-left: 5px; }

    /* Layout Home */
    .home-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 15px; align-items: center; padding: 0 20px; margin-top: 10px; }
    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; }
    .item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: #475569; margin-bottom: 8px; font-weight: 500; }
    .baby-photo { width: 100%; border-radius: 25px; object-fit: cover; }

    /* SEZIONE 2 ICONE (VUOI CAMBIARE PRIMA?) */
    .icon-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px 20px; margin-top: 5px; }
    .icon-card { background: #f8fafc; border: 1px solid #eee; border-radius: 15px; padding: 12px 10px; text-align: center; font-size: 11px; color: #475569; }
    .icon-card b { display: block; color: #1e293b; margin: 4px 0; font-size: 12px; }

    /* Card Box / Vetrina */
    .card { border-radius: 20px; padding: 20px; margin: 10px 20px; border: 1px solid #eee; text-align: center; }
    .box-luna { background-color: #f1f5f9; } .box-sole { background-color: #fffbeb; } .box-nuvola { background-color: #e0f2fe; }
    .box-premium { background: linear-gradient(135deg, #0d9488 0%, #065f46 100%); color: white !important; }
    .prezzo-rosa { color: #ec4899; font-size: 24px; font-weight: 900; }

    /* Pulsante Rosa */
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 18px !important; width: 85% !important; height: 55px !important;
        font-size: 17px !important; font-weight: 800 !important; margin: 15px auto !important; display: block !important;
    }

    /* Barra Fissa */
    [data-testid="stHorizontalBlock"] {
        position: fixed !important; bottom: 0 !important; left: 0 !important; width: 100% !important;
        background: white !important; border-top: 1px solid #f1f5f9 !important; z-index: 99999; padding: 8px 0 !important;
    }
    [data-testid="stHorizontalBlock"] button {
        background: transparent !important; color: #0d9488 !important; border: none !important; font-size: 10px !important; font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><div class="logo-h"><span class="heart">💗</span> LoopBaby</div><div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div></div>', unsafe_allow_html=True)

# --- 3. PAGINE ---

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" class="baby-photo">' if img_data else ""
    st.markdown(f"""
        <div class="home-grid">
            <div>
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
                <div style="margin-top:15px;">
                    <div class="item">👶 Capi di qualità selezionati</div>
                    <div class="item">🔄 Cambi quando cresce</div>
                    <div class="item">💰 Risparmi più di 1000€ l’anno</div>
                    <div class="item">🏠 Scegli il locker più vicino a te</div>
                    <div class="item">🧘 Zero stress per te</div>
                </div>
            </div>
            <div>{img_html}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Scegli la tua Box"): vai("Box")
    st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px; margin-top:10px;">❤️ Creato da genitori, per genitori.</p>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center; color:#1e293b;">Come funziona</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 8px 20px; font-size: 13px; color: #475569; line-height: 1.6;">
            <b>1. Le nostre opzioni:</b> Box <b>Standard</b> (capi usati ancora ottimi), Box <b>Premium</b> (nuovi o seminuovi). Nella sezione <b>Vetrina</b>, ciò che acquisti rimane a te per sempre.<br><br>
            <b>2. Scegli e ricevi:</b> Seleziona lo stile e ricevi la Box nel locker più vicino a te.<br><br>
            <b>3. Controllo 48h:</b> Controlla i capi entro 48h dalla ricezione, per qualsiasi problema contattaci (info su Chi Siamo).<br><br>
            <b>4. Dopo 3 mesi:</b> Scegli se rendere o ricevere la nuova taglia (ti ricordiamo 10gg. prima noi).
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding:15px 20px 0 20px; font-weight:800; font-size:18px; text-align:center;">Vuoi cambiare prima?</div>', unsafe_allow_html=True)
    st.markdown('<div class="icon-row">'
                '<div class="icon-card">🔄<br><b>Cambio taglia</b>Se cresce prima, contattaci! (vedi Chi Siamo).</div>'
                '<div class="icon-card">🏠<br><b>Restituisci</b>Se vuoi fermarti, rendi la Box al costo di 7,90€.</div>'
                '</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:20px; font-weight:800; font-size:22px; text-align:center; color:#1e293b;">Regole importanti</div>', unsafe_allow_html=True)
    regole = [
        ("💰", "La Box costa 19,90€ (Standard) o 29,90€ (Premium)."),
        ("🚚", "Se prendi una nuova Box, ritiro e consegna sono <b>GRATUITI</b>."),
        ("€", "Se restituisci senza nuova Box, il ritiro costa 7,90€."),
        ("🕒", "Controlla i capi entro 48h dalla ricezione, per qualsiasi problema contattaci (info su Chi Siamo)."),
        ("💡", "<b>Regola del 10:</b> Rendi 10 capi per riceverne 10. Se rompi o perdi un capo, vale lo scambio <b>'Jeans x Jeans'</b> o 5 euro a capo mancante.")
    ]
    for icon, txt in regole:
        st.markdown(f'<div style="display:flex; gap:12px; padding:8px 20px; align-items:flex-start; font-size:12px; color:#475569;"><div style="font-size:18px; min-width:25px;">{icon}</div><div>{txt}</div></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 22px; text-align:center;">Scegli la tua Box</div>', unsafe_allow_html=True)
    st.markdown('<div class="card box-luna"><h3>LUNA 🌙</h3><p>Neutro (Usato ottimo)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli LUNA", key="l")
    st.markdown('<div class="card box-sole"><h3>SOLE ☀️</h3><p>Vivace (Usato ottimo)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli SOLE", key="s")
    st.markdown('<div class="card box-nuvola"><h3>NUVOLA ☁️</h3><p>Casual (Usato ottimo)</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli NUVOLA", key="n")
    st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="color:white; font-size:24px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
    st.button("Scegli PREMIUM", key="p")

elif st.session_state.pagina == "Vetrina":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Vetrina Shop 🛍️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; padding: 0 20px; color:#475569; font-size:14px; margin-bottom:15px;">Ciò che acquisti in vetrina <b>rimane a te</b> per sempre.</div>', unsafe_allow_html=True)
    st.warning("🚚 Spedizione GRATUITA sopra i 50€ o associata ad una Box!")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh1")
    with col2:
        st.markdown('<div class="card">👖 <b>Salopette</b><br><span class="prezzo-rosa">19,90€</span></div>', unsafe_allow_html=True)
        st.button("Compra", key="sh2")

elif st.session_state.pagina == "Profilo":
    st.markdown('<div style="padding: 20px; font-weight: 800; font-size: 24px; text-align:center;">Il tuo profilo 👤</div>', unsafe_allow_html=True)
    st.text_input("Nome Mamma", "Giulia Rossi")
    st.text_input("Cellulare", "333 1234567")
    st.text_input("Email", "giulia@email.it")
    st.markdown("---")
    st.text_input("Nome Bambino", "Leonardo")
    st.date_input("Data di nascita", date(2024, 5, 12))
    st.markdown("<b>📍 Il tuo Locker di fiducia</b>", unsafe_allow_html=True)
    if st.button("🔍 Trova il più vicino"): st.toast("Ricerca Locker...")
    st.text_input("Indirizzo Locker o Posizione")
    st.button("SALVA PROFILO")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2 style="font-size:24px;">Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
            Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino. Per questo abbiamo creato LoopBaby.
        </div>
        <div style="background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; color:#1e293b;">
            <b style="color:#f43f5e;">Il nostro obiettivo?</b><br>
            Offrirti vestiti di qualità, farti risparmiare più di 1000€ l'anno e lasciare un mondo migliore ai nostri figli.
        </div>
        <div style="text-align:center; font-size:14px; color:#475569; padding:20px;">
            💬 WhatsApp: 333 1234567<br>📧 hello@loopbaby.it<br>🕒 Lun - Ven 9:00 - 18:00
        </div>
    """, unsafe_allow_html=True)

# --- 4. BARRA NAVIGAZIONE FISSA (6 TASTI) ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: if st.button("🏠\nHome"): vai("Home")
with c2: if st.button("📖\nInfo"): vai("Info")
with c3: if st.button("📦\nBox"): vai("Box")
with c4: if st.button("🛍️\nVetrina"): vai("Vetrina")
with c5: if st.button("👤\nProfilo"): vai("Profilo")
with c6: if st.button("👋\nChi Siamo"): vai("ChiSiamo")
