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
# DB
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
            return False

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
# LOGIN
# =========================
if not st.session_state.auth:

    st.markdown("<h1 style='text-align:center;color:#5a4636'>🌸 LoopBaby</h1>", unsafe_allow_html=True)

    mode = st.radio("Accesso", ["Login", "Registrati", "Reset Password"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Entra"):
            u = find_user(email)
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
                st.error("Email già registrata")

    if mode == "Reset Password":
        newp = st.text_input("Nuova password", type="password")

        if st.button("Aggiorna"):
            if find_user(email):
                update_user(email, {"password": newp})
                st.success("Password aggiornata")
            else:
                st.error("Email non trovata")

    st.stop()

# =========================
# DESIGN
# =========================
st.markdown("""
<style>
.stApp{
    background:#F5F1E8;
    max-width:480px;
    margin:auto;
}
div.stButton > button{
    background:#f43f5e;
    color:white;
    border-radius:14px;
    width:100%;
    font-weight:bold;
}
.card{
    background:#fffdf9;
    padding:14px;
    border-radius:16px;
    margin:10px 0;
    border:1px solid #e7dfd2;
}
.badge{
    background:#fff1f2;
    padding:10px;
    border-radius:12px;
    text-align:center;
    border:1px solid #fda4af;
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

    st.title(f"Ciao {nome} 👋")

    if fond == "SI":
        st.markdown('<div class="badge">🌸 Mamma Fondatrice</div>', unsafe_allow_html=True)

    st.markdown("""
♻️ LoopBaby è un sistema circolare  
👶 pensato per crescere con il tuo bambino  
💛 meno sprechi, più risparmio  
""")

    st.markdown('<div class="card">🔥 Promo: 10 capi → BOX GRATIS</div>', unsafe_allow_html=True)

# =========================
# BOX
# =========================
if st.session_state.page == "Box":

    st.title("Box")

    for n,p in [
        ("LUNA 🌙",19.9),
        ("SOLE ☀️",19.9),
        ("NUVOLA ☁️",19.9),
        ("PREMIUM 💎",29.9)
    ]:
        st.markdown(f'<div class="card">{n} - {p}€</div>', unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": p})

# =========================
# VETRINA
# =========================
if st.session_state.page == "Vetrina":

    st.title("Vetrina")

    for n,p in [("Body",9.9),("Maglia",8.9),("Pantaloni",12.9)]:
        st.markdown(f'<div class="card">{n} - {p}€</div>', unsafe_allow_html=True)
        if st.button(f"Aggiungi {n}"):
            st.session_state.cart.append({"name": n, "price": p})

# =========================
# INFO (COME FUNZIONA LOOPBABY)
# =========================
if st.session_state.page == "Info":

    st.title("Come funziona LoopBaby 🔄")

    st.markdown("""
1. Scegli la tua Box e ricevila nel locker  
2. Hai 48h per controllare i capi  
3. Usi i vestiti fino a 3 mesi  
4. Quando il bambino cresce cambi taglia  
5. Spedizioni sempre semplici e circolari  
""")

    st.markdown('<div class="card">🚚 Spedizione gratuita sopra 50€ o con Box</div>', unsafe_allow_html=True)

# =========================
# CHI SIAMO
# =========================
if st.session_state.page == "ChiSiamo":

    st.title("Chi siamo ❤️")

    st.markdown("""
Siamo genitori come te.

Abbiamo creato LoopBaby per:

- semplificare la vita  
- ridurre gli sprechi  
- far risparmiare famiglie  
""")

# =========================
# CARRELLO
# =========================
if st.session_state.page == "Carrello":

    st.title("Carrello")

    tot = sum(i["price"] for i in st.session_state.cart)
    has_box = any("Box" in i["name"] for i in st.session_state.cart)

    sped = 0 if tot > 50 or has_box else 7.90

    for i,item in enumerate(st.session_state.cart):
        st.write(f"{item['name']} - {item['price']}€")

    st.markdown(f"**Totale:** {tot}€")
    st.markdown(f"**Spedizione:** {sped}€")
    st.markdown(f"**Totale finale:** {tot + sped}€")

# =========================
# PROFILO
# =========================
if st.session_state.page == "Profilo":

    st.title("Profilo")

    u = st.session_state.user

    nome = st.text_input("Nome", u.get("nome",""))
    tel = st.text_input("Telefono", u.get("telefono",""))
    city = st.text_input("Città", u.get("citta",""))

    if st.button("Salva"):
        update_user(u["email"], {
            "nome": nome,
            "telefono": tel,
            "citta": city
        })
        st.success("Salvato")
