import streamlit as st
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE CSS (Fedele al tuo design) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4 { color: #0d9488 !important; font-family: 'Helvetica'; }
    p, li { color: #4b5563 !important; font-size: 0.95em; }
    
    /* Pulsanti come nel design */
    .stButton>button { 
        border-radius: 10px !important; height: 3em !important; 
        background: #ec4899 !important; /* Rosa come nel tuo tasto 'Scegli la tua Box' */
        color: white !important; border: none !important; width: 100% !important;
        font-weight: bold !important;
    }
    
    /* Card per sezioni */
    .info-card { 
        background: #f9fafb; padding: 20px; border-radius: 15px; 
        border: 1px solid #e5e7eb; margin-bottom: 20px; 
    }
    .price-tag { color: #ec4899; font-weight: bold; font-size: 1.1em; }
    .badge-promo { background: #fef3c7; color: #d97706; padding: 5px 10px; border-radius: 10px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DI NAVIGAZIONE ---
if "pagina" not in st.session_state: st.session_state.pagina = "Home"

def cambia_pag(nome): st.session_state.pagina = nome

# --- 4. SIDEBAR MENU ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.title("LoopBaby")
    if st.button("🏠 Home"): cambia_pag("Home")
    if st.button("📦 Le nostre Box"): cambia_pag("Box")
    if st.button("🛍️ Vetrina Shop"): cambia_pag("Vetrina")
    if st.button("📖 Come Funziona"): cambia_pag("Info")
    if st.button("👤 Il mio Profilo"): cambia_pag("Profilo")
    if st.button("👋 Chi Siamo"): cambia_pag("ChiSiamo")

# --- PAGINA: HOME ---
if st.session_state.pagina == "Home":
    st.title("Ciao Mamma! 👋")
    st.subheader("Vestiamo il tuo bambino con amore e qualità, senza sprechi.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("✅ Capi di qualità selezionati")
        st.write("✅ Cambi quando cresce")
        st.write("✅ Risparmi più di 1000€")
    
    if st.button("Scegli la tua Box ➔"): cambia_pag("Box")
    
    st.image("https://placeholder.com") # Qui andrà la foto del bimbo

# --- PAGINA: BOX ---
elif st.session_state.pagina == "Box":
    st.title("Scegli la tua Box 📦")
    
    # Box Standard
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("BOX STANDARD - 19,90€")
        st.write("3 stili tra cui scegliere: **LUNA** (Neutro), **SOLE** (Vivace), **NUVOLA** (Casual).")
        st.image("https://placeholder.com")
        if st.button("Scegli STANDARD"): st.success("Hai scelto la Box Standard!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Box Premium
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("BOX PREMIUM - 29,90€")
        st.write("10 capi selezionati dei migliori brand.")
        st.image("https://placeholder.com")
        if st.button("Scegli PREMIUM"): st.success("Hai scelto la Box Premium!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGINA: VETRINA ---
elif st.session_state.pagina == "Vetrina":
    st.title("Vetrina Shop 🛍️")
    st.write("Capi che restano tuoi per sempre.")
    
    items = [
        {"n": "Body in cotone bio", "p": "9,90€"},
        {"n": "Completo salopette", "p": "19,90€"},
        {"n": "Felpa con cappuccio", "p": "15,90€"},
        {"n": "Giacca leggera", "p": "24,90€"}
    ]
    
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="info-card" style="text-align:center;">
                <p style="font-size:3em;">👕</p>
                <b>{item['n']}</b><br>
                <span class="price-tag">{item['p']}</span>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Aggiungi", key=f"btn_{i}")

# --- PAGINA: INFO (REGOLE E FUNZIONAMENTO) ---
elif st.session_state.pagina == "Info":
    st.title("Come funziona 🔄")
    st.markdown("""
    1. **Scegli la Box:** Lo stile e la taglia che preferisci.
    2. **Ritiro al Locker:** Ricevi la box vicino a te.
    3. **Controlla entro 48h:** Se c'è un problema, contattaci.
    4. **Dopo 3 mesi scegli:** Cambia box o restituisci.
    """)
    
    st.divider()
    st.subheader("Regole importanti ⚠️")
    st.info("Il reso è GRATIS se ordini la box successiva. Se restituisci senza cambiare, il costo è di 7,90€.")

# --- PAGINA: CHI SIAMO ---
elif st.session_state.pagina == "ChiSiamo":
    st.title("Chi siamo? ❤️")
    st.write("### Siamo genitori, come te.")
    st.write("Abbiamo vissuto sulla nostra pelle quanto sia impegnativo far crescere un bambino: vestiti che durano poco, costi che aumentano, tempo che non basta mai.")
    st.write("**Il nostro obiettivo:** Offrirti vestiti di qualità, risparmiare e lasciare un mondo migliore ai nostri figli.")
    
    st.subheader("Contatti")
    st.write("💬 WhatsApp: 333 1234567")
    st.write("📧 Email: hello@loopbaby.it")
