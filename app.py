import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (SCHELETRO ORIGINALE) ---
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
    
    .card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .story-card { background: #e0f2f1; padding: 20px; border-radius: 20px; border-left: 6px solid #0d9488; margin-bottom: 20px; }
    .highlight-box { background: #f0fdfa; border-left: 5px solid #0d9488; padding: 12px; margin: 10px 0; border-radius: 0 15px 15px 0; }
    .savings-badge { background: #0d9488; color: white !important; padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "email": "", "bimbo": "", "sesso": "Neutro",
        "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "0-1m", "taglia_confermata": False
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
        e_l = st.text_input("Email", key="l_e")
        p_l = st.text_input("Password", type="password", key="l_p")
        if st.button("ENTRA", key="btn_l"):
            if e_l == "admin" and p_l == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e_l: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Entra nel mondo LoopBaby")
        n = st.text_input("Nome", key="r_n"); cg = st.text_input("Cognome", key="r_cg")
        em = st.text_input("Email Professionale", key="r_em")
        b = st.text_input("Nome del Bimbo/a", key="r_b")
        sx = st.selectbox("Sesso", ["Maschietto", "Femminuccia", "Neutro"], key="r_sx")
        ps = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0, key="r_ps")
        tl = st.text_input("Cellulare", key="r_tl")
        if st.button("REGISTRATI ORA", key="btn_r"):
            st.session_state.user_data.update({"nome": n, "cognome": cg, "email": em, "bimbo": b, "sesso": sx, "peso": ps, "cellulare": tl, "taglia": calcola_tg(ps)})
            st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. CONFERMA TAGLIA ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="card" style="text-align:center;"><h4>Taglia suggerita</h4><h2 style="color:#e11d48; font-size:2.5em;">{st.session_state.user_data["taglia"]}</h2></div>', unsafe_allow_html=True)
    if st.button("✅ CONFERMA", key="c_tg"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU SIDEBAR ---
with st.sidebar:
    u = st.session_state.user_data
    st.write(f"Mamma: **{u.get('nome')}**")
    st.write(f"Bimbo: **{u.get('bimbo')}** ({u.get('sesso')})")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci", key="logout"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u.get('nome')}! ✨")
    
    st.markdown(f'<div style="text-align: center; margin-bottom: 20px;"><span class="savings-badge">💰 Risparmio garantito: € 1.240 / anno</span></div>', unsafe_allow_html=True)

    # SEZIONE CHI SIAMO
    st.markdown(f"""
    <div class="story-card">
        <h4>Chi Siamo? 👨‍👩‍👧</h4>
        <p>Siamo prima di tutto <b>genitori</b>. Sappiamo cosa significa vedere i propri figli crescere ogni giorno e dover cambiare l'intero guardaroba ogni mese. 
        Abbiamo creato LoopBaby perché capiamo la necessità di avere abiti belli, sani e della taglia giusta, senza lo stress degli acquisti continui e dello spazio che manca.</p>
    </div>
    """, unsafe_allow_html=True)

    # OBIETTIVO E GARANZIE
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align: center;">L'Obiettivo di LoopBaby 🌿</h3>
        <p style="text-align: center; font-size: 1.1em;"><b>Risparmio di Tempo, Denaro e Spazio.</b><br>Vestiti sempre perfetti con un occhio al prezzo e al pianeta.</p>
        <hr>
        <div class="highlight-box">
            <b>🛡️ Qualità Superiore:</b><br>Non facciamo "passamano". Ogni capo è controllato e igienizzato dal Team LoopBaby per garantirti solo il meglio.
        </div>
        <div class="highlight-box">
            <b>⚡ Efficienza Reale:</b><br>Dubbi o necessità? Ti garantiamo una risposta entro <b>12 ore</b>.
        </div>
        <div class="highlight-box">
            <b>🤝 Soddisfatti o Rimborsati:</b><br>Se entro <b>48 ore</b> dalla consegna riscontri problemi, ritiriamo il pacco immediatamente. <b>Siamo unici perché siamo genitori come te.</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3></div>""", unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_p"):
        u = st.session_state.user_data
        n = st.text_input("Nome", u.get('nome')); em = st.text_input("Email", u.get('email'))
        tl = st.text_input("Telefono", u.get('cellulare'))
        if st.form_submit_button("SALVA"):
            st.session_state.user_data.update({"nome": n, "email": em, "cellulare": tl}); st.success("Dati aggiornati!")

# --- 9. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title(f"Box {u.get('sesso')} - Taglia {u.get('taglia')}")
    for s, d in [("🌙 LUNA", "Neutri"), ("☀️ SOLE", "Vivaci"), ("☁️ NUVOLA", "Casual")]:
        with st.expander(f"{s} - Stile {d}"):
            st.write(f"10 capi selezionati per {u.get('sesso')} taglia {u.get('taglia')}.")
            if st.button(f"Scegli Box {s}", key=f"btn_{s}"):
                st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
                st.success("Loop attivato!")

# --- 10. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        u = st.session_state.user_data
        if u.get('nome'):
            st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
            msg = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
            st.markdown(f'[![WA](https://shields.io)](https://wa.me{u["cellulare"]}?text={msg})', unsafe_allow_html=True)
