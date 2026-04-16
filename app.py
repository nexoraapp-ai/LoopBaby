import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE LOGO E ICONA ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="logo.png" if os.path.exists("logo.png") else "🧸", 
    layout="centered"
)

# --- 2. STILE GRAFICO BLINDATO (CSS) ---
st.markdown("""
    <style>
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti Moderni */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    
    /* Card e Box */
    .step-box { background-color: white !important; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; min-height: 200px; display: flex; flex-direction: column; justify-content: center; }
    .vision-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background-color: #fef3c7 !important; padding: 25px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .patto-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .nota-rossa { color: #e11d48; font-weight: 800; font-size: 1em; text-align: center; margin-bottom: 25px; border: 3px solid #e11d48; padding: 15px; border-radius: 15px; background-color: #fff1f2; }
    .legal-box { background-color: #ffffff; padding: 15px; border-radius: 15px; border: 1px solid #cbd5e1; color: #475569; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTIONE DATI E SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now() - timedelta(days=83)}

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        nm = st.text_input("Il tuo Nome")
        nb = st.text_input("Nome del Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI ORA"):
            if nm: 
                st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}
                st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. MENU LATERALE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"### Ciao {st.session_state.user_data['nome']}! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina", "⚖️ SOS & Privacy"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME ---
if scelta == "🏠 Home":
    # Notifica Scadenza
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="nota-rossa">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg alla fine dei 3 mesi. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa seguendo la crescita del tuo bimbo.</p></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="step-box"><h3>🚚 Ricevi Box</h3><p>10 capi igienizzati e stirati.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Usali e rendili entro 3 mesi!</p></div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e 1° BOX OMAGGIO (prime 50 mamme che inviano 10+ capi)</p><b>{st.session_state.iscritti} / 50 posti occupati</b><br><small>Svuota l'armadio: ci pensa LoopBaby per etichetta e costi!</small></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="patto-card"><h4>🤝 Il Patto del 10</h4><ul><li>Prendi 10, Ritorna 10.</li><li>Scambio Jeans x Jeans o penale 5€.</li></ul></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="costi-card"><h4>💰 Tariffe e Spedizioni</h4><ul><li>🏷️ Box Standard: 19€ | 💎 Premium: 29€</li><li>🔄 Reso GRATIS se rinnovi | 🚛 Vetrina: gratis > 50€</li></ul></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="nota-rossa">⚠️ RICORDA: i capi vanno resi entro 3 mesi. Se non rinnovi, il costo del reso è 7,90€.</div>""", unsafe_allow_html=True)

# --- 7. SOS & PRIVACY ---
elif scelta == "⚖️ SOS & Privacy":
    st.title("⚖️ SOS & Note Legali")
    st.info("📧 **Email Reclami:** supporto.loopbaby@gmail.com\n\n💬 **WhatsApp:** +39 [Tuo Numero]")
    st.markdown("""<div class="legal-box"><b>Privacy Policy:</b> I tuoi dati sono usati solo per le spedizioni LoopBaby e non ceduti a terzi.</div>""", unsafe_allow_html=True)

# --- ALTRE SEZIONI ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"🔍 Vedi Foto {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button(f"Ordina {s}", key=s)

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina"); st.success("Capi da tenere per sempre.")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra")

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo"); st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**"); st.write(f"Taglia: **{st.session_state.user_data['taglia']}**")
