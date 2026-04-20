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

# Fix Icona per cellulare
st.markdown("""
    <head>
        <link rel="icon" href="logo.png" type="image/png">
        <link rel="apple-touch-icon" href="logo.png">
    </head>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONE INVIO MAIL REALE ---
def invia_codice_mail(destinatario, codice, nome_mamma):
    mittente = "loopbaby000@gmail.com"
    password_app = "kqdz yeso kdyk cgsg" 
    
    corpo = f"Ciao {nome_mamma}! ✨ Benvenuta in LoopBaby. Il tuo codice di verifica è: {codice}. Inseriscilo nell'app per attivare il profilo!"
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

# --- 3. STILE GRAFICO (SCHELETRO ORIGINALE PERFETTO) ---
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
    .savings-badge { background: #0d9488; color: white !important; padding: 8px 20px; border-radius: 50px; font-weight: bold; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "verificando_mail" not in st.session_state: st.session_state.verificando_mail = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 38
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "cognome": "", "email": "", "bimbo": "Bimbo", "sesso": "Neutro",
        "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "0-1m", "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

# --- 5. LOGICA ACCESSO / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    if st.session_state.verificando_mail:
        st.title("Verifica Email 📧")
        cod_in = st.text_input("Codice di 6 cifre", key="verify_cod")
        if st.button("VERIFICA"):
            if cod_in == str(st.session_state.codice_segreto):
                st.session_state.autenticato = "utente"; st.session_state.verificando_mail = False; st.rerun()
            else: st.error("Codice errato")
        st.stop()

    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t2:
        n = st.text_input("Nome", key="r_n"); cg = st.text_input("Cognome", key="r_cg"); em = st.text_input("Email", key="r_em")
        b = st.text_input("Nome Bimbo/a", key="r_b"); sx = st.selectbox("Sesso", ["Maschietto", "Femminuccia", "Neutro"], key="r_sx")
        ps = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0, key="r_ps"); tl = st.text_input("Cellulare", key="r_tl")
        if st.button("REGISTRATI ORA"):
            if n and em and tl:
                st.session_state.codice_segreto = random.randint(100000, 999999)
                st.session_state.temp_email = em
                st.session_state.user_data.update({"nome": n, "cognome": cg, "email": em, "bimbo": b, "sesso": sx, "peso": ps, "cellulare": tl, "taglia": calcola_tg(ps)})
                if invia_codice_mail(em, st.session_state.codice_segreto, n):
                    st.session_state.verificando_mail = True; st.rerun()
    st.stop()

# --- 6. MENU SIDEBAR ---
u = st.session_state.user_data
with st.sidebar:
    st.write(f"Ciao **{u.get('nome')}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (DETTAGLIATA) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {u.get('nome')}! ✨")
    
    # CHI SIAMO
    st.markdown("""<div class="story-card"><h4>Chi Siamo? 👨‍👩‍👧</h4><p>Siamo <b>genitori</b> che capiscono la necessità di cambiare i vestiti ogni mese. Abbiamo creato LoopBaby per eliminare lo stress, lo spazio sprecato e i costi eccessivi.</p></div>""", unsafe_allow_html=True)
    
    # OBIETTIVO E PATTO 10x10
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align: center;">L'Obiettivo di LoopBaby 🌿</h3>
        <p style="text-align: center;"><b>Risparmio di Tempo, Denaro e Spazio.</b><br>Vestiti controllati con cura, con un occhio al prezzo e al pianeta.</p>
        <hr>
        <div class="highlight-box">🤝 <b>Il Patto del 10:</b> Ricevi 10 capi, rendi 10 capi. Se uno si rompe, lo sostituisci con uno simile (<b>Jeans x Jeans</b>, T-shirt x T-shirt).</div>
        <div class="highlight-box">🛡️ <b>Qualità Certificata:</b> Ogni capo è verificato singolarmente dal Team LoopBaby.</div>
    </div>
    """, unsafe_allow_html=True)

    # LOCKER & RESI
    st.markdown("""
    <div class="card">
        <h4>Consegne e Resi Smart 📦</h4>
        <p>Lavoriamo con i <b>Locker</b> vicino a casa tua: ritiri e consegni quando vuoi, senza dover aspettare il corriere a casa!</p>
        <hr>
        <p>🔄 <b>La politica del cambio:</b></p>
        <ul>
            <li><b>Entro 3 mesi:</b> Se ordini una nuova box, il reso della vecchia è <b>GRATIS</b>. Mandiamo noi l'etichetta già pagata.</li>
            <li><b>Se non rinnovi:</b> Pagherai solo un ticket di <b>7,90€</b> e ti invieremo l'etichetta per il rientro al Locker.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # PROMO
    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3><p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b>.</p></div>""", unsafe_allow_html=True)

