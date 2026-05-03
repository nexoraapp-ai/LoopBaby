import streamlit as st
import requests

API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

st.set_page_config(page_title="LoopBaby", layout="centered")

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = {}
if "cart" not in st.session_state:
    st.session_state.cart = []
if "page" not in st.session_state:
    st.session_state.page = "Home"

def go(p):
    st.session_state.page = p
    st.rerun()

# =========================
# DB FUNCTIONS
# =========================
def get_users():
    try:
        return requests.get(API_URL).json()
    except:
        return []

def find_user(email):
    for u in get_users():
        if u.get("email","").lower() == email.lower():
            return u
    return None

def create_user(data):
    users = get_users()

    for u in users:
        if u.get("email","").lower() == data["email"].lower():
            return False  # già registrata

    data["fondatrice"] = "SI" if len(users) < 100 else "NO"
    data["locker"] = ""

    requests.post(API_URL, json={"data": data})
    return True

def update_user(email, data):
    requests.patch(API_URL, json={
        "data": data,
        "query": {"email": email}
    })

# =========================
# LOGIN / REGISTER
# =========================
if not st.session_state.auth:

    st.markdown("""
    <div style='text-align:center'>
        <h1 style='color:#5a4636'>🌸 LoopBaby</h1>
        <p style='color:#a38f7b'>Crescita circolare per bambini</p>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login", "Registrati", "Password dimenticata"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # LOGIN
    if mode == "Login":
        if st.button("Entra"):
            u = find_user(email)
            if u and u.get("password") == password:
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Credenziali errate")

    # REGISTER
    if mode == "Registrati":
        nome = st.text_input("Nome e Cognome")
        telefono = st.text_input("Telefono")
        bambino = st.text_input("Nome bambino")
        citta = st.text_input("Città")

        if st.button("Crea account"):
            ok = create_user({
                "email": email,
                "password": password,
                "nome": nome,
                "telefono": telefono,
                "bambino": bambino,
                "citta": citta
            })

            if ok:
                st.success("Account creato")
            else:
                st.error("Questa email è già registrata")

    # RESET PASSWORD
    if mode == "Password dimenticata":
        newp = st.text_input("Nuova password", type="password")

        if st.button("Aggiorna"):
            if find_user(email):
                update_user(email, {"password": newp})
                st.success("Password aggiornata")
            else:
                st.error("Email non trovata")

    st.stop()

# =========================
# DESIGN SYSTEM
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
}

div.stButton > button{
    background:#f4b400;
    color:black;
    border-radius:14px;
    width:100%;
    font-weight:bold;
    border:none;
}

.card{
    background:#fffdf8;
    padding:14px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #eadfcd;
}

.header{
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#5a4636;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
with st.sidebar:
    st.title("☰ Menu")
    if st.button("Home"): go("Home")
    if st.button("Box"): go("Box")
    if st.button("Vetrina"): go("Vetrina")
    if st.button("Info"): go("Info")
    if st.button("Chi Siamo"): go("ChiSiamo")
    if st.button("Carrello"): go("Carrello")
    if st.button("Profilo"): go("Profilo")

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    u = st.session_state.user
    nome = u.get("nome","")
    fond = u.get("fondatrice","NO")

    st.markdown("<div class='header'>🌸 LoopBaby</div>", unsafe_allow_html=True)

    st.title(f"Ciao {nome} 👋")

    if fond == "SI":
        st.success("🌸 Mamma Fondatrice")

    st.markdown("""
✔ crescita circolare  
✔ bambini al centro  
✔ risparmio reale  
✔ riuso intelligente  
""")

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box LoopBaby")

    st.markdown("💛 Standard 14,90€")

    for n in ["LUNA 🌙","SOLE ☀️","NUVOLA ☁️"]:
        st.markdown(f"<div class='card'>{n}</div>", unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": 14.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina 🛍️")

    st.markdown("""
💛 Questi capi rimangono a te per sempre  
🚚 Spedizione semplice e trasparente
""")

    for n,p in [("Body",9.9),("Maglia",8.9),("Pantaloni",12.9)]:
        st.markdown(f"<div class='card'>{n} - {p}€</div>", unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": p})

# =========================
# INFO (SPEDIZIONE CHIARA)
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona 🚚")

    st.markdown("""
1. Ricevi Box GRATIS andata  
2. Usi i capi  
3. Dopo 90 giorni puoi:
   - continuare → ritorno GRATIS  
   - fermarti → 7,90€ per reso etichetta  
""")

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "ChiSiamo":

    st.title("Chi siamo ❤️")

    st.markdown("""
Siamo genitori come te.

Abbiamo creato LoopBaby per:

✔ ridurre sprechi  
✔ far risparmiare famiglie  
✔ semplificare la crescita dei bambini  

Non è un e-commerce.  
È un sistema circolare.
""")

# =========================
# CARRELLO (CON RIMOZIONE)
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello 🛒")

    for i,item in enumerate(st.session_state.cart):
        col1,col2,col3 = st.columns([3,1,1])
        col1.write(item["name"])
        col2.write(f"{item['price']}€")
        if col3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

    tot = sum(i["price"] for i in st.session_state.cart)
    st.markdown(f"**Totale:** {tot}€")

# =========================
# PROFILO COMPLETO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo 👤")

    u = st.session_state.user

    nome = st.text_input("Nome", u.get("nome",""))
    tel = st.text_input("Telefono", u.get("telefono",""))
    citta = st.text_input("Città", u.get("citta",""))
    bambino = st.text_input("Bambino", u.get("bambino",""))

    if st.button("Salva"):
        update_user(u["email"], {
            "nome": nome,
            "telefono": tel,
            "citta": citta,
            "bambino": bambino
        })
        st.success("Profilo aggiornato")
