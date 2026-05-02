import streamlit as st
import requests
from datetime import date

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

def register(email,password):
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
        "nome":"",
        "bimbo":"",
        "citta":"",
        "locker":"",
        "taglia":""
    }

def go(p): st.session_state.page = p

def add(name,price):
    st.session_state.cart.append({"n":name,"p":price})

def remove(i):
    st.session_state.cart.pop(i)

user = st.session_state.get("user",{})
nome = user.get("email","").split("@")[0]

# =========================
# LOGIN
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso",["Login","Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password",type="password")

    if mode=="Registrati":
        if st.button("Crea"):
            register(email,password)
            st.success("Creato!")

    if mode=="Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# LOGO ALLUNGATO HEADER
# =========================
st.markdown("""
<div style="text-align:center;margin-bottom:10px">
    <img src="logo.png" style="width:260px">
</div>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
col1,col2,col3,col4,col5 = st.columns(5)

if col1.button("🏠"): go("home")
if col2.button("📦"): go("box")
if col3.button("🔥"): go("info")
if col4.button("👤"): go("profile")
if col5.button(f"🛒 {len(st.session_state.cart)}"): go("cart")

# =========================
# HOME (COMPLETA COME VOLEVI)
# =========================
if st.session_state.page == "home":

    st.markdown(f"## Ciao {nome} 👋")

    colA,colB = st.columns([2,1])

    with colA:

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
Dona 10 capi → Box omaggio
</div>
""", unsafe_allow_html=True)

        if st.button("Partecipa alla Promo"):
            go("info")

    with colB:
        st.image("bimbo.jpg", use_container_width=True)

# =========================
# BOX (IDENTICHE AL TUO SISTEMA)
# =========================
elif st.session_state.page == "box":

    st.title("📦 Box LoopBaby")

    st.markdown("## STANDARD 14,90€ (spedizione inclusa)")

    standard = [
        ("SOLE ☀️","#FFD600","Colori vivaci"),
        ("LUNA 🌙","#E2E8F0","Neutro"),
        ("NUVOLA ☁️","#94A3B8","Toni soft")
    ]

    for name,color,desc in standard:

        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin:10px 0">
        <b>{name}</b><br>
        {desc}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            add(name,14.90)

    st.markdown("## 💎 PREMIUM 24,90€")

    st.markdown("""
<div style="background:#4F46E5;color:white;padding:15px;border-radius:15px">
<b>BOX PREMIUM</b><br>
Capi nuovi o seminuovi
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi Premium"):
        add("Premium Box",24.90)

# =========================
# INFO (COME FUNZIONA + PROMO)
# =========================
elif st.session_state.page == "info":

    st.title("🔄 Come funziona LoopBaby")

    st.markdown("""
### 1. Ricevi la Box
Scegli e ricevi nel locker.

### 2. Uso (90 giorni)
Usa la box per 3 mesi.

### 3. Dopo 90 giorni:
- nuova box (taglia successiva) → ritiro gratis  
- restituzione → 7,90€  

### 4. Regole 10 giorni:
- 48h per segnalare problemi  
- sostituzione jeans x jeans  
- oppure 5€  

---

## 🔥 Promo Mamme Fondatrici
Dona 10 capi → Box omaggio (etichetta entro 48h)
""")

    if st.button("Vai alla promo"):
        go("promo")

# =========================
# PROMO
# =========================
elif st.session_state.page == "promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.markdown("""
Compila per richiedere il ritiro gratuito.

Riceverai etichetta entro 48h.
""")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni")
    locker = st.text_input("Locker / Città")

    if st.button("Invia"):
        st.success("Richiesta inviata!")

# =========================
# VETRINA
# =========================
elif st.session_state.page == "vetrina":

    st.title("🛍️ Vetrina")

    st.markdown("""
I capi della vetrina rimangono per sempre a te.

- spedizione gratuita sopra 50€
- oppure con acquisto box
- altrimenti 7,90€
""")

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
            if st.button("❌",key=str(i)):
                remove(i)
                st.rerun()

        total += item["p"]

    st.markdown(f"## Totale: {total}€")

# =========================
# PROFILE
# =========================
elif st.session_state.page == "profile":

    st.title("👤 Profilo")

    nome = st.text_input("Nome genitore",st.session_state.profile["nome"])
    bimbo = st.text_input("Nome bambino",st.session_state.profile["bimbo"])
    citta = st.text_input("Città")

    locker = st.selectbox("Locker Italia",[
        "InPost",
        "Poste Italiane",
        "Amazon Locker"
    ])

    taglia = st.selectbox("Taglia",["50-56","62-68","74-80","86-92"])

    if st.button("Salva"):
        st.session_state.profile.update({
            "nome":nome,
            "bimbo":bimbo,
            "citta":citta,
            "locker":locker,
            "taglia":taglia
        })
        st.success("Profilo salvato")
