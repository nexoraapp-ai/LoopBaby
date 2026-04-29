import streamlit as st
import os
import base64
import json
from datetime import date
from supabase import create_client, Client

# --- 1. CONFIGURAZIONE E SUPABASE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# Inizializzazione Supabase (Assicurati di aver impostato i Secrets)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except:
    st.error("Configura SUPABASE_URL e SUPABASE_KEY nei Secrets di Streamlit!")
    st.stop()

# --- 2. STATO DELL'APP ---
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

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def carica_profilo_db(user_id):
    res = supabase.table("profili").select("*").eq("id", user_id).execute()
    if res.data:
        d = res.data[0]
        # Converte la stringa data in oggetto date
        if d.get("nascita"): d["nascita"] = date.fromisoformat(d["nascita"])
        st.session_state.dati.update(d)

def salva_profilo_db():
    d = st.session_state.dati.copy()
    d["nascita"] = d["nascita"].isoformat()
    d["id"] = st.session_state.user.id
    supabase.table("profili").upsert(d).execute()
    st.success("Profilo salvato!")

# --- 4. GESTIONE ACCESSO (PUNTO 1) ---
if st.session_state.user is None:
    st.markdown("<h2 style='text-align:center;'>LoopBaby 🌸</h2>", unsafe_allow_html=True)
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
            except: st.error("Credenziali errate o email non confermata.")
            
    with t2:
        st.write("Crea il tuo account per iniziare il ciclo.")
        r_em = st.text_input("Email", key="r_em")
        r_pw = st.text_input("Password (min. 6 car.)", type="password", key="r_pw")
        r_nome = st.text_input("Il tuo Nome")
        if st.button("REGISTRATI", use_container_width=True):
            try:
                res = supabase.auth.sign_up({"email": r_em, "password": r_pw})
                supabase.table("profili").insert({"id": res.user.id, "email": r_em, "nome_genitore": r_nome}).execute()
                st.success("📩 Controlla l'email per confermare l'account!")
            except Exception as e: st.error(f"Errore: {e}")

    with t3:
        f_em = st.text_input("Email per il recupero")
        if st.button("RECUPERA PASSWORD", use_container_width=True):
            supabase.auth.reset_password_for_email(f_em)
            st.info("Se l'email è registrata, riceverai un link.")
    st.stop()

# --- 5. DESIGN E CSS ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 110px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 25px; border-radius: 0 0 30px 30px;
    }}
    .header-text {{ color: white; font-size: 28px; font-weight: 800; letter-spacing: 2px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); }}
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; border: none !important;
    }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 15px; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); border: 1px solid #EAE2D6; }}
    .box-luna {{ background-color: #f1f5f9 !important; }}
    .box-sole {{ background-color: #FFD600 !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 22px; font-weight: 900; }}
    </style>
    <div class="header-custom"><div class="header-text">LOOPBABY</div></div>
    """, unsafe_allow_html=True)

# --- 6. PAGINE ---

if st.session_state.pagina == "Home":
    u_nome = st.session_state.dati['nome_genitore'].split()[0] if st.session_state.dati['nome_genitore'] else "Mamma"
    st.markdown(f"""<div style="padding: 0 20px;">
        <div style="font-size:26px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
        <div style="font-size:14px; color:#475569; margin-top:5px;">L'armadio circolare che cresce con il tuo bambino.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48;">✨ Promo Fondatrici</b><br><p style="font-size:12px;">Dona 10 capi e ricevi una <b>BOX OMAGGIO</b>!</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa ora"): vai("PromoDettaglio"); st.rerun()

elif st.session_state.pagina == "Box":
    st.markdown('<h3 style="text-align:center;">Scegli la tua Box 📦</h3>', unsafe_allow_html=True)
    tg = st.session_state.dati['taglia']
    st.info(f"Taglia attuale: {tg}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("LUNA 🌙"): aggiungi_al_carrello(f"Box Luna {tg}", 19.90)
    with col2:
        if st.button("SOLE ☀️"): aggiungi_al_carrello(f"Box Sole {tg}", 19.90)
    if st.button("VERSIONE PREMIUM 💎"): aggiungi_al_carrello(f"Box Premium {tg}", 29.90)

elif st.session_state.pagina == "Profilo":
    st.markdown('<h3 style="text-align:center;">Il tuo Profilo 👤</h3>', unsafe_allow_html=True)
    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card">
            <b>Genitore:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>Taglia:</b> {st.session_state.dati['taglia']}<br>
            <b>Locker:</b> {st.session_state.dati['locker']}
        </div>""", unsafe_allow_html=True)
        if st.button("MODIFICA PROFILO"): st.session_state.edit_mode = True; st.rerun()
        if st.button("LOGOUT", type="secondary"): st.session_state.user = None; st.rerun()
    else:
        with st.form("p_form"):
            n = st.text_input("Nome", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Bambino", st.session_state.dati['nome_bambino'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            if st.form_submit_button("SALVA"):
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                salva_profilo_db()
                st.session_state.edit_mode = False; st.rerun()

elif st.session_state.pagina == "Carrello":
    st.markdown('<h3 style="text-align:center;">Carrello 🛒</h3>', unsafe_allow_html=True)
    if not st.session_state.carrello: st.write("Vuoto.")
    else:
        tot = sum(i['prezzo'] for i in st.session_state.carrello)
        for i in st.session_state.carrello: st.write(f"• {i['nome']} - {i['prezzo']}€")
        st.subheader(f"Totale: {tot:.2f}€")
        if st.button("PAGA ORA"): st.success("Reindirizzamento a Stripe..."); st.session_state.carrello = []

# Pagine mancanti (Info, ChiSiamo, ecc.) seguono lo stesso schema elif...

# --- 7. BARRA DI NAVIGAZIONE FISSA ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
nav_cols = st.columns(5)
btns = [("🏠", "Home"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello")]
for i, (icon, pag) in enumerate(btns):
    with nav_cols[i]:
        if st.button(icon, key=f"n_{pag}"): vai(pag); st.rerun()
