import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE GRAFICO PULITO ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa; max-width: 500px; margin: 0 auto; }
    .stButton>button { border-radius: 25px; height: 3.5em; font-weight: bold; background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); color: white; border: none; width: 100%; }
    .step-box { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; min-height: 270px; display: flex; flex-direction: column; justify-content: center; }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 10px; }
    .step-box p { color: #333; font-size: 0.95em; line-height: 1.3; font-weight: 600; }
    .promo-card { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 20px; border-radius: 20px; border: 2px solid #d97706; margin-bottom: 20px; color: #92400e; text-align: center; }
    .alert-scadenza { background-color: #fef3c7; border-left: 10px solid #d97706; padding: 20px; border-radius: 15px; color: #92400e; font-weight: bold; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 25px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .vision-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE SESSIONE (Evita il KeyError) ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "nome": "Mamma", 
        "bimbo": "", 
        "taglia": "da definire",
        "data_ultimo_ordine": datetime.now() # Imposta una data di default
    }
if "iscritti_totali" not in st.session_state:
    st.session_state.iscritti_totali = 12

# --- LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with tab2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Il tuo Nome")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        t_c = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
        if st.button("REGISTRATI"):
            if n_m: 
                st.session_state.user_data = {"nome": n_m, "bimbo": n_b, "taglia": t_c, "data_ultimo_ordine": datetime.now()}
                st.session_state.autenticato = "utente"
                st.session_state.iscritti_totali += 1
                st.rerun()
    st.stop()

# --- MENU ---
with st.sidebar:
    st.markdown(f"### Ciao, **{st.session_state.user_data['nome']}**! 🧸")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.radio("Naviga:", menu)
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- HOME ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # Notifica 10 giorni
    scadenza = st.session_state.user_data["data_ultimo_ordine"] + timedelta(days=90)
    residui = (scadenza - datetime.now()).days
    if 0 <= residui <= 10:
        st.markdown(f'<div class="alert-scadenza">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {residui} gg alla fine del Loop. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4 style="color: #0d9488; margin-top:0;">Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare che ti fa risparmiare oltre 1.000€ l'anno seguendo la crescita del tuo bambino.</p></div>""", unsafe_allow_html=True)

    posti_o = st.session_state.iscritti_totali
    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e PRIMA BOX OMAGGIO!</p><div style="font-weight:bold;">{posti_o} / 50 posti occupati</div></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="costi-card"><h4>💰 Tariffe e Resi</h4><ul><li>🏷️ <b>Box Standard: 19,00 €</b> (Sped. Inclusa)</li><li>💎 <b>Box Premium: 29,00 €</b></li><li>🔄 <b>Reso GRATIS</b> se rinnovi la box</li></ul></div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: spedisci 10+ capi.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>10 capi igienizzati: il fabbisogno ideale.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia!</p></div>', unsafe_allow_html=True)

# --- ALTRE SEZIONI ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    for s, d in {"🌙 LUNA": "Pastello", "☀️ SOLE": "Vivace", "☁️ NUVOLA": "Casual"}.items():
        with st.expander(f"🔍 Vedi {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): 
            st.session_state.user_data["data_ultimo_ordine"] = datetime.now()
            st.success("Ordine inviato!")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"): st.balloons(); st.success("Richiesta inviata!")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra")

elif scelta == "🔐 Area Admin":
    st.title("🔐 Admin")
    st.write(f"Iscritti: {st.session_state.iscritti_totali}")
