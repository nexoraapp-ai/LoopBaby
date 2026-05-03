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


# =========================
# LOGIN SYSTEM
# =========================
def login(email, password):
    res = requests.get(API_URL)
    for u in res.json():
        if u.get("email") == email and u.get("password") == password:
            st.session_state.user = u
            return True
    return False


def register(data):
    check = requests.get(API_URL, params={"email": data["email"]})
    if len(check.json()) > 0:
        return False

    requests.post(API_URL, json={"data": data})
    return True


def reset_password(email, new_pass):
    requests.patch(API_URL, json={
        "data": {"password": new_pass},
        "query": {"email": email}
    })


# =========================
# BLOCCO LOGIN OBBLIGATORIO
# =========================
if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati", "Reset Password"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # LOGIN
    if mode == "Login":
        if st.button("Accedi"):
            if login(email, password):
                st.session_state.auth = True
                st.success("Login effettuato")
                st.rerun()
            else:
                st.error("Credenziali errate")

    # REGISTRAZIONE (UNA SOLA VOLTA)
    if mode == "Registrati":

        nome = st.text_input("Nome")
        telefono = st.text_input("Telefono")

        if st.button("Registrati"):
            data = {
                "nome": nome,
                "email": email,
                "telefono": telefono,
                "password": password
            }

            if register(data):
                st.success("Account creato")
            else:
                st.error("Email già registrata")

    # RESET PASSWORD
    if mode == "Reset Password":
        new_pass = st.text_input("Nuova password", type="password")

        if st.button("Reset"):
            reset_password(email, new_pass)
            st.success("Password aggiornata")

    st.stop()


# =========================
# UI NEUTRA
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F8F8F8;
    max-width: 500px;
    margin: auto;
}

div.stButton > button {
    background-color: black;
    color: white;
    border-radius: 12px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.button("Home", on_click=lambda: go("Home"))
    st.button("Box", on_click=lambda: go("Box"))
    st.button("Vetrina", on_click=lambda: go("Vetrina"))
    st.button("Carrello", on_click=lambda: go("Carrello"))
    st.button("Profilo", on_click=lambda: go("Profilo"))
    st.button("Info", on_click=lambda: go("Info"))


# =========================
# HOME
# =========================
if st.session_state.page == "Home":

    nome = st.session_state.user.get("nome", "")

    st.title(f"Ciao {nome} 👋" if nome else "Benvenuto 👋")

    st.write("LoopBaby è un sistema circolare per bambini ♻️")

    st.markdown("🔥 Promo: dona 10 capi → box gratis")


# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box")

    if st.button("Box Standard - 14.90€"):
        st.session_state.cart.append({"name": "Box", "price": 14.90})


# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    st.write("I capi qui restano tuoi per sempre")

    if st.button("Body 9.90€"):
        st.session_state.cart.append({"name": "Body", "price": 9.90})


# =========================
# CARRELLO + SPEDIZIONE
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    totale = sum(i["price"] for i in st.session_state.cart)

    has_box = any("Box" in i["name"] for i in st.session_state.cart)

    spedizione = 0
    if totale < 50 and not has_box:
        spedizione = 7.90

    totale_finale = totale + spedizione

    for item in st.session_state.cart:
        st.write(item["name"], item["price"])

    st.markdown(f"Totale: {totale}€")
    st.markdown(f"Spedizione: {spedizione}€")
    st.markdown(f"Totale finale: {totale_finale}€")


# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo")

    st.write(st.session_state.user)


# =========================
# INFO + CHI SIAMO
# =========================
if st.session_state.page == "Info":

    st.title("Info + Chi siamo")

    st.write("""
LoopBaby è nato da genitori.

Obiettivo:
- risparmio reale
- meno sprechi
- sistema circolare
""")
