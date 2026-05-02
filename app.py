import streamlit as st
import requests
import os
import base64
import json
import webbrowser
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# LOGO CENTER (COME TUO CODICE)
# =========================
def get_base64(path):
    if os.path.exists(path):
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo = get_base64("logo.png")
bimbo = get_base64("bimbo.jpg")

st.markdown(f"""
<div style="text-align:center; margin-top:10px;">
    <img src="data:image/png;base64,{logo}" style="width:140px;">
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
        "nome_genitore": "Mamma",
        "email": "",
        "telefono": "",
        "bambino": "",
        "nascita": "",
        "taglia": "50-56 cm",
        "locker": ""
    }

# =========================
# LOCKER ITALIA (REALI + GENERICI)
# =========================
LOCKER = [
    "InPost Italia",
    "Poste Italiane Italia",
    "Amazon Locker Italia",
    "Esselunga Locker",
    "Carrefour Locker",
    "Milano Centro",
    "Roma Termini",
    "Torino Porta Nuova",
    "Napoli Centro",
    "Calolziocorte (LC)",
    "Bergamo Centro",
    "Brescia Centro",
    "Tutta Italia (rete completa)"
]

# =========================
# FUNZIONI
# =========================
def vai(p): st.session_state.pagina = p

def add_cart(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})

def remove_item(i):
    st.session_state.carrello.pop(i)

def whatsapp():
    webbrowser.open("https://wa.me/393921404637")

# =========================
# STYLE (TUO + MIGLIORATO)
# =========================
st.markdown("""
<style>
.stApp {background:#FDFBF7; max-width:450px; margin:auto;}
div.stButton > button {background:#f43f5e;color:white;border-radius:18px;width:100%;}
.card{background:white;padding:15px;border-radius:20px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU (SIDEBAR HAMBURGER)
# =========================
with st.sidebar:
    st.markdown("## 🍔 Menu")
    scelta = st.radio("", [
        "Home","Box","Vetrina","Profilo",
        "Carrello","Info","ChiSiamo","Contatti"
    ])
    vai(scelta)

# =========================
# HOME (COMPLETA COME BRAND)
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.user.get("nome_genitore","Mamma")

    st.markdown(f"### Ciao {nome} 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **LoopBaby è la moda circolare per bambini**

        👶 Capi selezionati  
        🔄 Cambio taglia automatico  
        ♻️ Zero sprechi  
        💰 Risparmio reale  
        """)

    with col2:
        if bimbo:
            st.image("bimbo.jpg")

    st.markdown("""
    <div class="card">
    ✨ Scopri la tua Box personalizzata e inizia il ciclo LoopBaby
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX (IDENTICO CONCEPT TUO)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Scegli la tua Box")

    col1, col2 = st.columns(2)

    # STANDARD
    with col1:
        st.markdown("### STANDARD")
        st.markdown("**14,90€ spedizione inclusa**")

        st.markdown("""
        ✔ Capi usati in buono stato  
        ✔ Igienizzati e selezionati  
        ✔ Qualità LoopBaby  
        """)

        colori = st.multiselect(
            "Colori",
            ["Neutro","Rosa","Azzurro","Mix","Pastello"]
        )

        taglie = st.multiselect(
            "Taglie",
            ["50-56","62-68","74-80","86-92"]
        )

        if st.button("Aggiungi Box Standard"):
            add_cart("Box Standard", 14.90)

    # PREMIUM
    with col2:
        st.markdown("### PREMIUM 💎")
        st.markdown("**24,90€**")

        st.markdown("""
        ✔ Vestiti nuovi o seminuovi  
        ✔ Alta qualità  
        ✔ Brand selezionati  
        """)

        colori2 = st.multiselect(
            "Colori premium",
            ["Bianco","Beige","Pastello","Elegante"]
        )

        taglie2 = st.multiselect(
            "Taglie premium",
            ["50-56","62-68","74-80","86-92"]
        )

        if st.button("Aggiungi Box Premium"):
            add_cart("Box Premium", 24.90)

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

    u = st.session_state.user

    u["nome_genitore"] = st.text_input("Nome", u["nome_genitore"])
    u["email"] = st.text_input("Email", u["email"])
    u["telefono"] = st.text_input("Telefono", u["telefono"])
    u["bambino"] = st.text_input("Nome Bambino", u["bambino"])
    u["taglia"] = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm"])
    u["locker"] = st.selectbox("Locker Italia", LOCKER)

    st.session_state.user = u

# =========================
# CARRELLO (AMAZON STYLE)
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for i,item in enumerate(st.session_state.carrello):
        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"{item['nome']} - {item['prezzo']}€")

        with col2:
            if st.button("❌", key=f"del{i}"):
                remove_item(i)
                st.rerun()

        totale += item["prezzo"]

    st.markdown(f"### Totale: {totale}€")

    st.button("Procedi al pagamento (attivo domani)")

# =========================
# INFO (COMPLETO)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    1. Scegli la tua Box  
    2. Ricevi al locker  
    3. Provi i capi  
    4. Se il bambino cresce cambi taglia  
    5. Restituisci e continui il ciclo  

    ♻️ Sistema circolare reale, senza sprechi
    """)

# =========================
# CHI SIAMO (COMPLETO)
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori come te.

    LoopBaby nasce per:

    - Ridurre sprechi nell’abbigliamento baby  
    - Far risparmiare famiglie  
    - Creare un sistema circolare vero  

    Ogni capo ha una seconda vita.
    """)

# =========================
# CONTATTI (WHATSAPP CLICK)
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com  
    📱 WhatsApp: 392 140 4637  
    """)

    if st.button("Apri WhatsApp"):
        whatsapp()
