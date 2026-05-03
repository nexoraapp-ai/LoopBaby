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
# DB FUNCTIONS (FIXED)
# =========================
def get_all_users():
    try:
        return requests.get(API_URL).json()
    except:
        return []

def get_user(email):
    for u in get_all_users():
        if u.get("email","").lower() == email.lower():
            return u
    return None

def create_user(data):
    if get_user(data["email"]):
        return False
    requests.post(API_URL, json={"data": data})
    return True

def update_user(email, new_data):
    requests.patch(API_URL, json={
        "data": new_data,
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
        citta = st.text_input("Città")

        if st.button("Crea account"):
            if not email or not password:
                st.error("Email e password obbligatorie")
            else:
                data = {
                    "email": email,
                    "password": password,
                    "nome": nome,
                    "telefono": telefono,
                    "bambino": bambino,
                    "citta": citta
                }
                if create_user(data):
                    st.success("Account creato ✅")
                else:
                    st.error("Email già registrata")

    if mode == "Reset Password":
        new_pass = st.text_input("Nuova password", type="password")
        if st.button("Aggiorna"):
            if get_user(email):
                update_user(email, {"password": new_pass})
                st.success("Password aggiornata")
            else:
                st.error("Email non trovata")

    st.stop()

# =========================
# DESIGN
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #FDFBF7;
    max-width: 480px;
    margin: auto;
}
div.stButton > button {
    background-color: #f43f5e;
    color: white;
    border-radius: 14px;
    font-weight: bold;
    width: 100%;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 18px;
    margin: 10px 0;
    border: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (HAMBURGER)
# =========================
with st.sidebar:
    st.title("☰ Menu")
    if st.button("🏠 Home"): go("Home")
    if st.button("📦 Box"): go("Box")
    if st.button("🛍️ Vetrina"): go("Vetrina")
    if st.button("📖 Info"): go("Info")
    if st.button("🛒 Carrello"): go("Carrello")
    if st.button("👤 Profilo"): go("Profilo")

# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    nome = st.session_state.user.get("nome","")

    st.title(f"Ciao {nome} 👋")

    st.markdown("""
LoopBaby non è un e-commerce. È un sistema.

♻️ crescita circolare  
👶 bambini al centro  
🔄 riuso intelligente  
💛 risparmio reale  
""")

    st.markdown('<div class="card">🔥 Promo Mamme Fondatrici → Dona 10 capi e ricevi BOX GRATIS</div>', unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Scegli la tua Box")

    for name, price in [
        ("🌙 LUNA", 19.90),
        ("☀️ SOLE", 19.90),
        ("☁️ NUVOLA", 19.90),
        ("💎 PREMIUM", 29.90)
    ]:
        st.markdown(f'<div class="card">{name} - {price}€</div>', unsafe_allow_html=True)
        if st.button(f"Aggiungi {name}"):
            st.session_state.cart.append({"name": name, "price": price})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.write("I capi qui restano tuoi per sempre")

    prodotti = [
        ("Body", 9.90),
        ("Maglietta", 8.90),
        ("Pantaloni", 12.90)
    ]

    for p, prezzo in prodotti:
        st.markdown(f'<div class="card">{p} - {prezzo}€</div>', unsafe_allow_html=True)
        if st.button(f"Aggiungi {p}"):
            st.session_state.cart.append({"name": p, "price": prezzo})

# =========================
# INFO + CHI SIAMO
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona")

    st.markdown("""
1. Scegli una Box  
2. Usala fino a 3 mesi  
3. Cambia quando cresce  
4. Riduci sprechi  
""")

    st.markdown("## Chi siamo ❤️")

    st.write("""
Siamo genitori.

LoopBaby nasce per semplificare la vita e ridurre gli sprechi.

💡 Obiettivo:
- risparmiare oltre 1000€
- meno spreco
- sistema circolare
""")

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
        c1,c2,c3 = st.columns([2,1,1])
        c1.write(item["name"])
        c2.write(f"{item['price']}€")
        if c3.button("❌", key=i):
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

    nome = st.text_input("Nome", u.get("nome",""))
    telefono = st.text_input("Telefono", u.get("telefono",""))
    bambino = st.text_input("Bambino", u.get("bambino",""))
    citta = st.text_input("Città", u.get("citta",""))

    if st.button("Salva"):
        new_data = {
            "nome": nome,
            "telefono": telefono,
            "bambino": bambino,
            "citta": citta
        }
        update_user(u["email"], new_data)
        st.session_state.user.update(new_data)
        st.success("Profilo aggiornato")
