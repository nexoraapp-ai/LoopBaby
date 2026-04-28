import streamlit as st
from supabase import create_client, Client
from datetime import date
import base64
import os

# --- 1. CONNESSIONE SUPABASE ---
# URL corretto per il tuo progetto izyfzqyopmpvijdtfqfe
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_9t_Psdh5tIz9OsfrSAwuMw_hJQ9i89Z"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Welcome" if not st.session_state.user else "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

# --- 3. FUNZIONI LOGICHE ---
def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        aggiorna_dati_da_db()
        vai("Home"); st.rerun()
    except: st.error("Email o Password errati. Hai confermato la mail?")

def registrazione(email, password):
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("📩 Ti abbiamo inviato una mail! Clicca sul link per attivare l'account (controlla anche in Spam).")
    except Exception as e: st.error(f"Errore: {e}")

def aggiorna_dati_da_db():
    try:
        res = supabase.table("profili").select("*").eq("id", st.session_state.user.id).execute()
        if res.data: st.session_state.dati = res.data[0]
    except: pass

def salva_profilo_db(nuovi_dati):
    try:
        nuovi_dati["id"] = st.session_state.user.id
        supabase.table("profili").upsert(nuovi_dati).execute()
        st.session_state.dati = nuovi_dati
        st.success("✅ Dati salvati online!")
    except Exception as e: st.error(f"Errore: {e}")

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 4. CSS (Look professionale + Nav Fissa) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; background-position: center; height: 130px; display: flex; align-items: center; justify-content: center; margin-bottom: 35px; border-radius: 0 0 30px 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 10px rgba(244, 63, 94, 0.1); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. PAGINE ---

# WELCOME / LOGIN
if st.session_state.user is None:
    if st.session_state.pagina == "Welcome":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Benvenuta in LoopBaby! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login"); st.rerun()
    else:
        st.markdown('<div class="header-custom"><div class="header-text">LOGIN</div></div>', unsafe_allow_html=True)
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login(e, p)
        with t2:
            with st.form("r"):
                er, pr = st.text_input("La tua migliore Email"), st.text_input("Scegli Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"): registrazione(er, pr)

# APP DOPO LOGIN
else:
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        u_nome = st.session_state.dati.get('nome_genitore', 'Genitore').split() if st.session_state.dati.get('nome_genitore') else "Mamma"
        img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;"><div><div style="font-size:28px; font-weight:800;">Ciao {u_nome}! 👋</div><div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">Cresciamo insieme, un capo alla volta, senza sprechi.</div></div><div>{img_html}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa"): vai("PromoDettaglio"); st.rerun()

    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona</h2>', unsafe_allow_html=True)
        st.markdown(f"""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
                1. <b>Le opzioni:</b> Box Standard o Premium.<br><br>
                2. <b>Scegli e ricevi:</b> Nel locker più vicino.<br><br>
                3. <b>Problemi?</b> Per aiuto <a href="/?nav=Contatti" target="_self" class="link-inline"><b>contattaci</b></a>.</div>""", unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        st.markdown('<h2 style="text-align:center;">Scegli la tua Box 📦</h2>', unsafe_allow_html=True)
        tg = st.session_state.dati.get('taglia', 'Da impostare nel profilo')
        st.markdown(f'<div style="text-align:center; margin-bottom:10px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; color:#00796b; font-weight:800;">TAGLIA: {tg}</span></div>', unsafe_allow_html=True)
        for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s} ({tg})", 19.90)

    elif st.session_state.pagina == "Vetrina":
        st.markdown('<h2 style="text-align:center;">Vetrina Shop 🛍️</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi al carrello 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

    elif st.session_state.pagina == "Carrello":
        st.markdown('<h2 style="text-align:center;">Il tuo Carrello 🛒</h2>', unsafe_allow_html=True)
        totale = sum(item['prezzo'] for item in st.session_state.carrello)
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            for item in st.session_state.carrello: st.write(f"**{item['nome']}** - {item['prezzo']}€")
            st.markdown(f"### Totale: {totale:.2f}€")
            if st.button("PROCEDI AL PAGAMENTO 💳"): st.info("Link Stripe in arrivo...")

    elif st.session_state.pagina == "Profilo":
        st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left;">
                <b>👤 Nome:</b> {st.session_state.dati.get('nome_genitore', '---')}<br>
                <b>👶 Bambino:</b> {st.session_state.dati.get('nome_bambino', '---')}<br>
                <b>📅 Nascita:</b> {st.session_state.dati.get('nascita', '---')}<br>
                <b>📞 Tel:</b> {st.session_state.dati.get('telefono', '---')}<hr>
                <b>📏 Taglia:</b> {st.session_state.dati.get('taglia', '---')}<br>
                <b>📍 Locker:</b> {st.session_state.dati.get('locker', '---')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
            if st.button("LOGOUT"): 
                supabase.auth.sign_out()
                st.session_state.user = None; st.rerun()
        else:
            with st.form("edit"):
                n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
                nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
                tel = st.text_input("Telefono", st.session_state.dati.get('telefono', ''))
                tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                lock = st.selectbox("Locker", ["Locker Esselunga", "InPost Point"])
                if st.form_submit_button("SALVA ONLINE"):
                    salva_profilo_db({"nome_genitore": n, "nome_bambino": nb, "telefono": tel, "taglia": tg, "locker": lock})
                    st.session_state.edit_mode = False; st.rerun()

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<h2 style="text-align:center;">Chi siamo? ❤️</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per semplificarti la vita e ridurre gli sprechi.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag); st.rerun()
