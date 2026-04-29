import streamlit as st
from supabase import create_client

# =====================================================
# 🔐 SUPABASE (USA SOLO CHIAVE PUBBLICA)
# =====================================================
SUPABASE_URL = "https://izyfzqyopmpvijdtfqfe.supabase.co"

SUPABASE_KEY = "sb_publishable_9t_Psdh5tIz9OsfrSAwuMw_hJQ9i89Z"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================================================
# STATE
# =====================================================
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "cart" not in st.session_state:
    st.session_state.cart = []

# =====================================================
# NAV
# =====================================================
def go(p):
    st.session_state.page = p
    st.rerun()

def add_cart(name, price):
    st.session_state.cart.append({"name": name, "price": price})
    st.toast("Aggiunto ✔")

# =====================================================
# UI BASE
# =====================================================
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

    st.title("👶 LoopBaby")

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

                    prof = supabase.table("profili") \
                        .select("*") \
                        .eq("id", res.user.id) \
                        .execute()

                    if prof.data:
                        st.session_state.profile = prof.data[0]

                    go("home")

                except:
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
    if st.session_state.page == "home":
        st.title("LoopBaby 👶")
        st.write("Armadio circolare per bambini")

        if st.button("📦 Box"):
            go("box")

        if st.button("👤 Profilo"):
            go("profile")

        if st.button("🛒 Carrello"):
            go("cart")

    # ---------------- BOX ----------------
    elif st.session_state.page == "box":
        st.title("Box disponibili 📦")

        boxes = [
            ("Luna 🌙", 19.90),
            ("Sole ☀️", 19.90),
            ("Premium 💎", 29.90)
        ]

        for name, price in boxes:
            st.markdown(f"### {name}")
            st.write(f"{price}€")

            if st.button(f"Aggiungi {name}"):
                add_cart(name, price)

        if st.button("⬅ Home"):
            go("home")

    # ---------------- PROFILE ----------------
    elif st.session_state.page == "profile":
        st.title("Profilo 👤")

        p = st.session_state.profile

        with st.form("profile"):
            name = st.text_input("Genitore", p.get("nome_genitore",""))
            baby = st.text_input("Bimbo", p.get("nome_bambino",""))
            size = st.selectbox("Taglia", ["50-56","62-68","74-80"])

            if st.form_submit_button("Salva"):
                supabase.table("profili").upsert({
                    "id": st.session_state.user.id,
                    "nome_genitore": name,
                    "nome_bambino": baby,
                    "taglia": size
                }).execute()

                st.success("Salvato ✔")

        if st.button("Home"):
            go("home")

    # ---------------- CART ----------------
    elif st.session_state.page == "cart":
        st.title("Carrello 🛒")

        if not st.session_state.cart:
            st.info("Vuoto")
        else:
            total = 0

            for i in st.session_state.cart:
                st.write(f"{i['name']} - {i['price']}€")
                total += i["price"]

            st.markdown(f"## Totale: {total:.2f}€")

            if st.button("Checkout"):
                st.success("Pagamento (Stripe dopo)")

        if st.button("Home"):
            go("home")

# =====================================================
# NAV BAR
# =====================================================
st.markdown("---")
cols = st.columns(4)

for i, p in enumerate(["home","box","profile","cart"]):
    with cols[i]:
        if st.button(p.capitalize()):
            go(p)
