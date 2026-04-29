import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime, timedelta

# --- 1. DATABASE LOCALE (ADDIO SUPABASE / ADDIO ERRORI 404) ---
DB_FILE = "database_loop.csv"

def carica_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['email', 'password', 'nome', 'taglia', 'scadenza'])

def salva_db(df):
    df.to_csv(DB_FILE, index=False)

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. CSS PROFESSIONALE ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #FDFBF7; max-width: 450px; margin: 0 auto; }
    div.stButton > button { 
        background-color: #f43f5e !important; color: white !important; 
        border-radius: 20px !important; width: 100% !important; 
        border: none !important; font-weight: bold; height: 45px;
    }
    .card { border-radius: 20px; padding: 20px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #EAE2D6; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_db()

if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<div class='card' style='text-align:center;'><h3>L'armadio circolare che cresce con il tuo bambino 🔄</h3></div>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    
    elif st.session_state.pagina == "Login":
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    user = df[(df['email'] == e) & (df['password'].astype(str) == str(p))]
                    if not user.empty:
                        st.session_state.user = e
                        vai("Home")
                    else: st.error("Dati errati")
        with t2:
            with st.form("r"):
                er = st.text_input("La tua migliore Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if er in df['email'].values: st.error("Sei già registrata!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = pd.DataFrame([{"email": er, "password": str(pr), "nome": "Mamma", "taglia": "---", "scadenza": scad}])
                        salva_db(pd.concat([df, nuovo]))
                        st.success("REGISTRATA! Ora fai l'accesso dalla scheda 'Accedi'.")
else:
    # --- HOME DOPO IL LOGIN ---
    st.markdown(f"## Ciao! 👋")
    st.write(f"Account: {st.session_state.user}")
    
    st.markdown("""
    <div class='card'>
        ✨ <b>Promo Fondatrici</b><br>
        Dona 10 capi e ricevi una Box OMAGGIO!
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Esci"):
        st.session_state.user = None
        vai("Welcome")

    # BARRA NAVIGAZIONE FISSA
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("🏠 Home")
    with c2: st.button("📦 Box")
    with c3: st.button("👤 Profilo")
