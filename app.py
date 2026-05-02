import streamlit as st
import requests
import base64
import json
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"
DB_FILE = "db_loopbaby.json"

# =========================
# AUTH
# =========================
def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower() and u.get("password") == password:
                st.session_state.user = u
                return True
    except:
        pass
    return False

def register(email, password):
    requests.post(SHEETDB_URL, json={"data":[{"email":email,"password":password}]})

# =========================
# STATE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "nome": "",
        "bimbo": "",
        "citta": "",
        "locker": "",
        "taglia": ""
    }

def go(p): st.session_state.page = p

def add_cart(name, price):
    st.session_state.cart.append({"name": name, "price": price})

def remove_cart(i):
    st.session_state.cart.pop(i)

# =========================
# LOGIN
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            register(email, password)
            st.success("Creato!")

    if mode == "Login":
        if st.button("Entra"):
            if login(email, password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# HEADER LOGO (SOLO LOGO CENTRATO ALLUNGATO)
# =========================
st.markdown("""
<div style="text-align:center;margin:10px 0 20px 0">
    <img src="logo.png" style="width:260px; max-width:80%;">
</div>
""", unsafe_allow_html=True)

# =========================
# NAVBAR (STILE APP)
# =========================
c1,c2,c3,c4,c5 = st.columns(5)

if c1.button("🏠"): go("home")
if c2.button("📦"): go("box")
if c3.button("🔥"): go("info")
if c4.button("👤"): go("profile")
if c5.button(f"🛒 {len(st.session_state.cart)}"): go("cart")

# =========================
# HOME (VERA, NON ROTTA)
# =========================
if st.session_state.page == "home":

    user = st.session_state.get("user", {})
    name = user.get("email","").split("@")[0]

    st.markdown(f"## Ciao {name} 👋")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
### LoopBaby non è un e-commerce.

È uno stile. Una scelta. Un sistema.

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
💛 moda che cresce con il bambino  

---

<div style="background:#fff0f3;padding:15px;border-radius:15px">
<b>🔥 Promo Mamme Fondatrici</b><br>
Dona 10 capi → Box omaggio (etichetta entro 48h)
</div>
""", unsafe_allow_html=True)

        if st.button("Vai alla Promo"):
            go("info")

    with col2:
        st.image("bimbo.jpg", use_container_width=True)

# =========================
# BOX (TUO SISTEMA ORIGINALE MIGLIORATO MA IDENTICO LOGICA)
# =========================
elif st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    st.markdown("## STANDARD — 14,90€ (spedizione inclusa)")

    standard = [
        ("SOLE ☀️", "#FFD600", "Colori vivaci"),
        ("LUNA 🌙", "#E5E7EB", "Neutro"),
        ("NUVOLA ☁️", "#94A3B8", "Soft")
    ]

    for name, color, desc in standard:

        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0">
        <b>{name}</b><br>{desc}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            add_cart(name, 14.90)

    st.markdown("## 💎 PREMIUM — 24,90€")

    st.markdown("""
<div style="background:#4F46E5;color:white;padding:15px;border-radius:15px">
<b>BOX PREMIUM</b><br>
Capi nuovi o seminuovi
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi Premium"):
        add_cart("Box Premium", 24.90)

# =========================
# INFO (COMPLETA + BUSINESS READY)
# =========================
elif st.session_state.page == "info":

    st.title("🔄 Come funziona LoopBaby")

    st.markdown("""
### 1. Scegli la Box
Ricevi nel locker.

### 2. Usa per 90 giorni
Crescita del bambino = cambio taglia.

### 3. Dopo 90 giorni:
- nuova box → ritiro gratis  
- restituzione → 7,90€  

### 4. Regole 10 giorni:
- 48h segnalazioni  
- jeans x jeans  
- oppure 5€  

---

## 🔥 Promo Mamme Fondatrici
Dona 10 capi → Box omaggio
""")

# =========================
# PROMO
# =========================
elif st.session_state.page == "promo":

    st.title("🔥 Promo Mamme Fondatrici")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")
    city = st.text_input("Città / Locker")

    if st.button("Invia richiesta"):
        st.success("Entro 48h ricevi etichetta")

# =========================
# VETRINA
# =========================
elif st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
✔ capi tuoi per sempre  
✔ spedizione 7,90€ se <50€  
✔ gratis con box o sopra 50€
""")

# =========================
# CART (AMAZON STYLE BASIC)
# =========================
elif st.session_state.page == "cart":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["name"], "-", item["price"], "€")

        with c2:
            if st.button("❌", key=i):
                remove_cart(i)
                st.rerun()

        total += item["price"]

    st.markdown(f"## Totale: {total}€")

# =========================
# PROFILE (FIXATO SERIO)
# =========================
elif st.session_state.page == "profile":

    st.title("👤 Profilo")

    st.session_state.profile["nome"] = st.text_input("Nome genitore")
    st.session_state.profile["bimbo"] = st.text_input("Nome bambino")
    st.session_state.profile["citta"] = st.text_input("Città")

    st.session_state.profile["locker"] = st.selectbox(
        "Locker Italia",
        ["InPost", "Poste Italiane", "Amazon Locker"]
    )

    st.session_state.profile["taglia"] = st.selectbox(
        "Taglia",
        ["50-56", "62-68", "74-80", "86-92"]
    )

    if st.button("Salva profilo"):
        st.success("Salvato")

# =========================
# CONTATTI READY (DOMANI WHATSAPP + EMAIL STRIPE READY)
# =========================
elif st.session_state.page == "contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 3921404637 (WhatsApp)")
