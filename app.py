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
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    .stButton>button { 
        border-radius: 30px !important; background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; width: 100% !important; font-weight: 800 !important;
    }
    .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .story-card { background: #e0f2f1; padding: 20px; border-radius: 20px; border-left: 6px solid #0d9488; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "verificando_mail" not in st.session_state: st.session_state.verificando_mail = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "email": "", "cellulare": "", "bimbo": "", "taglia": "0-1m"}

# --- 5. LOGICA ACCESSO ---
if not st.session_state.autenticato:
    if st.session_state.verificando_mail:
        st.title("Verifica Email 📧")
        cod_in = st.text_input("Codice ricevuto")
        if st.button("VERIFICA"):
            if cod_in == str(st.session_state.codice_segreto):
                st.session_state.autenticato = "utente"; st.rerun()
        st.stop()
    
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t2:
        n = st.text_input("Nome"); em = st.text_input("Email"); tl = st.text_input("Cellulare")
        if st.button("REGISTRATI"):
            st.session_state.codice_segreto = random.randint(100000, 999999)
            if invia_codice_mail(em, st.session_state.codice_segreto, n):
                st.session_state.user_data.update({"nome": n, "email": em, "cellulare": tl})
                st.session_state.verificando_mail = True; st.rerun()
    st.stop()

# --- 6. SIDEBAR ---
u = st.session_state.user_data
with st.sidebar:
    st.title("Naviga:")
    scelta = st.radio("", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin", "✉️ Contatti"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. LOGICA PAGINE ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u['nome']}! ✨")
    st.markdown("""
    <div class="story-card">
        <h4>Chi Siamo? 👨‍👩‍👧</h4>
        <p>Siamo genitori che eliminano lo stress e i costi eccessivi del cambio vestiti mensile.</p>
    </div>
    """, unsafe_allow_html=True)

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.markdown("<div class='card'><b>Cappottino Firmato</b> - 45€</div>", unsafe_allow_html=True)
    if st.button("Acquista"): st.success("Aggiunto al carrello!")

elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.write("Hai bisogno di aiuto? Clicca il tasto rosso sotto.")
    st.markdown(f"""
    <a href="mailto:assistenza.loopbaby@gmail.com" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px; border-radius: 15px; cursor: pointer; width: 100%; font-weight: bold;">
            📩 Inviaci un'email: assistenza.loopbaby@gmail.com
        </button>
    </a>
    """, unsafe_allow_html=True)

elif scelta == "🔐 Admin":
    st.title("Admin 🔐")
    st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
    wa_msg = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
    st.markdown(f'[📲 CONTATTA SU WHATSAPP](https://wa.me{u["cellulare"]}?text={wa_msg})')
