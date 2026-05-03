import streamlit as st
import os
import json
import base64

st.set_page_config(page_title="LoopBaby", layout="centered")

DB_FILE = "db.json"

# =========================
# IMMAGINI
# =========================
def load_img(path):
    if os.path.exists(path):
        return base64.b64encode(open(path,"rb").read()).decode()
    return ""

logo = load_img("logo.png")
baby = load_img("bimbo.jpg")

# =========================
# DB
# =========================
def load():
    if os.path.exists(DB_FILE):
        return json.load(open(DB_FILE))
    return {
        "nome":"", "email":"", "telefono":"",
        "bimbo":"", "taglia":"50-56",
        "paese":"Italia","citta":"","locker":""
    }

def save(d):
    json.dump(d, open(DB_FILE,"w"))

if "dati" not in st.session_state:
    st.session_state.dati = load()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

def go(p):
    st.session_state.page = p


# =========================
# LOCKER
# =========================
LOCKERS = {
    "Italia": {
        "Milano": ["Centrale","Porta Romana","Bicocca"],
        "Lecco": ["Calolziocorte","Lecco Centro"],
        "Roma": ["Termini","Tiburtina"],
        "Napoli": ["Centro","Vomero"],
        "Palermo": ["Centro"],
        "Catania": ["Centrale"],
        "Bergamo": ["Centro"],
        "Brescia": ["Centro"],
        "Torino": ["Porta Nuova"],
        "Firenze": ["SMN"],
        "Bari": ["Centro"],
        "Canicattì": ["Hub"],
        "Giffone": ["Reggio Calabria Locker"]
    }
}

def locker_ui():
    paese = st.selectbox("Paese", list(LOCKERS.keys()))
    citta = st.selectbox("Città", list(LOCKERS[paese].keys()))
    locker = st.selectbox("Locker", LOCKERS[paese][citta])
    return paese, citta, locker


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    if logo:
        st.image("logo.png", width=130)

    st.button("🏠 Home", on_click=lambda: go("Home"))
    st.button("📦 Box", on_click=lambda: go("Box"))
    st.button("🛍️ Vetrina", on_click=lambda: go("Vetrina"))
    st.button("ℹ️ Info", on_click=lambda: go("Info"))
    st.button("🔥 Promo", on_click=lambda: go("Promo"))
    st.button("👤 Profilo", on_click=lambda: go("Profilo"))
    st.button("🛒 Carrello", on_click=lambda: go("Carrello"))

    st.markdown("---")
    st.markdown("📞 WhatsApp: https://wa.me/393921404637")
    st.markdown("✉️ assistenza.loopbaby@gmail.com")


# =========================
# HEADER
# =========================
if logo:
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{logo}' width='180'></div>",
        unsafe_allow_html=True
    )


# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    d = st.session_state.dati
    nome = d.get("nome","")

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown(f"## Ciao {nome or '👋'}")

        st.markdown("""
**LoopBaby non è un e-commerce. È un sistema circolare.**

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
💛 risparmio reale  
""")

        st.markdown("""
### 👕 Capi tuoi per sempre

🚚 Spedizione:
- GRATIS sopra 50€
- GRATIS con abbinamento Box
- oppure 7,90€ spedizione standard
""")

    with col2:
        if baby:
            st.image("bimbo.jpg", use_container_width=True)

    st.markdown("### 🔥 Promo Mamme Fondatrici")
    st.markdown("Dona 10+ capi → Box omaggio")

    if st.button("Partecipa alla promo"):
        go("Promo")


# =========================
# PROMO
# =========================
if st.session_state.page == "Promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.markdown("""
## Cos’è
Un programma speciale per mamme fondatrici.

🎁 Doni 10 o più capi  
📦 Ricevi Box gratuita  
🚚 Spedizione inclusa  
""")

    st.markdown("""
## ♻️ Obiettivo LoopBaby
Ridurre sprechi tessili e creare economia circolare reale.
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")

    paese, citta, locker = locker_ui()

    if st.button("Invia richiesta"):
        st.success("✔ Etichetta inviata entro 48h")


# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("📦 Box LoopBaby")

    tipo = st.radio("Scegli", ["Standard","Premium"])

    if tipo == "Standard":

        st.markdown("### Standard 14,90€")

        boxes = [
            ("SOLE ☀️","#FFD600","colorati e vivaci"),
            ("LUNA 🌙","#E5E7EB","neutri soft"),
            ("NUVOLA ☁️","#94A3B8","delicati")
        ]

        for name,color,desc in boxes:
            st.markdown(f"""
            <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0">
                <b>{name}</b><br>
                {desc}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Aggiungi {name}"):
                st.session_state.cart.append({"name":name,"price":14.90})

    else:

        st.markdown("""
        <div style="background:#4F46E5;color:white;padding:15px;border-radius:15px">
        <b>BOX PREMIUM 💎</b><br>
        capi nuovi/semi-nuovi - 24,90€
        </div>
        """, unsafe_allow_html=True)

        if st.button("Aggiungi Premium"):
            st.session_state.cart.append({"name":"Premium Box","price":24.90})


# =========================
# INFO
# =========================
if st.session_state.page == "Info":

    st.title("ℹ️ Come funziona LoopBaby")

    st.markdown("""
♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  

---

## 📦 Sistema

📦 Ricevi Box  
👕 Usi i capi  
🔍 Controllo qualità

👉 Se qualcosa non va → <b>supporto immediato</b>  
👉 <a href='https://wa.me/393921404637' style='font-weight:bold;color:#f43f5e'>CONTATTACI SUBITO</a>

---

## ⏱ Utilizzo

Usi i capi per **massimo 90 giorni**, tempo reale di crescita del bambino.

Se il bambino cresce prima:
👉 <a href='https://wa.me/393921404637' style='font-weight:bold;color:#f43f5e'>CONTATTACI SUBITO</a>

---

## 🔔 10 giorni prima

Ti contattiamo noi:

- nuova Box (spedizione gratuita)
- restituzione
- oppure reso 7,90€

---

## 📍 Perché i locker

- libertà totale
- zero attese corriere
- ritiro quando vuoi
- meno emissioni CO₂

---

## ❤️ Chi siamo

LoopBaby nasce da genitori.

Non da un’azienda.

👉 È un sistema circolare, non un e-commerce.
""", unsafe_allow_html=True)


# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        c1,c2,c3 = st.columns([3,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")

        if c3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

        total += item["price"]

    st.markdown(f"### Totale: {total}€")


# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    d = st.session_state.dati

    st.title("👤 Profilo")

    st.markdown(f"### Ciao {d.get('nome','')} 👋")

    d["nome"] = st.text_input("Nome", d["nome"])
    d["email"] = st.text_input("Email", d["email"])
    d["telefono"] = st.text_input("Telefono", d["telefono"])
    d["bimbo"] = st.text_input("Bambino", d["bimbo"])

    d["paese"], d["citta"], d["locker"] = locker_ui()

    if st.button("Salva"):
        save(d)
        st.success("✔ Salvato")


# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
Capi tuoi per sempre.

🚚 gratis sopra 50€
""")

    if st.button("Aggiungi capo"):
        st.session_state.cart.append({"name":"Body","price":9.90})


# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📞 WhatsApp | ✉️ assistenza.loopbaby@gmail.com")
