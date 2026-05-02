import streamlit as st
import webbrowser
import os
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# IMMAGINI
# =========================
def b64(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = b64("logo.png")
bimbo = "bimbo.jpg"

# =========================
# HEADER LOGO ALLUNGATO (COME TUO PRIMO CODICE)
# =========================
st.markdown(f"""
<div style="
background: linear-gradient(to right,#fff,#fff1f2);
padding:20px;
border-radius:0 0 30px 30px;
text-align:center;
">
    <img src="data:image/png;base64,{logo}" style="width:220px;">
</div>
""", unsafe_allow_html=True)

# =========================
# SESSION
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
# LOCKER ITALIA COMPLETO (LOGICA PAESI → LOCKER)
# =========================
LOCKER_MAP = {
    "milano": ["InPost Milano Centrale","Esselunga Milano","Amazon Locker Milano"],
    "roma": ["Poste Roma Termini","InPost Roma Centro","Amazon Locker Roma"],
    "torino": ["InPost Torino Porta Nuova","Poste Torino Centro"],
    "napoli": ["Poste Napoli Centro","InPost Napoli"],
    "bergamo": ["Locker Bergamo Centro"],
    "brescia": ["Locker Brescia Centro"],
    "lecco": ["InPost Lecco","Locker Provincia LC"],
    "calolziocorte": ["InPost Calolziocorte"],
    "bergamo provincia": ["Locker Bergamo provincia"],
}

def get_lockers_by_city(city):
    c = city.lower()
    for k,v in LOCKER_MAP.items():
        if k in c:
            return v
    return ["InPost Italia","Poste Italiane","Amazon Locker (Tutta Italia)"]

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
.stApp {background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button {background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
with st.sidebar:
    st.radio("Menu", [
        "Home","Box","Vetrina","Promo Mamme Fondatrici",
        "Profilo","Carrello","Info","ChiSiamo","Contatti"
    ], key="m")
    vai(st.session_state.m)

# =========================
# HOME (LOGO + FOTO BAMBINO + 4 PUNTI IN LINEA)
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.user["nome"]

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"### Ciao {nome} 👋")

        st.markdown("""
        LoopBaby è un sistema circolare per vestire bambini.
        """)

        st.markdown("""
        👶 Qualità selezionata  
        🔄 Crescita continua  
        ♻️ Zero sprechi  
        💰 Risparmio reale  
        """)

    with col2:
        st.image(bimbo, width=140)

    st.markdown("""
    <div class="card">
    ✨ Il tuo guardaroba circolare parte da qui
    </div>
    """, unsafe_allow_html=True)

    # PROMO HOME (GRASSETTO CLICCABILE)
    if st.button("🔥 PROMO MAMME FONDATRICI"):
        vai("Promo Mamme Fondatrici")
        st.rerun()

# =========================
# BOX (SOLE GIALLO + STANDARD COME TUO STILE)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Box LoopBaby")

    col1, col2 = st.columns(2)

    # STANDARD
    with col1:
        st.markdown("""
        <div class="card" style="background:#fef9c3;">
        <h3>SOLE ☀️</h3>
        <b>14,90€ spedizione inclusa</b><br><br>
        ✔ Capi usati in buono stato<br>
        ✔ Igienizzati<br>
        ✔ Selezione qualità
        </div>
        """, unsafe_allow_html=True)

        if st.checkbox("Seleziona Sole"):
            st.markdown("### Capi inclusi")
            st.image("https://via.placeholder.com/300x200?text=Sole+Box")

        if st.button("Aggiungi Box Sole"):
            add("Box Sole", 14.90)

    # PREMIUM
    with col2:
        st.markdown("""
        <div class="card">
        <h3>PREMIUM 💎</h3>
        <b>24,90€</b><br><br>
        ✔ Nuovi o seminuovi<br>
        ✔ Alta qualità
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
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
# PROMO MAMME FONDATRICI (FLOW COMPLETO)
# =========================
elif st.session_state.pagina == "Promo Mamme Fondatrici":

    st.markdown("## 🔥 Promo Mamme Fondatrici")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni pacco")
    citta = st.text_input("Città / Paese")

    locker = st.selectbox("Locker disponibili", get_lockers_by_city(citta))

    if st.button("Invia richiesta"):

        st.success("Richiesta inviata!")

        st.info("""
        📦 ENTRO 48 ORE riceverai:
        - etichetta spedizione
        - istruzioni

        🚚 Ritiro sempre gratuito
        """)

# =========================
# PROFILO (FATTO BENE)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    u = st.session_state.user

    u["nome"] = st.text_input("Nome", u["nome"])
    u["citta"] = st.text_input("Città / Paese", u["citta"])

    if u["citta"]:
        st.markdown("### Locker vicino a te")
        st.write(get_lockers_by_city(u["citta"]))

    st.session_state.user = u

# =========================
# CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for item in st.session_state.carrello:
        st.write(item["nome"], "-", item["prezzo"], "€")
        totale += item["prezzo"]

    st.markdown(f"### Totale: {totale}€")

# =========================
# INFO (CHIARO + BUSINESS)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    LoopBaby è un sistema circolare.

    📦 Ricevi la Box  
    ⏱️ Usi per 90 giorni  

    ⚠️ Nei primi 2 giorni puoi segnalare problemi  

    🔁 Dopo 90 giorni:
    - nuova Box (ritiro gratis)
    - oppure restituzione (7,90€)

    👉 In entrambi i casi inviamo noi l’etichetta

    ♻️ Patto del 10:
    10 capi = nuova Box o sostituzione
    """)

# =========================
# CHI SIAMO
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori.

    LoopBaby nasce da un problema reale:

    - vestiti costano troppo  
    - bambini crescono velocemente  
    - spreco enorme  

    ### 🌍 Soluzione:

    Un sistema circolare dove i vestiti:

    ✔ circolano  
    ✔ non si buttano  
    ✔ non si accumulano  

    ### 🎯 Missione:

    Rendere l’abbigliamento bambino sostenibile, economico e intelligente.
    """)

# =========================
# CONTATTI (WHATSAPP OK)
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com  
    📱 WhatsApp: 392 140 4637  
    """)

    if st.button("Apri WhatsApp"):
        whatsapp()
