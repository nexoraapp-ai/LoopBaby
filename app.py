import streamlit as st
import requests
import bcrypt

st.set_page_config(page_title="LoopBaby", layout="centered")

SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

# =========================
# SAFE
# =========================
def g(d,k,default=""):
    return (d or {}).get(k,default)

def hash_password(p):
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_password(p,h):
    return bcrypt.checkpw(p.encode(),h.encode())

# =========================
# DATA
# =========================
def users():
    try:
        return requests.get(SHEETDB_URL).json()
    except:
        return []

def find(email):
    for u in users():
        if g(u,"email").lower()==email.lower():
            return u
    return None

def save(u):
    requests.post(SHEETDB_URL,json={"data":[u]})

# =========================
# LOCKER SMART
# =========================
LOCKER = {
    "Milano": ["Duomo Locker","Centrale","Porta Garibaldi"],
    "Lecco": ["Lecco Centro","Bione"],
    "Calolziocorte": ["InPost","Esselunga","Poste"]
}

def suggest_city(address):
    a = address.lower()
    if "milano" in a: return "Milano"
    if "lecco" in a: return "Lecco"
    return "Calolziocorte"

# =========================
# SESSION
# =========================
if "u" not in st.session_state:
    st.session_state.u = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# DESIGN
# =========================
st.markdown("""
<style>
.stApp{background:#f5f1e8;}
.card{background:white;padding:18px;border-radius:18px;margin:10px 0;}
.big{font-size:26px;font-weight:800;}
</style>
""",unsafe_allow_html=True)

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.page=="login":

    st.title("LoopBaby 🌸")

    mode=st.radio("Accesso",["Login","Registrati"])

    email=st.text_input("Email")
    pw=st.text_input("Password",type="password")

    if mode=="Registrati":

        nome=st.text_input("Nome e Cognome")
        bambino=st.text_input("Nome bambino")
        nascita=st.date_input("Data nascita")
        taglia=st.selectbox("Taglia",["50-56","62-68","74-80"])

        indirizzo=st.text_input("Dove abiti?")
        città=suggest_city(indirizzo)
        locker=st.selectbox("Locker",LOCKER[città])

        if st.button("Crea account"):

            if find(email):
                st.error("Email già registrata")
                st.stop()

            u={
                "email":email,
                "password":hash_password(pw),
                "nome":nome,
                "bambino":bambino,
                "nascita":str(nascita),
                "taglia":taglia,
                "indirizzo":indirizzo,
                "città":città,
                "locker":locker
            }

            save(u)
            st.session_state.u=u
            st.session_state.page="home"
            st.rerun()

    else:
        if st.button("Entra"):
            u=find(email)
            if u and check_password(pw,g(u,"password")):
                st.session_state.u=u
                st.session_state.page="home"
                st.rerun()
            else:
                st.error("Errore login")

    st.stop()

# =========================
# USER
# =========================
u=st.session_state.u or {}
nome=(g(u,"nome") or "Utente").split()[0]

# =========================
# HOME
# =========================
if st.session_state.page=="home":

    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <img src="https://via.placeholder.com/80" style="border-radius:15px;">
        <div class="big">Ciao """+nome+""" 👋</div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    👶 Capi selezionati<br>
    🔄 Cresce con il bambino<br>
    💰 Risparmio reale<br>
    🏠 Locker vicino a te<br>
    ♻️ Zero sprechi
    </div>

    <div class="card" style="border:2px solid #f43f5e;">
    <b>✨ PROMO MAMME FONDATRICI (CLICCA)</b><br>
    Dona 10+ capi → gift card box entro 3 mesi
    </div>
    """,unsafe_allow_html=True)

    if st.button("Apri Promo"):
        st.session_state.page="promo"
        st.rerun()

# =========================
# PROMO
# =========================
elif st.session_state.page=="promo":

    st.title("Promo Mamme Fondatrici")

    peso=st.text_input("Peso pacco")
    dim=st.text_input("Dimensioni")
    locker=g(u,"locker")

    if st.button("Invia richiesta"):

        st.success("Etichetta inviata entro 24h al tuo locker: "+locker)

# =========================
# BOX
# =========================
elif st.session_state.page=="box":

    st.title("Box")

    tipo=st.radio("Tipo",["Standard 14,90","Premium 24,90"])

    if tipo.startswith("Standard"):
        st.markdown("👕 Usati in buono stato")
    else:
        st.markdown("✨ Seminuovi o nuovi")

# =========================
# VETRINA
# =========================
elif st.session_state.page=="vetrina":

    st.title("Vetrina")

    st.write("💰 Spedizione gratis sopra 50€")
    st.write("📦 Sotto 50€ → 7,90€ locker")

# =========================
# PROFILO
# =========================
elif st.session_state.page=="profilo":

    st.title("Profilo")

    st.write("Nome:",g(u,"nome"))
    st.write("Bambino:",g(u,"bambino"))
    st.write("Taglia:",g(u,"taglia"))
    st.write("Locker:",g(u,"locker"))

# =========================
# COME FUNZIONA
# =========================
elif st.session_state.page=="come":

    st.title("Come funziona")

    st.write("""
1. scegli box  
2. ricevi al locker  
3. usi  
4. restituisci  
5. cambi taglia
""")

# =========================
# CONTATTI
# =========================
elif st.session_state.page=="contatti":

    st.title("Contatti")

    st.write("📧 assistenza.loopbaby@gmail.com")
    st.write("📱 WhatsApp 3921404637")
    st.write("❌ NO chiamate")

# =========================
# LOGOUT
# =========================
elif st.session_state.page=="logout":
    st.session_state.u=None
    st.session_state.page="login"
    st.rerun()
