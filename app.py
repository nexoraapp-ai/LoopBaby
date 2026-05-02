import streamlit as st
import requests
import base64
import os
import webbrowser
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# FUNZIONI IMMAGINI
# =========================
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo = get_base64("logo.png")
bimbo = get_base64("bimbo.jpg")

# =========================
# LOGO CENTRATO (SOLO LOGO)
# =========================
st.markdown(f"""
<div style="text-align:center;">
    <img src="data:image/png;base64,{logo}" style="width:120px;">
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "user" not in st.session_state:
    st.session_state.user = {
        "nome": "Mamma",
        "citta": "",
        "locker": ""
    }

# =========================
# LOCKER (TUTTA ITALIA)
# =========================
LOCKER_LIST = [
    "InPost Italia",
    "Poste Italiane Italia",
    "Amazon Locker Italia",
    "Esselunga Locker",
    "Carrefour Locker",
    "Milano",
    "Roma",
    "Torino",
    "Napoli",
    "Bergamo",
    "Brescia",
    "Calolziocorte (LC)"
]

# =========================
# FUNZIONI
# =========================
def vai(p): st.session_state.pagina = p

def add(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})

def whatsapp():
    webbrowser.open("https://wa.me/393921404637")

# =========================
# STYLE BASE
# =========================
st.markdown("""
<style>
.stApp {background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button {background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU (HAMBURGER)
# =========================
with st.sidebar:
    st.radio("Menu", [
        "Home","Box","Vetrina","Promo Mamme Fondatrici",
        "Profilo","Carrello","Info","ChiSiamo","Contatti"
    ], key="menu")
    vai(st.session_state.menu)

# =========================
# HOME (FIX: FOTO PICCOLA + NOME UTENTE)
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.user["nome"]

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"### Ciao {nome} 👋")

        st.markdown("""
        LoopBaby è il sistema circolare per vestire i bambini.

        👶 qualità selezionata  
        🔄 crescita continua  
        ♻️ zero sprechi  
        💰 risparmio reale  
        """)

    with col2:
        if bimbo:
            st.image("bimbo.jpg", width=120)

    st.markdown("""
    <div class="card">
    ✨ Inizia il tuo ciclo LoopBaby con la tua prima Box
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX (COME TUO CODICE: COLONNE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Scegli la tua Box")

    col1, col2 = st.columns(2)

    # STANDARD
    with col1:
        st.markdown("### STANDARD")
        st.markdown("14,90€ spedizione inclusa")

        st.markdown("""
        ✔ Capi usati in buono stato  
        ✔ Igienizzati  
        ✔ Selezione qualità  
        """)

        option1 = st.radio("Colori Standard", ["Neutro","Rosa","Azzurro","Mix"], key="std")

        if st.button("Aggiungi Standard"):
            add("Box Standard", 14.90)

    # PREMIUM
    with col2:
        st.markdown("### PREMIUM 💎")
        st.markdown("24,90€")

        st.markdown("""
        ✔ Vestiti nuovi o seminuovi  
        ✔ Alta qualità  
        """)

        option2 = st.radio("Colori Premium", ["Bianco","Beige","Elegante"], key="pre")

        if st.button("Aggiungi Premium"):
            add("Box Premium", 24.90)

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":

    st.markdown("## 🛍️ Vetrina")

    st.markdown("""
    I capi della Vetrina rimangono per sempre a te.

    🚚 Spedizione:
    - GRATIS con Box
    - GRATIS sopra 50€
    - 7,90€ sotto 50€
    """)

    prodotti = [
        ("Body LoopLove", 9.90),
        ("Tutina Soft", 14.90),
        ("Set Premium Baby", 24.90)
    ]

    for n,p in prodotti:
        st.markdown(f"<div class='card'><b>{n}</b><br>{p}€</div>", unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            add(n,p)

# =========================
# PROMO MAMME FONDATRICI (FIX COMPLETO)
# =========================
elif st.session_state.pagina == "Promo Mamme Fondatrici":

    st.markdown("## ✨ Promo Mamme Fondatrici")

    attiva = st.checkbox("Attiva Promo")

    if attiva:

        peso = st.text_input("Peso pacco")
        dimensioni = st.text_input("Dimensioni")
        citta = st.text_input("Città / Paese")

        locker = st.selectbox("Locker disponibili", LOCKER_LIST)

        if st.button("Invia richiesta"):

            st.success("Richiesta inviata!")

            st.info("""
            📦 ENTRO 48 ORE riceverai:
            - etichetta spedizione
            - istruzioni consegna

            🚚 Ritiro sempre gratuito da parte nostra
            """)

# =========================
# PROFILO (FIX COMPLETO)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    u = st.session_state.user

    u["nome"] = st.text_input("Nome", u["nome"])
    u["citta"] = st.text_input("Città", u["citta"])

    if u["citta"]:
        st.markdown("### Locker consigliati")
        st.write(LOCKER_LIST[:4])

    st.session_state.user = u

# =========================
# CARRELLO (AMAZON STYLE)
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for i,item in enumerate(st.session_state.carrello):

        col1,col2 = st.columns([3,1])

        with col1:
            st.write(item["nome"], "-", item["prezzo"], "€")

        with col2:
            if st.button("❌", key=i):
                st.session_state.carrello.pop(i)
                st.rerun()

        totale += item["prezzo"]

    st.markdown(f"### Totale: {totale}€")

    st.button("Procedi al pagamento (domani)")

# =========================
# INFO (COMPLETO BUSINESS)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    LoopBaby è un sistema, non un semplice shop.

    ### 📦 1. Ricevi la Box

    ### ⏱️ 2. Utilizzo (90 giorni)
    Usi i vestiti normalmente

    ### ⚠️ 3. Primo controllo (2 giorni)
    Nei primi 2 giorni puoi segnalare problemi via email o WhatsApp

    ### 🔁 4. Dopo 90 giorni scegli:

    - Nuova Box (taglia successiva) → ritiro GRATIS  
    - Restituzione → costo 7,90€  

    👉 In entrambi i casi:
    noi inviamo l’etichetta  
    tu porti solo al locker scelto  

    ### ♻️ Patto del 10:

    - restituisci 10 capi  
    - sostituzione jeans x jeans oppure 5€

    LoopBaby è un sistema circolare per migliorare il modo di vestire i bambini.
    """)

# =========================
# CHI SIAMO (VERSIONE FORTE)
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori.

    LoopBaby nasce da un problema reale:

    - i bambini crescono velocemente  
    - i vestiti costano troppo  
    - si spreca troppo  

    ### 🌍 La soluzione

    Un sistema circolare dove i vestiti:

    ✔ non si buttano  
    ✔ non si accumulano  
    ✔ passano da famiglia a famiglia  

    ### 🎯 La nostra missione

    Rendere l’abbigliamento bambino:

    - sostenibile  
    - accessibile  
    - intelligente  

    LoopBaby non è un e-commerce.

    È un sistema.
    """)

# =========================
# CONTATTI (WHATSAPP FIX)
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com  
    📱 WhatsApp: 392 140 4637  
    """)

    if st.button("Apri WhatsApp"):
        whatsapp()
