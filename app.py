import streamlit as st
import webbrowser
import os
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# LOGO CENTRATO
# =========================
def b64(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = b64("logo.png")
bimbo = b64("bimbo.jpg")

st.markdown(f"""
<div style="text-align:center;">
    <img src="data:image/png;base64,{logo}" style="width:120px;">
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
        "nome_genitore": "",
        "telefono": "",
        "bambino": "",
        "locker": ""
    }

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
# MENU
# =========================
with st.sidebar:
    st.radio("Menu", ["Home","Box","Vetrina","Profilo","Carrello","Info","ChiSiamo","Contatti"], key="m")
    vai(st.session_state.m)

# =========================
# HOME (FIX + FOTO PICCOLA IN LINEA)
# =========================
if st.session_state.pagina == "Home":

    nome = st.session_state.user.get("nome_genitore","Mamma")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"### Ciao {nome} 👋")

        st.markdown("""
        LoopBaby è il sistema circolare per vestire bambini senza sprechi.

        👶 Qualità selezionata  
        🔄 Crescita continua  
        ♻️ Riutilizzo  
        💰 Risparmio reale  
        """)

    with col2:
        if bimbo:
            st.image("bimbo.jpg", width=120)

    st.markdown("""
    <div class="card">
    ✨ Inizia con la tua Box e attiva il ciclo LoopBaby
    </div>
    """, unsafe_allow_html=True)

    # PROMO FONDATRICI
    st.markdown("""
    <div class="card" style="background:#fff1f2;">
    <b>✨ Promo Mamme Fondatrici</b><br><br>
    Dona 10 capi in buono stato → ricevi Box omaggio + trasporto gratuito<br><br>
    🚚 Ritiro pagato da noi
    </div>
    """, unsafe_allow_html=True)

# =========================
# BOX (3 STANDARD + 1 PREMIUM COME HAI CHIESTO)
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## 📦 Scegli la tua Box")

    # STANDARD 3 OPZIONI
    st.markdown("### STANDARD (14,90€ spedizione inclusa)")

    standard = [
        ("LUNA 🌙","Neutro, delicato"),
        ("SOLE ☀️","Colorato, vivace"),
        ("NUVOLA ☁️","Toni soft")
    ]

    for n,desc in standard:
        with st.expander(n):
            st.write(desc)
            st.image("https://via.placeholder.com/300x200.png?text="+n)
            if st.button(f"Scegli {n}"):
                add("Box Standard - "+n, 14.90)

    # PREMIUM
    st.markdown("### 💎 PREMIUM (24,90€)")

    with st.expander("BOX PREMIUM"):
        st.write("Vestiti nuovi o seminuovi selezionati")
        st.image("https://via.placeholder.com/300x200.png?text=Premium")
        if st.button("Scegli Premium"):
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
# PROFILO (FIX COMPLETO)
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## 👤 Profilo")

    u = st.session_state.user

    u["nome_genitore"] = st.text_input("Nome", u.get("nome_genitore",""))
    u["telefono"] = st.text_input("Telefono", u.get("telefono",""))
    u["bambino"] = st.text_input("Nome Bambino", u.get("bambino",""))

    u["locker"] = st.selectbox("Locker Italia", [
        "InPost Italia","Poste Italiane","Amazon Locker",
        "Milano","Roma","Torino","Napoli","Calolziocorte","Tutta Italia"
    ])

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

    st.button("Procedi al pagamento (attivo domani)")

# =========================
# INFO (COMPLETO SERIO)
# =========================
elif st.session_state.pagina == "Info":

    st.markdown("## 🔄 Come funziona LoopBaby")

    st.markdown("""
    LoopBaby è un sistema circolare per vestire i bambini senza sprechi.

    ### 📦 Il ciclo:

    1. Scegli la tua Box  
    2. Ricevi al locker  
    3. Hai 90 giorni di utilizzo  
    4. Dopo 90 giorni scegli:
       - nuova Box (taglia successiva)
       - oppure restituzione  

    ### ⏱️ Controllo qualità:

    Nei primi **10 giorni** dal ricevimento:
    - puoi segnalare problemi
    - verrai contattato dal nostro team  

    ### ♻️ Patto del 10:

    - restituisci 10 capi
    - ricevi la Box successiva  
    - se manca un capo → sostituzione o 5€

    LoopBaby è un sistema circolare reale, non uno shop tradizionale.
    """)

# =========================
# CHI SIAMO (VERSIONE BRAND SERIA)
# =========================
elif st.session_state.pagina == "ChiSiamo":

    st.markdown("## ❤️ Chi siamo")

    st.markdown("""
    Siamo genitori.

    E abbiamo vissuto lo stesso problema di tutti:

    👶 I bambini crescono troppo in fretta  
    💸 I vestiti costano troppo  
    🌍 Si spreca troppo  

    ### 💡 Da qui nasce LoopBaby

    Un sistema pensato non come un e-commerce, ma come un **ciclo intelligente**:

    - i vestiti non si buttano  
    - i vestiti non si accumulano  
    - i vestiti circolano  

    ### 🎯 La nostra missione:

    Rendere l’abbigliamento bambino:
    - sostenibile  
    - economico  
    - senza sprechi  

    ### 🌍 Visione:

    Un guardaroba globale condiviso tra famiglie.

    LoopBaby non è un negozio.  
    È un sistema.
    """)

# =========================
# CONTATTI (WHATSAPP FIX)
# =========================
elif st.session_state.pagina == "Contatti":

    st.markdown("## 📞 Contatti")

    st.markdown("""
    📧 assistenza.loopbaby@gmail.com  
    """)

    st.markdown("📱 WhatsApp: 392 140 4637")

    if st.button("Apri WhatsApp"):
        whatsapp()
