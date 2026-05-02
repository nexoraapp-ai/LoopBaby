import streamlit as st
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# SESSION STATE
# =========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "nome_genitore": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": "",
        "taglia": "50-56 cm",
        "locker": ""
    }

# =========================
# LOCKER (TUTTA ITALIA)
# =========================
LOCKERS = [
    "InPost - Milano Centrale",
    "InPost - Roma Termini",
    "InPost - Torino Porta Nuova",
    "InPost - Napoli Centro",
    "InPost - Firenze SMN",
    "Amazon Locker - Bologna",
    "Poste Italiane - Milano Duomo",
    "Poste Italiane - Roma EUR",
    "Carrefour Locker - Verona",
    "Esselunga Locker - Brescia"
]

# =========================
# FUNZIONI
# =========================
def vai(p): st.session_state.pagina = p

def add_cart(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast("Aggiunto al carrello")

# =========================
# CSS BASE
# =========================
st.markdown("""
<style>
.stApp {background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button {background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER LOGO
# =========================
st.markdown("""
<div style="text-align:center;">
    <h1>LOOPBABY 🌸</h1>
</div>
""", unsafe_allow_html=True)

# =========================
# MENU (HAMBURGER STYLE SIDEBAR)
# =========================
with st.sidebar:
    st.title("🍔 Menu")

    scelta = st.radio("", [
        "Home",
        "Box",
        "Vetrina",
        "Profilo",
        "Carrello",
        "Info",
        "ChiSiamo",
        "Contatti"
    ])

vai(scelta)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    st.image("logo.png", width=140)

    st.markdown("### Ciao 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        LoopBaby è il sistema circolare per vestire i bambini senza sprechi.

        👶 Capi selezionati  
        🔄 Cambio taglia automatico  
        ♻️ Riutilizzo continuo  
        💰 Risparmio reale  
        """)

    with col2:
        if os.path.exists("bimbo.jpg"):
            st.image("bimbo.jpg")

    st.markdown("""
    <div class="card">
    ✨ Scopri la tua prima Box personalizzata
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Box LoopBaby")

    st.markdown("### Standard")

    box_standard = [
        ("LUNA 🌙", 19.90),
        ("SOLE ☀️", 19.90),
        ("NUVOLA ☁️", 19.90)
    ]

    for n,p in box_standard:
        st.markdown(f"<div class='card'><b>{n}</b><br>{p}€</div>", unsafe_allow_html=True)
        if st.button(f"Scegli {n}"):
            add_cart(f"Box {n}", p)

    st.markdown("### Premium 💎")

    st.markdown("""
    <div class="card" style="background:#4f46e5;color:white;">
    BOX PREMIUM<br>
    Capi selezionati premium<br>
    29.90€
    </div>
    """, unsafe_allow_html=True)

    if st.button("Scegli Premium"):
        add_cart("Box Premium", 29.90)

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":

    st.markdown("## 🛍️ Vetrina")

    st.markdown("""
    <div class="card">
    I capi della Vetrina rimangono per sempre a te.<br><br>

    🚚 Spedizione:<br>
    - GRATIS con Box<br>
    - GRATIS sopra 50€<br>
    - 7,90€ sotto 50€
    </div>
    """, unsafe_allow_html=True)

    prodotti = [
        ("Body Bio LoopLove", 9.90),
        ("Tutina Cotton Soft", 14.90),
        ("Set Premium Baby", 24.90)
    ]

    for n,p in prodotti:
        st.markdown(f"<div class='card'><b>{n}</b><br>{p}€</div>", unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            add_cart(n,p)

# =========================
# PROFILO
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    p = st.session_state.profile

    p["nome_genitore"] = st.text_input("Nome Genitore", p["nome_genitore"])
    p["telefono"] = st.text_input("Telefono", p["telefono"])
    p["nome_bambino"] = st.text_input("Nome Bambino", p["nome_bambino"])
    p["taglia"] = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm"])
    p["locker"] = st.selectbox("Locker", LOCKERS)

    if st.button("Salva Profilo"):
        st.session_state.profile = p
        st.success("Profilo aggiornato")

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for item in st.session_state.carrello:
        st.write(f"{item['nome']} - {item['prezzo']}€")
        totale += item["prezzo"]

    st.markdown(f"### Totale: {totale}€")

    st.markdown("🚧 Pagamento (attivo domani)")

    if st.button("Procedi al pagamento"):
        st.info("Funzione pagamento in arrivo domani 💳")

# =========================
# INFO
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona")

    st.markdown("""
    1. Scegli Box  
    2. Ricevi al locker  
    3. Provi i capi  
    4. Cambi taglia  
    5. Continui il ciclo  
    """)

# =========================
# CHI SIAMO
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori come te.

    LoopBaby nasce per ridurre sprechi e far risparmiare famiglie.

    ♻️ Moda circolare per bambini
    """)

# =========================
# CONTATTI
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com  
    📱 392 140 4637  
    """)
