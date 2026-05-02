import streamlit as st
import requests
import bcrypt
import os
import base64
import json
from datetime import date

# =========================
# 🔐 PASSWORD
# =========================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


# =========================
# 📡 SHEETDB
# =========================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"


def carica_dati(email):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower():
                return {
                    "nome_genitore": u.get("nome_genitore",""),
                    "email": u.get("email",""),
                    "telefono": u.get("telefono",""),
                    "nome_bambino": u.get("nome_bambino",""),
                    "nascita": date(2024, 1, 1),
                    "taglia": u.get("taglia","50-56 cm"),
                    "locker": u.get("locker","")
                }
    except:
        pass

    return {
        "nome_genitore": "",
        "email": email,
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }


def login(email, password):
    try:
        r = requests.get(SHEETDB_URL)
        for u in r.json():
            if u.get("email","").lower() == email.lower():
                if check_password(password, u.get("password","")):
                    st.session_state.user = u
                    return True
    except:
        pass
    return False


def registra(email, password):
    hashed = hash_password(password)
    requests.post(SHEETDB_URL, json={
        "data":[{"email":email,"password":hashed}]
    })


def email_esiste(email):
    try:
        r = requests.get(SHEETDB_URL)
        return any(u.get("email","").lower() == email.lower() for u in r.json())
    except:
        return False


# =========================
# 🔐 SESSIONE LOGIN
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.title("LoopBaby 🌸")

    mode = st.radio("Accesso", ["Login", "Registrati"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Registrati":

        if st.button("Crea account"):

            if not email or "@" not in email:
                st.error("Email non valida")

            elif len(password) < 4:
                st.error("Password troppo corta")

            elif email_esiste(email):
                st.error("Email già registrata")

            else:
                registra(email, password)
                st.success("Account creato!")

                login(email, password)
                st.session_state.auth = True
                st.session_state.dati = carica_dati(email)
                st.session_state.pagina = "Profilo"
                st.rerun()

    else:

        if st.button("Entra"):
            if login(email, password):
                st.session_state.auth = True
                st.session_state.dati = carica_dati(email)

                if st.session_state.dati.get("nome_genitore","") == "":
                    st.session_state.pagina = "Profilo"
                else:
                    st.session_state.pagina = "Home"

                st.rerun()
            else:
                st.error("Credenziali errate")

    st.stop()


# =========================
# 💾 STATO APP
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

if "carrello" not in st.session_state:
    st.session_state.carrello = []


def vai(p):
    st.session_state.pagina = p


def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto!")


# =========================
# 🎨 CSS (IDENTICO)
# =========================
st.markdown("""
<style>
.stApp { background-color:#FDFBF7; max-width:450px; margin:0 auto; padding-bottom:120px; }
.card { border-radius:25px; padding:20px; margin:10px 20px; background:#fff; border:1px solid #eee; }

.box-luna { background:#f1f5f9; }
.box-sole { background:#FFD600; }
.box-nuvola { background:#94A3B8; color:white; }
.box-premium { background:linear-gradient(135deg,#4F46E5,#312E81); color:white; }

.prezzo-rosa { color:#ec4899; font-size:22px; font-weight:900; }
</style>
""", unsafe_allow_html=True)

st.title("LOOPBABY 🌸")


# =========================
# 🏠 HOME
# =========================
if st.session_state.pagina == "Home":

    dati = st.session_state.get("dati", {})
    nome = dati.get("nome_genitore","")
    u_nome = nome.split()[0] if nome else ""

    st.markdown(f"### Ciao {u_nome} 👋")

    st.write("Benvenuto in LoopBaby")

    if st.button("Vai alle Box"):
        vai("Box")
        st.rerun()


# =========================
# 📦 BOX
# =========================
elif st.session_state.pagina == "Box":

    st.markdown("## Box 📦")

    for nome, cls in [
        ("LUNA 🌙","box-luna"),
        ("SOLE ☀️","box-sole"),
        ("NUVOLA ☁️","box-nuvola")
    ]:

        st.markdown(f"""
        <div class="card {cls}">
            <h3>{nome}</h3>
            <p>19.90€</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Scegli {nome}"):
            aggiungi(nome, 19.90)


# =========================
# 🛒 CARRELLO
# =========================
elif st.session_state.pagina == "Carrello":

    st.markdown("## Carrello")

    totale = 0

    for item in st.session_state.carrello:
        st.write(item["nome"], item["prezzo"])
        totale += item["prezzo"]

    st.write("Totale:", totale)


# =========================
# 👤 PROFILO
# =========================
elif st.session_state.pagina == "Profilo":

    st.markdown("## Profilo")

    d = st.session_state.get("dati", {})

    st.write(d)


# =========================
# 🧭 NAVBAR
# =========================
st.markdown("---")

cols = st.columns(4)

menu = [("Home","Home"),("Box","Box"),("Carrello","Carrello"),("Profilo","Profilo")]

for i,(icon,pag) in enumerate(menu):
    with cols[i]:
        if st.button(icon):
            vai(pag)
            st.rerun()