# --- 8. PROFILO (MODIFICABILE - PENULTIMO CODICE) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        u = st.session_state.user_data
        new_n = st.text_input("Nome", u.get('nome'))
        new_cg = st.text_input("Cognome", u.get('cognome'))
        new_em = st.text_input("Email", u.get('email'))
        new_tl = st.text_input("Telefono", u.get('cellulare'))
        new_b = st.text_input("Nome Bimbo/a", u.get('bimbo'))
        
        tg_opzioni = ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"]
        tg_idx = tg_opzioni.index(u["taglia"]) if u["taglia"] in tg_opzioni else 0
        new_tg = st.selectbox("Taglia attuale bimbo/a", tg_opzioni, index=tg_idx)
        
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": new_n, "cognome": new_cg, "email": new_em, "cellulare": new_tl, "bimbo": new_b, "taglia": new_tg})
            st.success("Profilo aggiornato con successo! ✨")

# --- 9. BOX STANDARD (CAPI USATI OTTIMA QUALITÀ) ---
elif scelta == "📦 Box Standard":
    st.title(f"Box Standard - {u.get('taglia')}")
    st.info("Capi usati ma ancora di ottima qualità, selezionati uno ad uno dal Team LoopBaby.")
    for s, d in [("🌙 LUNA", "Neutri"), ("☀️ SOLE", "Vivaci"), ("☁️ NUVOLA", "Casual")]:
        with st.expander(f"{s} - Stile {d}"):
            st.write(f"Qui caricheremo le 10 foto reali per {u.get('sesso')} in taglia {u.get('taglia')}.")
            if st.button(f"Scegli Box {s}", key=f"btn_{s}"):
                st.success(f"Box {s} selezionata!")

# --- 10. BOX PREMIUM (NUOVI O SEMINUOVI) ---
elif scelta == "💎 Box Premium":
    st.title(f"Box Premium - {u.get('taglia')}")
    st.markdown('<div class="card"><b>Nuovo o Semi-nuovo:</b> Solo capi eccellenti delle migliori marche per uno stile superiore.</div>', unsafe_allow_html=True)
    st.write("Qui caricheremo le 10 foto reali della box Premium.")
    if st.button("ORDINA PREMIUM"): st.success("Premium ordinata!")

# --- 11. VETRINA (ALTA GAMMA - ACQUISTO DEFINITIVO) ---
elif scelta == "🛍️ Vetrina":
    st.title(f"Vetrina Alta Gamma")
    st.info("I capi acquistati qui rimangono tuoi! Spedizione GRATIS sopra i 50€ o associata all'acquisto di una box.")
    capi = [("Vestitino Alta Gamma", 45.0), ("Giacchino Firmato", 65.0)]
    for n, p in capi:
        st.markdown(f"<div class='card'><b>{n}</b> - <span style='color:#e11d48; font-weight:bold;'>{p}€</span></div>", unsafe_allow_html=True)
        if st.button(f"Acquista {n}", key=f"v_{n}"): st.toast(f"{n} aggiunto!")

# --- 12. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Pannello Admin 🔐")
        u = st.session_state.user_data
        if u.get('nome'):
            st.write(f"**Utente:** {u['nome']} {u['cognome']} | **Taglia:** {u['taglia']} | **Tel:** {u['cellulare']}")
            wa = urllib.parse.quote(f"Buongiorno {u['nome']}, sono di LoopBaby...")
            st.markdown(f'[![WA](https://shields.io)](https://wa.me{u["cellulare"]}?text={wa})', unsafe_allow_html=True)
