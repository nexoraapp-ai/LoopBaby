import streamlit as st
import os

# --- 1. CONFIGURAZIONE E ICONE ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="logo.png", 
    layout="centered"
)

# --- 2. CSS PERSONALIZZATO (Stile Moodboard) ---
st.markdown("""
    <style>
    /* Sfondo e Font */
    .stApp { background-color: #FFFFFF !important; max-width: 450px; margin: 0 auto; }
    h1, h2, h3 { color: #0d9488 !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Card Prodotti Vetrina */
    .product-card {
        background: #f8fafc;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s;
    }
    .product-card:hover { transform: scale(1.02); }
    .product-price { color: #ec4899; font-weight: bold; font-size: 1.2em; margin: 10px 0; }
    
    /* Pulsanti Rosa Action */
    .stButton>button {
        background: #ec4899 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 3em !important;
    }

    /* Sezione Info/Regole */
    .rule-box {
        background: #f0fdfa;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #0d9488;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGAZIONE ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

def nav(p): st.session_state.pagina = p

# Sidebar fissa come nel design
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.markdown("### Menu LoopBaby")
    if st.button("🏠 Home"): nav("Home")
    if st.button("📦 Le nostre Box"): nav("Box")
    if st.button("🛍️ Vetrina Shop"): nav("Vetrina")
    if st.button("📖 Come Funziona"): nav("Info")
    if st.button("👋 Chi Siamo"): nav("ChiSiamo")

# --- 4. CONTENUTO PAGINE ---

if st.session_state.pagina == "Home":
    st.title("Benvenuta Mamma! ✨")
    st.write("Vestiamo il tuo bambino con amore e qualità, rispettando il pianeta.")
    st.image("https://unsplash.com", caption="Qualità e Sostenibilità")
    if st.button("Scegli la tua Box ➔"): nav("Box")

elif st.session_state.pagina == "Box":
    st.title("Scegli il tuo Loop 📦")
    
    # Box Standard
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.subheader("BOX STANDARD")
    st.write("10 Capi selezionati (Luna, Sole o Nuvola)")
    st.markdown('<p class="product-price">19,90 € / 3 mesi</p>', unsafe_allow_html=True)
    if st.button("Scegli Standard", key="b1"): st.success("Ottima scelta!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Box Premium
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.subheader("BOX PREMIUM")
    st.write("10 Capi grandi firme per il tuo bebè")
    st.markdown('<p class="product-price">29,90 € / 3 mesi</p>', unsafe_allow_html=True)
    if st.button("Scegli Premium", key="b2"): st.success("Lusso e risparmio!")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Vetrina":
    st.title("Vetrina Shop 🛍️")
    st.info("Spedizione GRATIS sopra i 50€")
    
    col1, col2 = st.columns(2)
    prodotti = [
        {"n": "Body Bio", "p": "9,90€", "i": "🌱"},
        {"n": "Salopette", "p": "19,90€", "i": "👖"},
        {"n": "Felpa", "p": "15,90€", "i": "🧸"},
        {"n": "Giacchina", "p": "24,90€", "i": "🧥"}
    ]
    
    for idx, p in enumerate(prodotti):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
            <div class="product-card">
                <div style="font-size:3em;">{p['i']}</div>
                <b>{p['n']}</b>
                <p class="product-price">{p['p']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Aggiungi", key=f"add_{idx}")

elif st.session_state.pagina == "Info":
    st.title("Come Funziona? 🔄")
    steps = [
        "1. Scegli la tua Box e lo stile.",
        "2. Ricevi la box al Locker più vicino.",
        "3. Usa i vestiti per 90 giorni.",
        "4. Cambia taglia e rendi la vecchia box!"
    ]
    for s in steps:
        st.markdown(f'<div class="rule-box">{s}</div>', unsafe_allow_html=True)
    
    st.warning("⚠️ Controlla i capi entro 48h dalla ricezione!")

elif st.session_state.pagina == "ChiSiamo":
    st.title("La nostra Storia ❤️")
    st.write("LoopBaby nasce da genitori per i genitori. Crediamo nel consumo circolare per garantire un futuro migliore ai nostri figli.")
    st.divider()
    st.markdown("📧 **Email:** info@loopbaby.it")
    st.markdown("💬 **WhatsApp:** +39 333 1234567")
