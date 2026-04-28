import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE ---
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_9t_Psdh5tIz9OsfrSAwuMw_hJQ9i89Z"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. SETUP ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome" if not st.session_state.user else "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}

def vai(p): st.session_state.pagina = p

def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        if d.data: st.session_state.dati = d.data[0]
        vai("Home"); st.rerun()
    except: st.error("Errore Accesso")

def reg(e, p):
    try:
        supabase.auth.sign_up({"email": e, "password": p})
        st.success("📩 Conferma la mail!")
    except: st.error("Errore Registrazione")

def salva_db(d):
    d["id"] = st.session_state.user.id
    supabase.table("profili").upsert(d).execute()
    st.session_state.dati = d
    st.success("✅ Salvato!")

def get_img(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img, logo = get_img("bimbo.jpg"), get_img("logo.png")

# --- 3. CSS ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; padding-bottom: 100px; }}
    .header {{ background-image: url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 20px; }}
    .header-t {{ color: white; font-size: 30px; font-weight: 800; text-shadow: 2px 2px 5px rgba(0,0,0,0.3); }}
    div.stButton > button {{ background: #f43f5e !important; color: white !important; border-radius: 15px; width: 100%; font-weight: 700; border: none; }}
    .card {{ border-radius: 20px; padding: 20px; margin: 10px; border: 1px solid #EAE2D6; background: white; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login"); st.rerun()
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("ENTRA"): login(e, p)
        with t2:
            er = st.text_input("Email ")
            pr = st.text_input("Password ", type="password")
            if st.button("CREA ACCOUNT"): reg(er, pr)
else:
    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        st.markdown(f"### Ciao {st.session_state.dati.get('nome_genitore', 'Mamma')}! 👋")
        st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; st.rerun()

    elif st.session_state.pagina == "Box":
        st.markdown("## Scegli Box 📦")
        tg = st.session_state.dati.get('taglia', 'Non impostata')
        st.info(f"Taglia attuale: {tg}")
        if st.button("Box Luna - 19,90€"): st.session_state.carrello.append("Box Luna"); st.toast("Aggiunta!")

    elif st.session_state.pagina == "Carrello":
        st.markdown("## Carrello 🛒")
        if not st.session_state.carrello: st.write("Vuoto")
        else:
            for i in st.session_state.carrello: st.write(f"- {i}")
            if st.button("PAGA ORA"): st.success("Pagamento completato!")

    elif st.session_state.pagina == "Profilo":
        with st.form("p"):
            n = st.text_input("Nome", st.session_state.dati.get('nome_genitore', ''))
            nb = st.text_input("Bimbo", st.session_state.dati.get('nome_bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            if st.form_submit_button("SALVA"): salva_db({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})

    # NAV
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    with c[0]: 
        if st.button("🏠"): vai("Home"); st.rerun()
    with c[1]: 
        if st.button("📦"): vai("Box"); st.rerun()
    with c[2]: 
        if st.button("👤"): vai("Profilo"); st.rerun()
    with c[3]: 
        if st.button("🛒"): vai("Carrello"); st.rerun()
