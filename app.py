import streamlit as st
import requests
import bcrypt
from datetime import date

st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# SAFE GET
# =========================
def g(d,k,default=""):
    return (d or {}).get(k,default)

# =========================
# PASSWORD
# =========================
def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p,h):
    return bcrypt.checkpw(p.encode(),h.encode())

# =========================
# LOCKER REALI (ESPANDIBILI)
# =========================
LOCKER = {
    "Milano": ["Duomo Locker", "Centrale FS", "Porta Garibaldi"],
    "Lecco": ["Lecco Centro", "Meridiana", "Bione"],
    "Calolziocorte": ["Esselunga", "Poste Italiane", "Centro Paese"]
}

# =========================
# TAGLIA AUTOMATICA
# =========================
def suggest_taglia(nascita):
    try:
        year = int(str(nascita)[:4])
        age_months = (2026 - year) * 12
        if age_months < 6: return "50-56"
        if age_months < 12: return "62-68"
        if age_months < 24: return "74-80"
        return "86-92"
    except:
        return "62-68"

# =========================
# DB
# =========================
def get_users():
    try:
        return requests.get(SHEETDB_URL).json()
    except:
        return []

def find_user(email):
    for u in get_users():
        if g(u,"email").lower() == email.lower():
            return u
    return None

def save_user(u):
    requests.post(SHEETDB_URL, json={"data":[u]})

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# DESIGN
# =========================
st.markdown("""
<style>
.stApp{background:#f5f1e8;}
.card{background:white;padding:18px;border-radius:18px;margin:10px 0;}
.title{font-size:26px;font-weight:800;}
.small{font-size:13px;color:#555;}
</style>
""", unsafe_allow_html=True)

# =========================
# MENU HAMBURGER (SIDEBAR)
# =========================
menu = st.sidebar.selectbox("Menu",[
    "Home","Box","Vetrina","Profilo",
    "Come funziona","Promo","Contatti","Logout"
])

# =========================
# LOGIN / REGISTER (OBBLIGATORIO COMPLETO)
# =========================
if st.session_state.page == "login":

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso",["Login","Registrati"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # ================= REGISTER =================
    if mode == "Registrati":

        nome = st.text_input("Nome e Cognome")
        bambino = st.text_input("Nome bambino")
        nascita = st.date_input("Data nascita")

        # TAGLIA AUTOMATICA SUGGERITA
        auto_taglia = suggest_taglia(nascita)
        st.info(f"Taglia suggerita: {auto_taglia}")

        taglia = st.selectbox("Conferma taglia",["50-56","62-68","74-80","86-92"],index=["50-56","62-68","74-80","86-92"].index(auto_taglia))

        città = st.selectbox("Città", list(LOCKER.keys()))
        locker = st.selectbox("Locker vicino", LOCKER[città])

        if st.button("Crea account"):

            if not email or "@" not in email:
                st.error("Email non valida")
                st.stop()

            if find_user(email):
                st.error("Email già registrata")
                st.stop()

            user = {
                "email": email,
                "password": hash_password(password),
                "nome": nome,
                "bambino": bambino,
                "nascita": str(nascita),
                "taglia": taglia,
                "città": città,
                "locker": locker
            }

            save_user(user)

            st.session_state.user = user
            st.session_state.page = "home"
            st.rerun()

    # ================= LOGIN =================
    else:
        if st.button("Entra"):

            u = find_user(email)

            if not u:
                st.error("Utente non trovato")
                st.stop()

            if not check_password(password, g(u,"password")):
                st.error("Password errata")
                st.stop()

            st.session_state.user = u
            st.session_state.page = "home"
            st.rerun()

    st.stop()

# =========================
# USER
# =========================
u = st.session_state.user or {}
nome = (g(u,"nome") or "Utente").split()[0]

# =========================
# HOME (DESIGN CORRETTO)
# =========================
if menu == "Home":

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <img src="https://via.placeholder.com/80" style="border-radius:15px;">
        <div class="title">Ciao {nome} 👋</div>
    </div>

    <div class="card">
    👶 Capi selezionati<br>
    🔄 Cresce con il bambino<br>
    💰 Risparmio reale<br>
    🏠 Locker vicino a te<br>
    ♻️ Zero sprechi
    </div>

    <div class="card" style="border:2px solid #f43f5e;">
    <b>✨ Promo Mamme Fondatrici</b><br>
    Dona 10+ capi → gift card valida 3 mesi
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROMO (COMPLETA + BACK)
# =========================
elif menu == "Promo":

    st.title("Promo Mamme Fondatrici")

    st.info("Dona 10 o più capi → noi ritiriamo tutto + regalo box (valido 3 mesi)")

    peso = st.text_input("Peso pacco")
    dim = st.text_input("Dimensioni pacco")

    città = g(u,"città")
    locker = st.selectbox("Locker di ritiro", LOCKER.get(città, []))

    if st.button("Invia richiesta etichetta"):

        st.success(f"Etichetta inviata entro 24h al locker: {locker}")
        st.info("La tua gift card sarà valida 3 mesi")

    if st.button("⬅ Torna indietro"):
        st.session_state.page = "home"
        st.rerun()

# =========================
# BOX
# =========================
elif menu == "Box":

    st.title("Box")

    tipo = st.radio("Scegli",["Standard 14,90€","Premium 24,90€"])

    if tipo.startswith("Standard"):
        st.write("👕 Capi usati in buono stato")
    else:
        st.write("✨ Capi seminuovi o nuovi")

# =========================
# VETRINA
# =========================
elif menu == "Vetrina":

    st.title("Vetrina")

    st.write("🚚 Gratis sopra 50€")
    st.write("📦 Sotto 50€ → 7,90€ locker")

# =========================
# PROFILO
# =========================
elif menu == "Profilo":

    st.title("Profilo")

    st.write("Nome:",g(u,"nome"))
    st.write("Bambino:",g(u,"bambino"))
    st.write("Taglia:",g(u,"taglia"))
    st.write("Locker:",g(u,"locker"))

# =========================
# COME FUNZIONA
# =========================
elif menu == "Come funziona":

    st.title("Come funziona")

    st.write("""
LoopBaby è semplice:
1. scegli box
2. ricevi al locker
3. usi i capi
4. restituisci
5. cambi taglia automaticamente
""")

# =========================
# CONTATTI
# =========================
elif menu == "Contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 WhatsApp 3921404637")
    st.write("❌ No chiamate")

# =========================
# LOGOUT
# =========================
elif menu == "Logout":
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()
