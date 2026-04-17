import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (VERDE MENTA & GRIGIO FUMO) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .tracker-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; text-align: center; }
    .diff-card { background: #ffffff; padding: 15px; border-radius: 15px; border-left: 5px solid #0d9488; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .price-tag { font-weight: bold; color: #e11d48; font-size: 1.2em; }
    .savings-badge { background: #0d9488; color: white !important; padding: 5px 15px; border-radius: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "email": "", "bimbo": "", "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire", "taglia_confermata": False
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
        e_log = st.text_input("Email")
        p_log = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e_log == "admin" and p_log == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e_log: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Nome")
        cg_m = st.text_input("Cognome")
        em_m = st.text_input("Email")
        n_b = st.text_input("Nome del Bimbo/a")
        d_n = st.date_input("Data di Nascita")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        c_m = st.text_input("Cellulare")
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and em_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "cognome": cg_m, "email": em_m, "bimbo": n_b, "nascita": d_n, "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)})
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. CONFERMA TAGLIA ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Taglia suggerita per {st.session_state.user_data["bimbo"]}</h4><h2 style="color:#e11d48;">{st.session_state.user_data["taglia"]}</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA"):
        nuova = st.selectbox("Seleziona taglia:", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.button("SALVA"): st.session_state.user_data["taglia"] = nuova; st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU ---
with st.sidebar:
    st.write(f"Ciao **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (IL MANIFESTO) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    if st.session_state.user_data["ha_ordinato"]:
        g = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo</h4><h2>Giorno {g} di 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span class="savings-badge">💰 Risparmio stimato: € 1.240 / anno</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>Perché scegliere LoopBaby? 🌿</h4>
        <div class="diff-card">
            <b>💶 Risparmio Economico:</b> Vesti tuo figlio con capi di alta qualità a meno di 2€ l'uno. Risparmi oltre il 70% rispetto all'acquisto del nuovo.
        </div>
        <div class="diff-card">
            <b>⏱️ Guadagno di Tempo:</b> Dimentica le ore passate a fotografare, caricare e contrattare sui mercatini dell'usato. Con noi gestisci tutto in un unico click.
        </div>
        <div class="diff-card">
            <b>🏠 Più Spazio in Casa:</b> Basta scatole di vestiti che non vanno più bene ammucchiate in garage o negli armadi. Quando cresce, rendi e liberi spazio.
        </div>
        <div class="diff-card">
            <b>🌍 Scelta Ecologica:</b> Riduci drasticamente l'impatto ambientale e lo spreco tessile. Ogni capo ha una vita più lunga e felice.
        </div>
        <div class="diff-card">
            <b>✨ Qualità Garantita:</b> Ogni singolo capo viene controllato dal Team LoopBaby. Igiene e stato dei vestiti sono la nostra priorità.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b> a casa nostra!</p>
    </div>
    """, unsafe_allow_html=True)

# --- RESTO DEL CODICE ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        u = st.session_state.user_data
        n = st.text_input("Nome", u['nome'])
        em = st.text_input("Email", u['email'])
        tg = st.selectbox("Taglia", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"], index=["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"].index(u['taglia']))
        if st.form_submit_button("SALVA"):
            st.session_state.user_data.update({"nome": n, "email": em, "taglia": tg})
            st.success("Dati salvati!")

elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        u = st.session_state.user_data
        if u['nome']:
            st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
            msg = urllib.parse.quote(f"Ciao {u['nome']}! Novità per il tuo Loop...")
            st.markdown(f'<a href="https://wa.me{u["cellulare"]}?text={msg}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%;">📲 CONTATTA WHATSAPP</button></a>', unsafe_allow_html=True)
