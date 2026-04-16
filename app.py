import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE UFFICIALE COL NUOVO LOGO ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="logo.png" if os.path.exists("logo.png") else "🧸", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. STILE GRAFICO BRANDIZZATO (CSS) ---
st.markdown("""
    <style>
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti con colori del logo */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    
    .step-box { background-color: white !important; padding: 20px; border-radius: 20px; border: 3px solid #7fa082; text-align: center; margin-bottom: 15px; min-height: 220px; display: flex; flex-direction: column; justify-content: center; }
    .promo-card { background-color: #fef3c7 !important; padding: 25px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .nota-rossa { color: #e11d48; font-weight: 800; font-size: 1em; text-align: center; margin-bottom: 25px; border: 3px solid #e11d48; padding: 15px; border-radius: 15px; background-color: #fff1f2; }
    .vision-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #7fa082; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATI E SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now() - timedelta(days=82)}

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #7fa082;'>🧸 LoopBaby</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa Mamma Fondatrice")
        nm = st.text_input("Il tuo Nome")
        nb = st.text_input("Nome del Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI ORA"):
            if nm: 
                st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}
                st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. MENU ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=180)
    st.write(f"### Ciao {st.session_state.user_data['nome']}! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"])
    st.write("---")
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME ---
if scelta == "🏠 Home":
    # Alert Scadenza
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="promo-card" style="background:#fff1f2; border-color:#e11d48; color:#e11d48;">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg alla fine del Loop. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4 style="color: #7fa082; margin-top:0;">Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa seguendo la crescita del tuo bimbo senza sprechi.</p></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="step-box"><h3>🚚 Ricevi Box</h3><p>10 capi igienizzati e stirati pronti all\'uso.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Usali e rendili entro 3 mesi per la nuova taglia!</p></div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e 1° BOX OMAGGIO</p><b>{st.session_state.iscritti} / 50 posti occupati</b><br><small>Svuota l'armadio: spedisci 10+ capi. LoopBaby paga tutto!</small></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="costi-card"><h4>🤝 Il Patto del 10</h4><p>Prendi 10, Ritorna 10. Se rompi/macchi un capo, cambialo (Jeans x Jeans) o penale 5€.</p><h4>💰 Tariffe e Spedizioni</h4><ul><li>🏷️ Box Standard: 19€ | 💎 Premium: 29€ (Sped. Inclusa)</li><li>🔄 Reso GRATIS se rinnovi | 🚛 Vetrina: gratis > 50€</li></ul></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="nota-rossa">⚠️ RICORDA: i capi vanno resi entro 3 mesi.<br>Se non rinnovi, il costo del reso è 7,90€.</div>""", unsafe_allow_html=True)

# (Altre sezioni Box e Vetrina rimangono uguali...)
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
    st.button("Ordina ora")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("Scegli Premium")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina"); st.info("Capi da tenere per sempre.")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo"); st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**"); st.write(f"Taglia: **{st.session_state.user_data['taglia']}**")
