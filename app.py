import streamlit as st
import pandas as pd
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE & ICONA ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# Fix Icona per cellulare (Apple e Android)
st.markdown("""
    <head>
        <link rel="icon" href="logo.png" type="image/png">
        <link rel="apple-touch-icon" href="logo.png">
    </head>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONE INVIO MAIL REALE ---
def invia_codice_mail(destinatario, codice, nome_mamma):
    mittente = "assistenza.loopbaby@gmail.com"
    password_app = "sqpw gpto jovf dlox" 
    corpo = f"Ciao {nome_mamma}! ✨ Il tuo codice di verifica LoopBaby è: {codice}. Inseriscilo nell'app per attivare il tuo profilo!"
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

# --- 3. STILE GRAFICO (LO SCHELETRO PERFETTO) ---
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
    .price-tag { font-weight: bold; color: #e11d48; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "verificando_mail" not in st.session_state: st.session_state.verificando_mail = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "email": "", "bimbo": "", "sesso": "Neutro",
        "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "0-1m"
    }

# --- 5. LOGICA ACCESSO / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    if st.session_state.verificando_mail:
        st.title("Verifica Email 📧")
        cod_in = st.text_input("Inserisci il codice ricevuto", key="verify_cod")
        if st.button("VERIFICA"):
            if cod_in == str(st.session_state.codice_segreto):
                st.session_state.autenticato = "utente"; st.session_state.verificando_mail = False; st.rerun()
            else: st.error("Codice errato")
        st.stop()
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e_log = st.text_input("Email", key="l_e"); p_log = st.text_input("Password", type="password", key="l_p")
        if st.button("ENTRA"):
            if e_log == "admin" and p_log == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e_log: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        n = st.text_input("Nome", key="reg_n"); em = st.text_input("Email", key="reg_em"); tl = st.text_input("Cellulare", key="reg_tl")
        if st.button("REGISTRATI"):
            if n and em and tl:
                st.session_state.codice_segreto = random.randint(100000, 999999)
                st.session_state.temp_email = em
                st.session_state.user_data.update({"nome": n, "email": em, "cellulare": tl})
                if invia_codice_mail(em, st.session_state.codice_segreto, n):
                    st.session_state.verificando_mail = True; st.rerun()
    st.stop()

# --- 6. SIDEBAR ---
u = st.session_state.user_data
u_nome = u.get('nome', 'Mamma')
with st.sidebar:
    st.write(f"Ciao **{u_nome}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u_nome}! ✨")
    st.markdown(f"""
    <div class="story-card">
        <h4>Chi Siamo? 👨‍👩‍👧</h4>
        <p>Siamo <b>genitori</b> che capiscono la necessità di cambiare i vestiti ogni mese. Abbiamo creato <b>LoopBaby</b> per eliminare lo stress e i costi eccessivi.</p>
    </div>
    <div class="card">
        <h3 style="text-align: center;">L'Obiettivo di LoopBaby 🌿</h3>
        <p style="text-align: center;"><b>Risparmio di Tempo, Denaro e Spazio.</b><br>Vestiti controllati con cura, con un occhio al prezzo e al pianeta.</p>
        <hr>
        <div class="highlight-box">🤝 <b>Il Patto del 10:</b> Ricevi 10 capi, rendi 10 capi. Se uno si rompe, sostituiscilo con uno simile (<b>Jeans x Jeans</b>).</div>
        <div class="highlight-box">🛡️ <b>Qualità Certificata:</b> Ogni capo è verificato singolarmente.</div>
        <div class="highlight-box">📦 <b>Locker Vicino a Te:</b> Ritiri e consegni quando vuoi senza aspettare il corriere.</div>
    </div>
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3>{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        new_n = st.text_input("Nome", u['nome']); new_em = st.text_input("Email", u['email'])
        new_tl = st.text_input("Telefono", u['cellulare']); new_b = st.text_input("Nome Bimbo/a", u['bimbo'])
        new_tg = st.selectbox("Taglia attuale", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": new_n, "email": new_em, "cellulare": new_tl, "bimbo": new_b, "taglia": new_tg})
            st.success("Profilo aggiornato!")

# --- 9. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title(f"Box Standard - {u.get('taglia')}")
    st.info("Capi usati in ottimo stato. Scegli lo stile:")
    for s in ["🌙 LUNA (Neutri)", "☀️ SOLE (Vivaci)", "☁️ NUVOLA (Casual)"]:
        with st.expander(s):
            st.write("Foto reali in arrivo...")
            if st.button(f"Scegli {s}"): st.success(f"Hai scelto {s}!")

# --- 10. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title(f"Box Premium - {u.get('taglia')}")
    st.info("Capi nuovi o semi-nuovi di grandi firme.")
    if st.button("ORDINA PREMIUM"): st.success("Premium ordinata!")

# --- 11. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.warning("I capi acquistati qui rimarranno a te!")
    st.markdown("<div class='card'><b>Cappottino Firmato</b> - 45€</div>", unsafe_allow_html=True)
    if st.button("Acquista"): st.toast("Aggiunto!")

# --- 12. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        st.write(f"Utente: {u['nome']} | Tel: {u['cellulare']}")
        wa = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
        st.markdown(f'[📲 WHATSAPP](https://wa.me{u["cellulare"]}?text={wa})')
