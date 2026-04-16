import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE MASTER ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. IL MOTORE GRAFICO (CSS TOTALE) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Forza testo scuro */
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #0d9488 !important; }
    
    /* Pulsanti */
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
    }
    
    /* Card */
    .vision-card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .costi-card { background: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; margin-bottom: 20px; }
    .step-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; text-align: center; margin-bottom: 10px; }
    
    /* Alert Push */
    .alert-push { background-color: #fff1f2 !important; border: 2px solid #e11d48; padding: 20px; border-radius: 20px; color: #e11d48 !important; text-align: center; font-weight: 800; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INIZIALIZZAZIONE SESSIONE (IMPORTANTE: RISOLVE I BUG) ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "bimbo": "", "cellulare": "", 
        "taglia": "da definire", "data_ordine": None, "ha_ordinato": False
    }

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            else: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa Mamma Fondatrice")
        n_m = st.text_input("Il tuo Nome")
        c_m = st.text_input("Tuo Cellulare (es. 39347...)")
        n_b = st.text_input("Nome Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 18.0, 5.0)
        if st.button("REGISTRATI ORA"):
            if n_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "cellulare": c_m, "bimbo": n_b})
                st.session_state.autenticato = "utente"
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 5. MENU LATERALE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"### Ciao {st.session_state.user_data['nome']}! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE ---
if scelta == "🏠 Home":
    st.title("Benvenuta nel Loop! ✨")
    
    # LOGICA NOTIFICA (Solo se ha ordinato e mancano <= 7gg)
    if st.session_state.user_data["ha_ordinato"] and st.session_state.user_data["data_ordine"]:
        scadenza = st.session_state.user_data["data_ordine"] + timedelta(days=90)
        res = (scadenza - datetime.now()).days
        if 0 <= res <= 7:
            st.markdown(f'<div class="alert-push">🔔 NOTIFICA: Mancano esattamente {res} gg alla fine del Loop. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa seguendo la crescita del tuo bimbo passo dopo passo.</p></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1: st.markdown('<div class="step-box"><h3>🚚 Ricevi Box</h3><p>10 capi igienizzati e stirati pronti all\'uso.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi i capi per il cambio taglia o acquistali!</p></div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e 1° BOX OMAGGIO (prime 50 mamme che inviano 10+ capi)</p><b>{st.session_state.iscritti} / 50 posti occupati</b></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="costi-card"><h4>💰 Tariffe e Spedizioni</h4><ul><li>🏷️ Box Standard: 19€ | 💎 Premium: 29€ (Sped. Inclusa)</li><li>🔄 Reso GRATIS se rinnovi</li></ul></div>""", unsafe_allow_html=True)

# --- 7. PROFILO ---
elif scelta == "📝 Profilo Bimbo":
    st.title("Il tuo Profilo 📝")
    st.subheader(f"Mamma: {st.session_state.user_data['nome']}")
    st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**")
    st.write(f"Taglia calcolata: **{st.session_state.user_data['taglia']}**")

# --- 8. BOX STANDARD ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19,00 €)")
    st.write("Scegli lo stile della tua Box da 10 capi:")
    for s, d in {"🌙 LUNA": "Toni pastello e delicati", "☀️ SOLE": "Colori vivaci e allegri", "☁️ NUVOLA": "Casual e pratico"}.items():
        with st.expander(f"🔍 Vedi dettagli {s}"):
            st.write(d)
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s):
            st.session_state.user_data["ha_ordinato"] = True
            st.session_state.user_data["data_ordine"] = datetime.now()
            st.success(f"Ordine {s} confermato!")

# --- 9. BOX PREMIUM ---
elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29,00 €)")
    st.info("Grandi firme selezionate (Nike, Adidas, Ralph Lauren...)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"):
        st.session_state.user_data["ha_ordinato"] = True
        st.session_state.user_data["data_ordine"] = datetime.now()
        st.balloons()

# --- 10. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.success("✨ Capi da tenere per sempre. Spedizione gratis > 50€")
    if os.path.exists("scarpe.jpg"):
        st.image("scarpe.jpg")
        st.button("Aggiungi al carrello")

# --- 11. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Area Gestione 🔐")
    st.write(f"Iscritti totali: {st.session_state.iscritti}")
    nome = st.session_state.user_data["nome"]
    tel = st.session_state.user_data["cellulare"]
    if tel:
        msg = urllib.parse.quote(f"Ciao {nome}! 😊 Sono di LoopBaby...")
        st.markdown(f'<a href="https://wa.me{tel}?text={msg}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%;">📲 CONTATTA MAMMA</button></a>', unsafe_allow_html=True)
    else:
        st.warning("Nessun numero di cellulare registrato per questo test.")
