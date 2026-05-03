import streamlit as st
import requests
from datetime import date

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
# DB FUNCTIONS (GOOGLE SHEET)
# =========================
def get_user(email):
    try:
        r = requests.get(API_URL, params={"email": email})
        if r.status_code == 200 and len(r.json()) > 0:
            return r.json()[0]
    except:
        pass
    return None

def create_user(data):
    if get_user(data["email"]):
        return False
    requests.post(API_URL, json={"data": data})
    return True

def update_user(email, data):
    requests.patch(API_URL, json={
        "data": data,
        "query": {"email": email}
    })

# =========================
# LOGIN SYSTEM
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati", "Reset Password"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Accedi"):
            u = get_user(email)
            if u and u.get("password") == password:
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Credenziali errate")

    if mode == "Registrati":

        nome = st.text_input("Nome")
        telefono = st.text_input("Telefono")
        bambino = st.text_input("Nome bambino")

        paese = st.selectbox("Paese", ["Italia"])
        citta = st.text_input("Città")
        locker = st.text_input("Locker")

        if st.button("Crea account"):
            data = {
                "email": email,
                "password": password,
                "nome": nome,
                "telefono": telefono,
                "bambino": bambino,
                "paese": paese,
                "citta": citta,
                "locker": locker
            }

            if create_user(data):
                st.success("Account creato ✅")
            else:
                st.error("Email già registrata")

    if mode == "Reset Password":
        new_pass = st.text_input("Nuova password", type="password")

        if st.button("Aggiorna"):
            update_user(email, {"password": new_pass})
            st.success("Password aggiornata")

    st.stop()

# =========================
# DESIGN UI (UGUALE PER TUTTO)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #FDFBF7;
    max-width: 480px;
    margin: auto;
    font-family: sans-serif;
}

h1,h2,h3 {
    text-align:center;
}

div.stButton > button {
    background-color: #f43f5e;
    color: white;
    border-radius: 16px;
    font-weight: bold;
    width: 100%;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 20px;
    margin: 10px 0;
    border: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
c = st.columns(5)

menu = ["Home", "Box", "Vetrina", "Carrello", "Profilo"]

for i, m in enumerate(menu):
    if c[i].button(m):
        go(m)

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    nome = st.session_state.user.get("nome", "")

    st.title(f"Ciao {nome} 👋")

    st.markdown("""
LoopBaby è un sistema circolare ♻️

👶 vestiti che crescono con il bambino  
🔄 riuso intelligente  
💰 risparmio reale  
""")

    st.markdown("""
<div class="card">
🔥 <b>Promo Mamme Fondatrici</b><br>
Dona 10 capi → Box GRATIS
</div>
""", unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Scegli la Box")

    if st.button("🌙 LUNA - 19,90€"):
        st.session_state.cart.append({"name": "Box LUNA", "price": 19.90})

    if st.button("☀️ SOLE - 19,90€"):
        st.session_state.cart.append({"name": "Box SOLE", "price": 19.90})

    if st.button("☁️ NUVOLA - 19,90€"):
        st.session_state.cart.append({"name": "Box NUVOLA", "price": 19.90})

    if st.button("💎 PREMIUM - 29,90€"):
        st.session_state.cart.append({"name": "Box PREMIUM", "price": 29.90})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.write("I capi acquistati qui restano tuoi")

    st.markdown('<div class="card">Body 9,90€</div>', unsafe_allow_html=True)

    if st.button("Aggiungi Body"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    totale = sum(i["price"] for i in st.session_state.cart)

    has_box = any("Box" in i["name"] for i in st.session_state.cart)

    spedizione = 0
    if totale < 50 and not has_box:
        spedizione = 7.90

    totale_finale = totale + spedizione

    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([2,1,1])

        col1.write(item["name"])
        col2.write(f"{item['price']}€")

        if col3.button("❌", key=i):
            st.session_state.cart.pop(i)
            st.rerun()

    st.markdown(f"Totale: {totale}€")
    st.markdown(f"Spedizione: {spedizione}€")
    st.markdown(f"Totale finale: {totale_finale}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo")

    u = st.session_state.user

    nome = st.text_input("Nome", u.get("nome", ""))
    telefono = st.text_input("Telefono", u.get("telefono", ""))
    bambino = st.text_input("Bambino", u.get("bambino", ""))
    citta = st.text_input("Città", u.get("citta", ""))
    locker = st.text_input("Locker", u.get("locker", ""))

    if st.button("Salva"):
        new_data = {
            "nome": nome,
            "telefono": telefono,
            "bambino": bambino,
            "citta": citta,
            "locker": locker
        }

        update_user(u["email"], new_data)
        st.session_state.user.update(new_data)

        st.success("Aggiornato")
