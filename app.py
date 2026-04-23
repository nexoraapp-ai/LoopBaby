import streamlit as st

st.set_page_config(page_title="LoopBaby", layout="wide")

# --- HEADER ---
st.title("👶 LoopBaby")
st.subheader("Vestiamo il tuo bambino senza sprechi e senza stress 💚")

# --- MENU ---
menu = st.sidebar.selectbox("Menu", [
    "Home",
    "Box Standard",
    "Box Premium",
    "Vetrina",
    "Profilo"
])

# --- HOME ---
if menu == "Home":
    st.markdown("## Ciao Mamma 👋")
    st.markdown("Risparmia fino a **1000€ all'anno** vestendo il tuo bambino.")

    st.image("https://images.unsplash.com/photo-1519681393784-d120267933ba", use_column_width=True)

    st.markdown("### Come funziona")
    st.write("1. Scegli la Box")
    st.write("2. Ritira al locker vicino a te")
    st.write("3. Dopo 3 mesi decidi cosa fare")

    st.button("👉 Scegli la tua Box")

# --- BOX STANDARD ---
elif menu == "Box Standard":
    st.header("📦 Box Standard - 19,90€ + spedizione")

    scelta = st.radio("Scegli stile", ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"])

    st.markdown("### Esempio capi inclusi")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://images.unsplash.com/photo-1600180758890-6b94519a8ba4")
    with col2:
        st.image("https://images.unsplash.com/photo-1596464716127-f2a82984de30")
    with col3:
        st.image("https://images.unsplash.com/photo-1585386959984-a4155224a1ad")

    st.write("10 capi selezionati e igienizzati")

    if st.button("Attiva Box Standard"):
        st.success(f"Hai scelto {scelta}")

# --- BOX PREMIUM ---
elif menu == "Box Premium":
    st.header("💎 Box Premium - 29,90€ + spedizione")

    st.markdown("### Capi premium selezionati")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://images.unsplash.com/photo-1588776814546-ec7e03c6f9c3")
    with col2:
        st.image("https://images.unsplash.com/photo-1593032465175-481ac7f4019c")
    with col3:
        st.image("https://images.unsplash.com/photo-1600185365483-26d7d0a3c8c1")

    st.write("Qualità superiore e outfit curati")

    if st.button("Attiva Box Premium"):
        st.success("Box Premium attivata")

# --- VETRINA ---
elif menu == "Vetrina":
    st.header("🛍️ Vetrina")

    st.write("I capi acquistati rimangono a te.")

    st.info("🚚 Spedizione gratuita sopra 50€ o se abbinata a una Box")

    prodotti = [
        {"nome": "Body cotone", "prezzo": 9.90, "img": "https://images.unsplash.com/photo-1588776814546-ec7e03c6f9c3"},
        {"nome": "Tutina baby", "prezzo": 14.90, "img": "https://images.unsplash.com/photo-1593032465175-481ac7f4019c"},
        {"nome": "Jeans baby", "prezzo": 19.90, "img": "https://images.unsplash.com/photo-1600185365483-26d7d0a3c8c1"}
    ]

    for p in prodotti:
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(p["img"])
        with col2:
            st.write(f"### {p['nome']}")
            st.write(f"{p['prezzo']}€")
            st.button("Compra", key=p["nome"])

# --- PROFILO ---
elif menu == "Profilo":
    st.header("👤 Il tuo profilo")

    nome = st.text_input("Nome mamma")
    telefono = st.text_input("Cellulare")
    email = st.text_input("Email")
    bambino = st.text_input("Nome bambino")
    nascita = st.date_input("Data di nascita")

    if st.button("Salva profilo"):
        st.success("Profilo salvato 💚")
