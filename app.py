import streamlit as st
import pandas as pd
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import urllib.parse

# --- 1. CONFIGURAZIONE & ICONA ---
st.set_page_config(page_title="LoopBaby", page_icon="🍼", layout="centered")

# --- 2. FUNZIONE INVIO MAIL REALE ---
def invia_codice_mail(destinatario, codice, nome_mamma):
    mittente = "assistenza.loopbaby@gmail.com"
    password_app = "sqpw gpto jovf dlox" 
    corpo = f"Ciao {nome_mamma}! ✨ Il tuo codice di verifica LoopBaby è: {codice}."
    messaggio = MIMEText(corpo)
    messaggio['Subject'] = 'Codice di Verifica LoopBaby 🧸'
    messaggio['From'] = f"LoopBaby <{mittente}>"
    messaggio['To'] = destinatario
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mittente, password_app)
        server.sendmail(mittente, destinatario, messaggio.as_string())
        server.quit()
        return True
    except:
        return False

# --- 3. STILE GRAFICO ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; width: 100% !important;
    }
    .card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .story-card { background: #e0f2f1; padding: 20px; border-radius: 20px; border-left: 6px solid #0d9488; margin-bottom: 20px; }
    .highlight-box { background: #f0fdfa; border-left: 5px solid #0d9488; padding: 12px; margin: 10px 0; border-radius: 0 15px 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "verificando_mail" not in st.session_state: st.session_state.verificando_mail = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "email": "", "cellulare": "", "bimbo": "", "taglia": "0-1m"}

# --- 5. LOGICA ACCESSO (Semplificata per il test) ---
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
        st.write("Inserisci i dati per entrare")
        if st.button("ACCESSO DI PROVA"): st.session_state.autenticato = "utente"; st.rerun()
    st.stop()

# --- 6. SIDEBAR ---
u = st.session_state.user_data
with st.sidebar:
    st.write(f"Ciao **{u['nome']}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin", "✉️ Contatti"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u['nome']}! ✨")
    st.markdown(f"""
    <div class="story-card">
        <h4>Chi Siamo? 👨‍👩‍👧</h4>
        <p>Siamo <b>genitori</b> che capiscono la necessità di cambiare i vestiti ogni mese. Abbiamo creato <b>LoopBaby</b> per eliminare lo stress e i costi eccessivi.</p>
    </div>
    <div class="card">
        <h3 style="text-align: center;">L'Obiettivo di LoopBaby 🌿</h3>
        <p style="text-align: center;"><b>Risparmio di Tempo, Denaro e Spazio.</b><br>Vestiti controllati con cura, con un occhio al prezzo e al pianeta.</p>
        <hr>
        <div class="highlight-box">🤝 <b>Il Patto del 10:</b> Ricevi 10 capi, rendi 10 capi.</div>
        <div class="highlight-box">🛡️ <b>Qualità Certificata:</b> Ogni capo è verificato singolarmente.</div>
        <div class="highlight-box">📦 <b>Locker Vicino a Te:</b> Ritiri e consegni quando vuoi.</div>
    </div>
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3>{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard")
    st.info("Scegli lo stile della tua Box Mensile (10 capi):")
    for stile in ["🌙 LUNA (Neutri)", "☀️ SOLE (Vivaci)", "☁️ NUVOLA (Casual)"]:
        with st.expander(stile):
            st.write(f"Stile {stile} selezionato per la taglia {u['taglia']}")
            if st.button(f"Sottoscrivi {stile}"): st.success("Richiesta inviata!")

# --- 9. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium")
    st.write("Brand di alta gamma per il tuo bambino.")
    st.image("https://placehold.co", caption="Esempio Premium")
    if st.button("ORDINA PREMIUM (89€)"): st.success("Benvenuta nel club Premium!")

# --- 10. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.warning("I capi acquistati qui rimarranno a te!")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placehold.co", caption="Cappottino Firmato")
        st.write("**Prezzo: 45€**")
        if st.button("Acquista ora"): st.success("Aggiunto!")

# --- 11. CONTATTI ---
elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.markdown(f"""
    <a href="mailto:assistenza.loopbaby@gmail.com" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px; border-radius: 15px; cursor: pointer; width: 100%; font-weight: bold; font-size: 16px;">
            📩 Inviaci un'email ora
        </button>
    </a>
    """, unsafe_allow_html=True)
    st.info("Rispondiamo solitamente entro 24 ore.")

# --- 12. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Admin 🔐")
    st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
    wa_msg = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
    st.markdown(f'[📲 WHATSAPP](https://wa.me{u["cellulare"]}?text={wa_msg})')

elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo")
    st.write(f"Nome: {u['nome']}")
    st.write(f"Email: {u['email']}")
