import streamlit as st
import requests

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
        "locker":"",
        "taglia":""
    }

def go(p): st.session_state.page = p

def add(name, price):
    st.session_state.cart.append({"name":name,"price":price})

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
        if st.button("Crea"):
            register(email,password)
            st.success("Creato!")

    if mode == "Login":
        if st.button("Entra"):
            if login(email,password):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# HEADER (LOGO COME VOLEVI)
# =========================
st.markdown("""
<div style="text-align:center;margin-bottom:10px">
    <img src="logo.png" style="width:180px">
</div>
""", unsafe_allow_html=True)

# =========================
# NAVBAR (APP STYLE)
# =========================
col1,col2,col3,col4 = st.columns(4)

if col1.button("🏠"): go("home")
if col2.button("📦"): go("box")
if col3.button("🔥"): go("promo")
if col4.button(f"🛒 {len(st.session_state.cart)}"): go("cart")

# =========================
# HOME (TUO DESIGN MIGLIORATO)
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
💛 moda consapevole per bambini  
""")

        st.markdown("""
<div style="background:#fff0f3;padding:15px;border-radius:15px">
<b>🔥 Promo Mamme Fondatrici</b><br>
Dona 10 capi → Box omaggio
</div>
""", unsafe_allow_html=True)

        if st.button("Partecipa"):
            go("promo")

    with colB:
        st.image("bimbo.jpg", use_container_width=True)

# =========================
# BOX (TUO SISTEMA ORIGINALE)
# =========================
elif st.session_state.page == "box":

    st.title("📦 Box")

    st.markdown("## Standard 14,90€ (spedizione inclusa)")

    box_standard = [
        ("SOLE ☀️","#FFD600","Colori vivaci"),
        ("LUNA 🌙","#E2E8F0","Neutro elegante"),
        ("NUVOLA ☁️","#94A3B8","Toni soft")
    ]

    for name,color,desc in box_standard:

        st.markdown(f"""
        <div style="background:{color};padding:15px;border-radius:15px;margin-bottom:10px">
        <b>{name}</b><br>
        {desc}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Aggiungi {name}"):
            add(name,14.90)

    st.markdown("## 💎 Premium 24,90€")

    st.markdown("""
<div style="background:#4F46E5;color:white;padding:15px;border-radius:15px">
<b>BOX PREMIUM</b><br>
Capi nuovi o seminuovi selezionati
</div>
""", unsafe_allow_html=True)

    if st.button("Aggiungi Premium"):
        add("Premium Box",24.90)

# =========================
# PROMO MAMME FONDATRICI
# =========================
elif st.session_state.page == "promo":

    st.title("🔥 Promo Mamme Fondatrici")

    st.markdown("""
### Cos'è:
Un programma speciale per le prime mamme della community.

### Come funziona:
- 10 capi in buono stato
- ritiro gratuito
- ricevi Box omaggio
- etichetta entro 48h
""")

    peso = st.text_input("Peso stimato")
    dim = st.text_input("Dimensioni pacco")

    if st.button("Invia"):
        st.success("Entro 48h riceverai etichetta via email")

# =========================
# CART (AMAZON STYLE BASE)
# =========================
elif st.session_state.page == "cart":

    st.title("🛒 Carrello")

    total = 0

    for i,item in enumerate(st.session_state.cart):

        c1,c2 = st.columns([3,1])

        with c1:
            st.write(item["name"], "-", item["price"], "€")

        with c2:
            if st.button("❌", key=str(i)):
                remove(i)
                st.rerun()

        total += item["price"]

    st.markdown(f"## Totale: {total}€")

# =========================
# PROFILO (SISTEMATO)
# =========================
elif st.session_state.page == "profile":

    st.title("👤 Profilo")

    nome_p = st.text_input("Nome genitore", st.session_state.profile["nome"])
    bimbo = st.text_input("Nome bambino", st.session_state.profile["bimbo"])

    st.session_state.profile["locker"] = st.selectbox(
        "Locker Italia",
        ["InPost", "Poste Italiane", "Amazon Locker", "SDA Point"]
    )

    st.session_state.profile["taglia"] = st.selectbox(
        "Taglia",
        ["50-56","62-68","74-80","86-92"]
    )

    if st.button("Salva"):
        st.session_state.profile["nome"] = nome_p
        st.session_state.profile["bimbo"] = bimbo
        st.success("Profilo aggiornato")
