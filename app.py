import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (LO SCHELETRO PERFETTO) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; font-family: 'Helvetica', sans-serif; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .story-card { background: #e0f2f1; padding: 20px; border-radius: 20px; border-left: 6px solid #0d9488; margin-bottom: 20px; }
    .highlight-box { background: #f0fdfa; border-left: 5px solid #0d9488; padding: 12px; margin: 10px 0; border-radius: 0 15px 15px 0; }
    .price-tag { font-weight: bold; color: #e11d48; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "carrello_vetrina" not in st.session_state: st.session_state.carrello_vetrina = []
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "cognome": "", "email": "", "bimbo": "Bimbo", "sesso": "Neutro",
        "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "tipo_box": "", "taglia": "0-1m", "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

# --- 4. ACCESSO E REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e_log = st.text_input("Email", key="l_e")
        p_log = st.text_input("Password", type="password", key="l_p")
        if st.button("ENTRA", key="btn_l"):
            if e_log == "admin" and p_log == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e_log: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n = st.text_input("Nome", key="r_n")
        cg = st.text_input("Cognome", key="r_cg")
        em = st.text_input("Email Professionale", key="r_em")
        b = st.text_input("Nome del Bimbo/a", key="r_b")
        sx = st.selectbox("Sesso", ["Maschietto", "Femminuccia", "Neutro"], key="r_sx")
        ps = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0, key="r_ps")
        tl = st.text_input("Cellulare", key="r_tl")
        if st.button("REGISTRATI ORA", key="btn_r"):
            if n and em and tl:
                st.session_state.user_data.update({"nome": n, "cognome": cg, "email": em, "bimbo": b, "sesso": sx, "peso": ps, "cellulare": tl, "taglia": calcola_tg(ps)})
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. BENVENUTA / CONFERMA TAGLIA (FIX NOME) ---
u_nome = st.session_state.user_data.get('nome', 'Mamma')
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {u_nome}! ✨")
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h4>Taglia suggerita per {st.session_state.user_data['bimbo']}</h4>
        <div style="font-size:2.5em; font-weight:bold; color:#e11d48; margin:15px 0;">{st.session_state.user_data['taglia']}</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA", key="c_tg"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA", key="m_tg"):
        nuova = st.selectbox("Scegli taglia:", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"], key="sel_new_tg")
        if st.button("SALVA TAGLIA", key="btn_save_tg"):
            st.session_state.user_data["taglia"] = nuova
            st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU SIDEBAR ---
with st.sidebar:
    st.write(f"Ciao **{u_nome}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci", key="logout"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (SCHELETRO PERFETTO) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u_nome}! ✨")
    st.markdown(f"""
    <div class="story-card">
        <h4>Chi Siamo? 👨‍👩‍👧</h4>
        <p>Siamo <b>genitori</b> che capiscono la necessità di cambiare i vestiti ogni mese. Per questo abbiamo creato LoopBaby.</p>
    </div>
    <div class="card">
        <h3 style="text-align: center;">L'Obiettivo di LoopBaby 🌿</h3>
        <p style="text-align: center;"><b>Risparmio di Tempo, Denaro e Spazio.</b><br>Vestiti sempre della taglia giusta (0-24 mesi).</p>
        <hr>
        <div class="highlight-box">🛡️ <b>Qualità Controllata:</b> Ogni capo è verificato singolarmente dal Team LoopBaby.</div>
        <div class="highlight-box">⚡ <b>Assistenza h12:</b> Risposte garantite entro 12 ore.</div>
        <div class="highlight-box">🤝 <b>Soddisfatti o Rimborsati:</b> Problemi entro 48h? Ritiriamo tutto subito.</div>
    </div>
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b> a casa!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_p"):
        u = st.session_state.user_data
        n_p = st.text_input("Nome", u.get('nome'))
        cg_p = st.text_input("Cognome", u.get('cognome'))
        em_p = st.text_input("Email", u.get('email'))
        tl_p = st.text_input("Telefono", u.get('cellulare'))
        tg_p = st.selectbox("Taglia Attuale", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"], index=["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"].index(u["taglia"]))
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": n_p, "cognome": cg_p, "email": em_p, "cellulare": tl_p, "taglia": tg_p})
            st.success("Dati aggiornati!")

# --- 9. ALTRE SEZIONI POPOLATE ---
elif scelta == "📦 Box Standard":
    st.title(f"Box {st.session_state.user_data['sesso']} - {st.session_state.user_data['taglia']}")
    st.write("Scegli tra Luna, Sole o Nuvola (10 foto reali in arrivo).")

elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium")
    st.write("Grandi Firme per il tuo bimbo. Foto reali in arrivo.")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("Capi definitivi. Trasporto GRATIS > 50€.")

elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        st.write(f"Utente: {st.session_state.user_data['nome']} {st.session_state.user_data['cognome']}")
    else: st.error("Solo Admin")
