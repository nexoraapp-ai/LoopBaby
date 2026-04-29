import streamlit as st
from supabase import create_client
import base64
import os
from datetime import date

# =========================
# 🔐 SUPABASE CONNECTION
# =========================
URL_DB = st.secrets["SUPABASE_URL"]
KEY_DB = st.secrets["SUPABASE_KEY"]

supabase = create_client(URL_DB, KEY_DB)

# =========================
# STATE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

if "pagina" not in st.session_state:
    st.session_state.pagina = "Welcome"

if "carrello" not in st.session_state:
    st.session_state.carrello = []

if "dati" not in st.session_state:
    st.session_state.dati = {}

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# =========================
# NAV
# =========================
def vai(p):
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast("Aggiunto ✔")

# =========================
# MAIN HEADER
# =========================
st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)

# =========================
# LOGIN / REGISTER
# =========================
if st.session_state.user is None:

    if st.session_state.pagina == "Welcome":
        st.write("Armadio circolare per bambini")
        if st.button("Inizia"):
            vai("login")

    elif st.session_state.pagina == "login":

        tab1, tab2 = st.tabs(["Login", "Registrati"])

        with tab1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Accedi"):
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    st.session_state.user = res.user

                    prof = supabase.table("profili") \
                        .select("*") \
                        .eq("id", res.user.id) \
                        .execute()

                    if prof.data:
                        st.session_state.dati = prof.data[0]

                    vai("home")

                except:
                    st.error("Errore login")

        with tab2:
            email = st.text_input("Email ")
            password = st.text_input("Password ", type="password")

            if st.button("Crea account"):
                try:
                    supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    st.success("Controlla email")
                except Exception as e:
                    st.error(str(e))

# =========================
# APP LOGGED IN
# =========================
else:

    # ---------------- HOME ----------------
    if st.session_state.pagina == "home":
        st.title("Home 👶")

        if st.button("Box"):
            vai("box")

        if st.button("Profilo"):
            vai("profilo")

        if st.button("Carrello"):
            vai("carrello")

    # ---------------- BOX ----------------
    elif st.session_state.pagina == "box":
        st.title("Box 📦")

        prodotti = [
            ("Luna 🌙", 19.90),
            ("Sole ☀️", 19.90),
            ("Premium 💎", 29.90)
        ]

        for n, p in prodotti:
            st.write(f"{n} - {p}€")
            if st.button(f"Aggiungi {n}"):
                aggiungi(n, p)

        if st.button("Home"):
            vai("home")

    # ---------------- PROFILO ----------------
    elif st.session_state.pagina == "profilo":
        st.title("Profilo 👤")

        d = st.session_state.dati

        with st.form("profile"):
            nome = st.text_input("Nome genitore", d.get("nome_genitore",""))
            bimbo = st.text_input("Nome bambino", d.get("nome_bambino",""))
            taglia = st.selectbox("Taglia", ["50-56","62-68","74-80"])

            if st.form_submit_button("Salva"):
                supabase.table("profili").upsert({
                    "id": st.session_state.user.id,
                    "nome_genitore": nome,
                    "nome_bambino": bimbo,
                    "taglia": taglia
                }).execute()

                st.success("Salvato ✔")

    # ---------------- CARRELLO ----------------
    elif st.session_state.pagina == "carrello":
        st.title("Carrello 🛒")

        total = 0

        for i in st.session_state.carrello:
            st.write(i["nome"], i["prezzo"])
            total += i["prezzo"]

        st.markdown(f"## Totale: {total:.2f}€")

        if st.button("Checkout"):
            st.success("Pagamento (da integrare dopo)")

        if st.button("Home"):
            vai("home")
