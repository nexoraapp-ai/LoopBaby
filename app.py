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
    corpo = f"Ciao {nome_mamma}! ✨ Il tuo codice di verifica LoopBaby è: {codice}. Inseriscilo nell'app!"
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

# --- 3. STILE GRAFICO COMPLETO ---
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
if "verificando_mail" not in st.session_state: st.session_state.verificando_mail = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "email": "", "cellulare": "", "bimbo": "", "taglia": "0-1m"}

# --- 5. ACCESSO / REGISTRAZIONE ---
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
    st.write(f"Ciao **{u['nome']}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin", "✉️ Contatti"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME (TUTTI I TESTI) ---
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

# --- 8. CONTATTI ---
elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.markdown(f"""
    <a href="mailto:assistenza.loopbaby@gmail.com" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px; border-radius: 15px; cursor: pointer; width: 100%; font-weight: bold;">
            📩 Inviaci un'email: assistenza.loopbaby@gmail.com
        </button>
    </a>
    """, unsafe_allow_html=True)

# --- 9. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Admin 🔐")
    st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
    wa_msg = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
    st.markdown(f'[📲 WHATSAPP](https://wa.me{u["cellulare"]}?text={wa_msg})')

# (Altre sezioni Box e Vetrina rimangono come da tuo scheletro)
