import streamlit as st
import os
import base64
from datetime import date
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE DIRETTA SUPABASE ---
# Inserite qui per evitare errori di configurazione nei Secrets
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

try:
    supabase: Client = create_client(URL_DB, KEY_DB)
except Exception as e:
    st.error(f"Errore tecnico di connessione: {e}")

# --- 2. CONFIGURAZIONE PAGINA E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None
if "dati" not in st.session_state:
    st.session_state.dati = {"nome_genitore": "", "email": "", "telefono": "", "nome_bambino": "", "nascita": date(2024, 1, 1), "taglia": "50-56 cm", "locker": ""}
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "carrello" not in st.session_state:
    st.session_state.carrello = []

# --- 3. FUNZIONI LOGICA ---
def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def carica_profilo_db(user_id):
    try:
        res = supabase.table("profili").select("*").eq("id", user_id).execute()
        if res.data:
            d = res.data[0]
            if d.get("nascita"): d["nascita"] = date.fromisoformat(d["nascita"])
            st.session_state.dati.update(d)
    except: pass

def salva_profilo_db():
    d = st.session_state.dati.copy()
    d["nascita"] = d["nascita"].isoformat()
    d["id"] = st.session_state.user.id
    supabase.table("profili").upsert(d).execute()
    st.success("Profilo salvato su database online!")

# --- 4. SCHERMATA DI ACCESSO (BLOCCANTE) ---
if st.session_state.user is None:
    st.markdown("<h2 style='text-align:center; color:#f43f5e;'>LoopBaby 🌸</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["Accedi", "Registrati", "Password dimenticata"])
    
    with t1:
        em = st.text_input("Email", key="l_em")
        pw = st.text_input("Password", type="password", key="l_pw")
        if st.button("ACCEDI", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": em, "password": pw})
                st.session_state.user = res.user
                carica_profilo_db(res.user.id)
                st.rerun()
            except: st.error("Email o password errati (o non hai confermato l'email).")
            
    with t2:
        st.write("Crea il tuo account Manuel!")
        r_nome = st.text_input("Il tuo Nome completo")
        r_em = st.text_input("Email", key="r_em")
        r_pw = st.text_input("Password (almeno 6 caratteri)", type="password", key="r_pw")
        if st.button("CREA ACCOUNT", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": r_em, "password": r_pw})
                # Inseriamo il profilo iniziale
                supabase.table("profili").insert({"id": res.user.id, "email": r_em, "nome_genitore": r_nome}).execute()
                st.success("📩 CONTROLLA L'EMAIL! Clicca sul link di conferma per attivare l'account.")
            except Exception as e: st.error(f"Errore: {e}")

    with t3:
        f_em = st.text_input("Email per ricevere il link di reset")
        if st.button("INVIA LINK DI RECUPERO", use_container_width=True):
            supabase.auth.reset_password_for_email(f_em)
            st.info("Se l'email è registrata, riceverai un link tra pochi istanti.")
    st.stop()

# --- 5. STYLE E HEADER (DOPO IL LOGIN) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{
        background-color: #f43f5e; height: 80px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 25px; border-radius: 0 0 30px 30px;
    }}
    .header-text {{ color: white; font-size: 24px; font-weight: 800; letter-spacing: 2px; }}
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; border: none !important; height: 45px;
    }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 15px; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); border: 1px solid #EAE2D6; }}
    </style>
    <div class="header-custom"><div class="header-text">LOOPBABY</div></div>
    """, unsafe_allow_html=True)

# --- 6. NAVIGAZIONE PAGINE ---
if st.session_state.pagina == "Home":
    nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else "Mamma"
    st.markdown(f'<div style="padding:0 20px;"><h2 style="margin:0;">Ciao {nome}! 👋</h2><p style="color:#64748b;">Bentornata nel ciclo della moda sostenibile.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="background:#fff1f2; border:1px solid #fda4af;"><b style="color:#e11d48;">🎁 PROMO FONDATRICI</b><br>Regala 10 capi, ricevi la tua prima Box gratis!</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    st.markdown("<h3 style='text-align:center;'>Il tuo Profilo</h3>", unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card">
            <b>Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>Taglia:</b> {st.session_state.dati['taglia']}<br>
            <b>Email:</b> {st.session_state.user.email}
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
        if st.button("ESCI (LOGOUT)", type="secondary"): 
            st.session_state.user = None
            st.rerun()
    else:
        with st.form("edit_p"):
            n = st.text_input("Tuo Nome", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            tg = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            if st.form_submit_button("SALVA NEL DATABASE"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                salva_profilo_db()
                st.session_state.edit_mode = False
                st.rerun()

# --- 7. BARRA DI NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🏠"): vai("Home")
with c2: 
    if st.button("📦"): vai("Box")
with c3: 
    if st.button("👤"): vai("Profilo")
with c4: 
    if st.button("🛒"): vai("Carrello")
