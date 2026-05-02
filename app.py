import streamlit as st
import requests
import json

st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

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

def registra(email, password):
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

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "nome_genitore":"",
        "bimbo":"",
        "locker":"",
        "taglia":""
    }

def go(p): st.session_state.page = p

def add(name, price):
    st.session_state.cart.append({"n":name,"p":price})

def remove(i):
    st.session_state.cart.pop(i)

user = st.session_state.get("user", {})
nome = user.get("email","").split("@")[0]

# =========================
# LOGIN
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login","Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":
        if st.button("Crea account"):
            registra(email,password)
            st.success("Creato!")

    if mode == "Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore")

    st.stop()

# =========================
# HEADER LOGO
# =========================
st.markdown("""
<div style='text-align:center;padding:10px'>
    <img src='logo.png' width='160'>
</div>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown(f"""
<div style='display:flex;justify-content:space-around;background:#fff;
padding:10px;border-radius:15px;box-shadow:0 2px 10px #00000010;margin-bottom:10px'>

<button onclick="">Home</button>
<button onclick="">Box</button>
<button onclick="">Promo</button>
<button onclick="">Carrello ({len(st.session_state.cart)})</button>

</div>
""", unsafe_allow_html=True)

# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown(f"### Ciao {nome} 👋")

    col1,col2 = st.columns([2,1])

    with col1:
        st.markdown("""
### LoopBaby non è un e-commerce.

È uno stile. Una scelta. Un sistema.

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  

---

### 🔥 Promo Mamme Fondatrici
Dona 10 capi → Box omaggio
""")

    with col2:
        st.image("bimbo.jpg", width=150)

    if st.button("Scopri Box"):
        go("box")

# =========================
# BOX
# =========================
elif st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    st.markdown("## Standard 14,90€ (spedizione inclusa)")

    standard = [
        ("SOLE ☀️","#FFD600"),
        ("LUNA 🌙","#E2E8F0"),
        ("NUVOLA ☁️","#94A3B8")
    ]

    for name,color in standard:
        st.markdown(f"""
        <div style='background:{color};padding:15px;border-radius:15px;margin-bottom:10px'>
        <b>{name}</b><br>
        Capo selezionato in base alla box
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            add(name,14.90)

    st.markdown("## 💎 Premium 24,90€")

    st.markdown("""
<div style='background:#4F46E5;color:white;padding:15px;border-radius:15px'>
<b>Box Premium</b><br>
Capi nuovi o seminuovi selezionati
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi Premium"):
        add("Premium Box",24.90)

# =========================
# PROMO
# =========================
elif st.session_state.page == "promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.markdown("""
### Come funziona:
- Dona almeno 10 capi
- Noi paghiamo il trasporto
- Ricevi Box gratuita

⏱ Entro 48h ricevi etichetta
""")

    peso = st.text_input("Peso stimato")
    dim = st.text_input("Dimensioni pacco")

    if st.button("Invia richiesta"):
        st.success("Ricevuto! Ti contatteremo via email entro 48h")

# =========================
# CART
# =========================
elif st.session_state.page == "cart":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):
        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["n"], item["p"], "€")

        with c2:
            if st.button("❌", key=str(i)):
                remove(i)
                st.rerun()

        total += item["p"]

    st.markdown(f"## Totale: {total}€")

# =========================
# PROFILO
# =========================
elif st.session_state.page == "profile":

    st.title("👤 Profilo")

    st.write("Email:", user.get("email",""))

    nome_g = st.text_input("Nome genitore", st.session_state.user_data["nome_genitore"])
    bimbo = st.text_input("Nome bimbo", st.session_state.user_data["bimbo"])

    paese = st.text_input("Città / Paese")

    locker = st.selectbox("Locker disponibili", [
        "InPost Italia",
        "Poste Italiane",
        "Amazon Locker",
        "SDA Point"
    ])

    if st.button("Salva"):
        st.session_state.user_data.update({
            "nome_genitore":nome_g,
            "bimbo":bimbo,
            "locker":locker
        })
        st.success("Salvato")
