import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import datetime

# --- 1. CONNESSIONE SUPABASE (FIX 404 DEFINITIVO) ---
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def get_supabase():
    return create_client(URL_DB, KEY_DB)

supabase = get_supabase()

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA PAGINE ---

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("login"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                        st.session_state.user = res.user
                        prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
                        if prof.data: st.session_state.dati = prof.data[0]
                        vai("Home")
                    except: st.error("Dati errati")
        with t2:
            with st.form("reg"):
                er, pr = st.text_input("Email "), st.text_input("Scegli Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"):
                    try:
                        supabase.auth.sign_up({"email": er, "password": pr})
                        st.success("📩 Controlla la mail per attivare l'account!")
                    except Exception as err: st.error(f"Errore: {err}")
else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio infinito è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Partecipa ora"): vai("Info")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida LoopBaby 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Riceverai la Box entro 3-5 giorni nel Locker InPost scelto.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Quando i vestiti stringono, ordina la taglia successiva. Consegniamo la nuova e ritiriamo la vecchia insieme.</div>
        <div class="info-box"><span class="accent">📦 RESO FACILE</span><br>Metti tutto nella scatola originale e prenota il ritiro dall'app. Se continui, è GRATIS.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Lavaggio professionale igienizzante certificato per ogni capo.</div>
        """, unsafe_allow_html=True)

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    '<b>Basta sacchi di vestiti ammassati in soffitta.</b><br><br>'
                    'Siamo genitori stanchi di comprare tutine messe due volte. Abbiamo creato LoopBaby per far viaggiare '
                    'i vestiti di famiglia in famiglia, seguendo la crescita dei piccoli senza sprechi di soldi e spazio.<br><br>'
                    '<i>Insieme proteggiamo il pianeta dei nostri figli.</i> 🌿</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", p)

    elif st.session_state.pagina == "Vetrina":
        st.markdown("<h2 style='text-align:center;'>Shop 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
        if st.button("Aggiungi 🎁"): aggiungi_al_carrello("Body Bio", 9.90)

    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Profilo 👤</h2>", unsafe_allow_html=True)
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left;">
                <b>👤 Genitore:</b> {st.session_state.dati.get('nome_genitore', '---')}<br>
                <b>👶 Bambino:</b> {st.session_state.dati.get('nome_bambino', '---')}<hr>
                <b>📏 Taglia:</b> {st.session_state.dati.get('taglia', '---')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
            if st.button("LOGOUT"): supabase.auth.sign_out(); st.session_state.user = None; vai("Welcome")
        else:
            with st.form("p_edit"):
                n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
                nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
                tg = st.selectbox("Taglia", ["50-56","62-68","74-80"])
                if st.form_submit_button("SALVA"):
                    nuovi = {"id": st.session_state.user.id, "nome_genitore": n, "nome_bambino": nb, "taglia": tg}
                    supabase.table("profili").upsert(nuovi).execute()
                    st.session_state.dati = nuovi
                    st.session_state.edit_mode = False; st.rerun()

    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Carrello 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Il carrello è vuoto.")
        else:
            tot = sum(i['prezzo'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            st.markdown(f"### Totale: {tot:.2f}€")
            if st.button("PAGA ORA (STRIPE)"): st.link_button("Procedi al pagamento sicuro", "https://stripe.com")

    # BARRA NAVIGAZIONE FISSA (7 ICONE)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
            if st.button(label, key=f"n_{pag}"): vai(pag)
