import streamlit as st
from supabase import create_client
import base64
import os

# -----------------------------
# 🔐 SUPABASE (METTI QUI LE TUE CHIAVI)
# -----------------------------
SUPABASE_URL = "https://TUO-PROGETTO.supabase.co"
SUPABASE_ANON_KEY = "LA_TUA_ANON_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# -----------------------------
# ⚙️ STATE
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"
if "profilo" not in st.session_state:
    st.session_state.profilo = {}
if "carrello" not in st.session_state:
    st.session_state.carrello = []

# -----------------------------
# 🔁 NAV
# -----------------------------
def vai(p):
    st.session_state.pagina = p
    st.rerun()

# -----------------------------
# 🛒 CARRELLO
# -----------------------------
def aggiungi(nome, prezzo):
    st.session_state.carrello.append({
        "nome": nome,
        "prezzo": prezzo
    })
    st.toast("Aggiunto al carrello")

# -----------------------------
# 🎨 UI BASE
# -----------------------------
st.set_page_config(page_title="LoopBaby", layout="centered")

st.markdown("""
<style>
.stApp {max-width:450px;margin:auto;background:#FDFBF7;}
button {border-radius:14px !important;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 🔐 LOGIN / REGISTER
# =====================================================
if st.session_state.user is None:

    st.title("LoopBaby 👶")

    tab1, tab2 = st.tabs(["Login", "Registrati"])

    # ---------------- LOGIN ----------------
    with tab1:
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Accedi"):
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    st.session_state.user = res.user

                    # carica profilo
                    prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
                    if prof.data:
                        st.session_state.profilo = prof.data[0]

                    vai("home")

                except Exception as e:
                    st.error("Login errato")

    # ---------------- REGISTER ----------------
    with tab2:
        with st.form("reg"):
            email = st.text_input("Email ")
            password = st.text_input("Password ", type="password")

            if st.form_submit_button("Crea account"):
                try:
                    supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    st.success("Controlla email per conferma")
                except Exception as e:
                    st.error(str(e))

# =====================================================
# 🚀 APP
# =====================================================
else:

    # ---------------- HOME ----------------
    if st.session_state.pagina == "home":
        st.title("LoopBaby 👶")

        st.write("Armadio circolare per bambini")

        if st.button("Vai alle Box"):
            vai("box")

        if st.button("Profilo"):
            vai("profilo")

        if st.button("Carrello"):
            vai("carrello")

    # ---------------- BOX ----------------
    elif st.session_state.pagina == "box":
        st.title("Box disponibili 📦")

        for nome, prezzo in [
            ("Box Luna 🌙", 19.90),
            ("Box Sole ☀️", 19.90),
            ("Box Premium 💎", 29.90)
        ]:
            st.markdown(f"### {nome} — {prezzo}€")

            if st.button(f"Aggiungi {nome}"):
                aggiungi(nome, prezzo)

    # ---------------- PROFILO ----------------
    elif st.session_state.pagina == "profilo":

        st.title("Profilo 👤")

        d = st.session_state.profilo

        with st.form("profilo"):
            nome = st.text_input("Nome genitore", d.get("nome_genitore", ""))
            bambino = st.text_input("Nome bambino", d.get("nome_bambino", ""))
            taglia = st.selectbox("Taglia", ["50-56", "62-68", "74-80"])

            if st.form_submit_button("Salva"):
                supabase.table("profili").upsert({
                    "id": st.session_state.user.id,
                    "nome_genitore": nome,
                    "nome_bambino": bambino,
                    "taglia": taglia
                }).execute()

                st.success("Profilo salvato")

    # ---------------- CARRELLO ----------------
    elif st.session_state.pagina == "carrello":

        st.title("Carrello 🛒")

        if not st.session_state.carrello:
            st.write("Vuoto")
        else:
            totale = 0

            for i in st.session_state.carrello:
                st.write(f"{i['nome']} - {i['prezzo']}€")
                totale += i["prezzo"]

            st.markdown(f"## Totale: {totale:.2f}€")

            if st.button("Checkout"):
                st.success("Pagamento (Stripe dopo)")

    # ---------------- NAV ----------------
    st.markdown("---")
    cols = st.columns(4)

    for i, p in enumerate(["home", "box", "profilo", "carrello"]):
        with cols[i]:
            if st.button(p.capitalize()):
                vai(p)
