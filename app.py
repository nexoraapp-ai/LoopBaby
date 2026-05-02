import streamlit as st
import os
import webbrowser

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# SESSION
# =========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "utente" not in st.session_state:
    st.session_state.utente = {"nome": "Mamma"}

# =========================
# LOCKER (TUTTA ITALIA + GENERICI)
# =========================
LOCKER = [
    "InPost Italia (Tutti i punti)",
    "Poste Italiane (Tutti i punti)",
    "Amazon Locker Italia",
    "Esselunga Locker",
    "Carrefour Locker",
    "Locker Milano",
    "Locker Roma",
    "Locker Torino",
    "Locker Napoli",
    "Locker Calolziocorte (LC)",
    "Locker Bergamo",
    "Locker Brescia",
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
# LOGO SOLO
# =========================
st.image("logo.png", width=120)

# =========================
# MENU
# =========================
with st.sidebar:
    st.radio("Menu", ["Home","Box","Vetrina","Profilo","Carrello","Info","ChiSiamo","Contatti"], key="menu")
    vai(st.session_state.menu)

# =========================
# HOME
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.utente.get("nome","Mamma")

    st.markdown(f"### Ciao {nome} 👋")

    st.markdown("""
    LoopBaby è il sistema circolare per vestire i bambini senza sprechi.
    """)

# =========================
# BOX (COME HAI CHIESTO IDENTICO STRUTTURA)
# =========================
elif st.session_state.pagina == "Box":

    col1, col2 = st.columns(2)

    # ================= STANDARD
    with col1:
        st.markdown("## 📦 STANDARD")
        st.markdown("**14,90€ (spedizione inclusa)**")

        st.markdown("""
        ✔ Capi usati in buono stato  
        ✔ Igienizzati  
        ✔ Selezione qualità LoopBaby  
        """)

        colori = st.multiselect(
            "Colori disponibili",
            ["Neutro","Rosa","Azzurro","Mix","Pastello"]
        )

        taglie = st.multiselect(
            "Taglie",
            ["50-56","62-68","74-80","86-92"]
        )

        if st.button("Aggiungi Box Standard"):
            add_cart("Box Standard", 14.90)

    # ================= PREMIUM
    with col2:
        st.markdown("## 💎 PREMIUM")
        st.markdown("**24,90€**")

        st.markdown("""
        ✔ Vestiti nuovi o seminuovi  
        ✔ Alta qualità selezionata  
        ✔ Brand premium baby  
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

    nome = st.text_input("Nome", st.session_state.utente["nome"])
    st.session_state.utente["nome"] = nome

    st.selectbox("Locker Italia", LOCKER)

# =========================
# CARRELLO (STILE AMAZON)
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## 🛒 Carrello")

    totale = 0

    for i,item in enumerate(st.session_state.carrello):
        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"{item['nome']} - {item['prezzo']}€")

        with col2:
            if st.button("❌", key=i):
                remove_item(i)
                st.rerun()

        totale += item["prezzo"]

    st.markdown(f"### Totale: {totale}€")

    st.button("Procedi al pagamento (domani)")

# =========================
# INFO
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    1. Scegli Box  
    2. Ricevi al locker  
    3. Provi i capi  
    4. Cambi taglia quando cresce  
    5. Restituisci e ricevi nuova box  

    ♻️ Sistema circolare intelligente
    """)

# =========================
# CHI SIAMO
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori come te.

    LoopBaby nasce per:

    - ridurre sprechi  
    - far risparmiare famiglie  
    - creare moda circolare reale  

    Ogni capo ha una seconda vita.
    """)

# =========================
# CONTATTI (WHATSAPP CLICK)
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com
    """)

    if st.button("💬 Contattaci su WhatsApp"):
        whatsapp()
