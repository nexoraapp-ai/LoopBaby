import streamlit as st
import webbrowser
import os

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = {
        "nome": "Mamma",
        "citta": "",
        "locker": ""
    }

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "promo" not in st.session_state:
    st.session_state.promo = False

# =========================
# LOCKER LOGICA (SEMPLICE SMART MATCH)
# =========================
LOCKER_MAP = {
    "milano": ["InPost Milano Centrale","Esselunga Milano","Amazon Locker Milano"],
    "roma": ["Poste Roma Termini","InPost Roma Centro"],
    "torino": ["InPost Torino Porta Nuova"],
    "napoli": ["Poste Napoli Centro"],
    "bergamo": ["Locker Bergamo Centro"],
    "calolziocorte": ["InPost Lecco Area","Locker Provincia LC"],
}

def suggerisci_locker(citta):
    c = citta.lower()
    for k,v in LOCKER_MAP.items():
        if k in c:
            return v
    return ["InPost Italia","Poste Italiane Italia","Amazon Locker Italia"]

# =========================
# FUNZIONI
# =========================
def vai(p): st.session_state.pagina = p

def add(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})

def whatsapp():
    webbrowser.open("https://wa.me/393921404637")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp{background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button{background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGO CENTRO
# =========================
st.image("logo.png", width=120)

# =========================
# MENU
# =========================
with st.sidebar:
    st.radio("Menu", ["Home","Box","Vetrina","Promo","Profilo","Carrello","Info","ChiSiamo","Contatti"], key="m")
    vai(st.session_state.m)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.user["nome"]

    st.markdown(f"### Ciao {nome} 👋")

    st.markdown("""
    LoopBaby è un sistema, non uno shop.

    👶 Vestiti che crescono con il bambino  
    🔄 Ciclo continuo  
    ♻️ Zero sprechi  
    💰 Risparmio reale  
    """)

# =========================
# BOX (COLONNE COME TUO CODICE ORIGINALE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Box LoopBaby")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### STANDARD")
        st.markdown("14,90€ spedizione inclusa")

        st.markdown("""
        ✔ Capi usati in buono stato  
        ✔ Igienizzati  
        ✔ Selezione LoopBaby  
        """)

        if st.button("Box Standard"):
            add("Box Standard", 14.90)

    with col2:
        st.markdown("### PREMIUM 💎")
        st.markdown("24,90€")

        st.markdown("""
        ✔ Nuovi o seminuovi  
        ✔ Alta qualità  
        """)

        if st.button("Box Premium"):
            add("Box Premium", 24.90)

# =========================
# VETRINA
# =========================
elif st.session_state.pagina == "Vetrina":

    st.markdown("## 🛍️ Vetrina")

    st.markdown("""
    I capi restano sempre tuoi.

    🚚 Spedizione:
    - GRATIS con Box
    - GRATIS sopra 50€
    - 7,90€ sotto 50€
    """)

# =========================
# PROMO MAMME FONDATRICI (FIX COMPLETO)
# =========================
elif st.session_state.pagina == "Promo":

    st.markdown("## ✨ Promo Mamme Fondatrici")

    check = st.checkbox("Attiva Promo Mamme Fondatrici")

    if check:

        peso = st.text_input("Peso pacco (kg)")
        dimensioni = st.text_input("Dimensioni (es 30x30x40)")
        citta = st.text_input("Città / Paese")
        locker = st.selectbox("Locker suggeriti", suggerisci_locker(citta))

        if st.button("Invia richiesta"):

            st.success("Richiesta inviata!")

            st.info("""
            📦 ENTRO 48 ORE riceverai:
            - etichetta spedizione
            - istruzioni ritiro

            🚚 Ritiro sempre pagato da noi
            """)

# =========================
# PROFILO (FIX)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    u = st.session_state.user

    u["nome"] = st.text_input("Nome", u["nome"])
    u["citta"] = st.text_input("Città", u["citta"])

    if u["citta"]:
        st.markdown("### Locker vicini a te")
        st.write(suggerisci_locker(u["citta"]))

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

    st.button("Checkout (attivo domani)")

# =========================
# INFO (SISTEMA COMPLETO)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    LoopBaby è un sistema, non un negozio.

    ### 📦 Ciclo:

    - Ricevi Box
    - Usi per 90 giorni

    ### ⏱️ Regola 2 giorni:
    Nei primi 2 giorni puoi segnalare problemi via mail o WhatsApp

    ### 🔁 Dopo 90 giorni:
    - Nuova Box (taglia successiva) → ritiro GRATIS
    - Restituzione → costo 7,90€

    In entrambi i casi:
    👉 noi inviamo l’etichetta
    👉 tu porti il pacco al locker

    ### ♻️ Patto del 10:
    - 10 capi restituiti
    - sostituzione jeans x jeans oppure 5€

    LoopBaby non è uno shop.
    È un modo di essere migliore.
    """)

# =========================
# CHI SIAMO (VERSIONE STARTUP SERIA)
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori.

    Abbiamo creato LoopBaby perché il sistema attuale non funziona.

    ### Problemi:
    - bambini crescono velocemente
    - vestiti costano troppo
    - spreco enorme

    ### Soluzione:
    LoopBaby è un sistema circolare:

    ♻️ I vestiti non si buttano  
    ♻️ I vestiti non si accumulano  
    ♻️ I vestiti circolano tra famiglie  

    ### Visione:
    creare il primo guardaroba condiviso per bambini in Europa.

    Non è un e-commerce.
    È un sistema sociale.
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
