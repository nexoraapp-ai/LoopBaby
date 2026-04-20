import streamlit as st
import pandas as pd
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🍼", layout="centered")

# --- 2. FUNZIONE INVIO MAIL ---
def invia_codice_mail(destinatario, codice, nome_mamma):
    mittente = "assistenza.loopbaby@gmail.com"
    password_app = "sqpw gpto jovf dlox" 
    corpo = f"Ciao {nome_mamma}! ✨ Il tuo codice di verifica LoopBaby è: {codice}."
    messaggio = MIMEText(corpo)
    messaggio['Subject'] = 'Codice di Verifica LoopBaby 🧸'
    messaggio['From'] = f"LoopBaby <{mittente}>"
    messaggio['To'] = destinatario
    try:
        server = smtplib.SMTP_SSL('://gmail.com', 465)
        server.login(mittente, password_app)
        server.sendmail(mittente, destinatario, messaggio.as_string())
        server.quit()
        return True
    except:
        return False

# --- 3. STILE GRAFICO ---
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
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "email": "", "cellulare": "", "bimbo": "", "taglia": "0-1m"}

# --- 5. LOGICA ACCESSO ---
if not st.session_state.autenticato:
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t2:
        n = st.text_input("Nome"); em = st.text_input("Email"); tl = st.text_input("Cellulare")
        if st.button("REGISTRATI"):
            st.session_state.codice_segreto = random.randint(100000, 999999)
            if invia_codice_mail(em, st.session_state.codice_segreto, n):
                st.session_state.user_data.update({"nome": n, "email": em, "cellulare": tl})
                st.session_state.verificando_mail = True; st.rerun()
    with t1:
        if st.button("ACCESSO RAPIDO"): st.session_state.autenticato = "utente"; st.rerun()
    st.stop()

# --- 6. SIDEBAR ---
u = st.session_state.user_data
with st.sidebar:
    st.write(f"Ciao **{u['nome']}**! 🧸")
    scelta = st.sidebar.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin", "✉️ Contatti"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME ---
if scelta == "🏠 Home":
    st.title("Benvenuta su LoopBaby ✨")
    
    st.markdown("""
    <div class="story-card">
        <h4>Come funziona LoopBaby? 🔄</h4>
        <p>LoopBaby è l'economia circolare per il tuo bambino. Quando i vestiti diventano piccoli, li sostituiamo con la taglia successiva senza sprechi.</p>
    </div>
    <div class="card">
        <h3 style="text-align: center;">🤝 Il Patto del 10</h3>
        <p style="text-align: center;">Ricevi <b>10 capi</b> curati, rendi <b>10 capi</b> usati. Se un capo si rompe, lo sostituisci con uno simile (es. Jeans con Jeans).</p>
    </div>
    <div class="card">
        <h4 style="text-align: center;">🚚 Spedizioni e Resi</h4>
        <div class="highlight-box">📦 <b>Spedizione Gratuita:</b> La consegna della tua Box è sempre inclusa.</div>
        <div class="highlight-box">🔄 <b>Reso Gratuito:</b> Se ordini una nuova Box, il ritiro di quella vecchia è gratuito!</div>
        <div class="highlight-box">🏷️ <b>Etichetta di Reso:</b> Se vuoi solo restituire i capi senza prendere una nuova Box, il costo è di 7,90€ e ti inviamo noi l'etichetta.</div>
    </div>
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3>38 / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        new_n = st.text_input("Nome", u['nome'])
        new_tl = st.text_input("Cellulare", u['cellulare'])
        new_b = st.text_input("Nome Bimbo/a", u['bimbo'])
        new_tg = st.selectbox("Taglia attuale", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": new_n, "cellulare": new_tl, "bimbo": new_b, "taglia": new_tg})
            st.success("Profilo aggiornato!")

# --- 9. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard")
    st.write("Vestiti usati in **ottimo stato**, selezionati e igienizzati.")
    for s in ["🌙 LUNA (Neutri)", "☀️ SOLE (Vivaci)", "☁️ NUVOLA (Casual)"]:
        with st.expander(s):
            if st.button(f"Scegli {s}"): st.success(f"Hai scelto lo stile {s}!")

# --- 10. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium")
    st.write("Vestiti **nuovi o seminuovi** dei migliori brand, selezionati e igienizzati.")
    if st.button("ORDINA PREMIUM (89€)"): st.success("Ordine Premium ricevuto!")

# --- 11. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    st.info("I capi acquistati in questa sezione rimangono a te.")
    st.markdown("""
    <div class="highlight-box">
    🚛 <b>Spedizione Gratuita:</b> Per ordini superiori a 50€ o se acquistati insieme a una Box.
    </div>
    """, unsafe_allow_html=True)
    st.write("---")
    st.image("https://placehold.co", caption="Esempio Prodotto")
    if st.button("Acquista (45€)"): st.success("Aggiunto!")

# --- 12. CONTATTI ---
elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.markdown(f"""
    <a href="mailto:assistenza.loopbaby@gmail.com" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px; border-radius: 15px; cursor: pointer; width: 100%; font-weight: bold;">
            📩 Inviaci un'email ora
        </button>
    </a>
    """, unsafe_allow_html=True)

# --- 13. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Admin 🔐")
    st.write(f"Contatta: {u['nome']} ({u['cellulare']})")
    wa = urllib.parse.quote(f"Ciao {u['nome']}, sono LoopBaby...")
    st.markdown(f'[📲 WHATSAPP](https://wa.me{u["cellulare"]}?text={wa})')
