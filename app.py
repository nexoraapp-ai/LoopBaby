import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (SCHELETRO ORIGINALE DALLE FOTO) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .tracker-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; text-align: center; }
    .price-tag { font-weight: bold; color: #e11d48; font-size: 1.2em; }
    .savings-badge { background: #0d9488; color: white !important; padding: 5px 15px; border-radius: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "carrello_vetrina" not in st.session_state: st.session_state.carrello_vetrina = []
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "email": "", "bimbo": "", "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "tipo_box": "", "taglia": "da definire", "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

# --- 4. ACCESSO E REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e_log = st.text_input("Email", key="log_e")
        p_log = st.text_input("Password", type="password", key="log_p")
        if st.button("ENTRA", key="btn_l"):
            if e_log == "admin" and p_log == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e_log: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Nome", key="reg_n")
        cg_m = st.text_input("Cognome", key="reg_cg")
        em_m = st.text_input("Email Professionale", key="reg_e")
        n_b = st.text_input("Nome del Bimbo/a", key="reg_b")
        d_n = st.date_input("Data di Nascita", key="reg_d")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0, key="reg_p")
        c_m = st.text_input("Cellulare", key="reg_c")
        if st.button("REGISTRATI E BLOCCA PROMO", key="btn_r"):
            if n_m and cg_m and em_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "cognome": cg_m, "email": em_m, "bimbo": n_b, "nascita": d_n, "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)})
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. CONFERMA/MODIFICA TAGLIA ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Taglia suggerita per {st.session_state.user_data["bimbo"]}</h4><h2 style="color:#e11d48;">{st.session_state.user_data["taglia"]}</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA", key="c_tg"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA", key="m_tg"):
        nuova = st.selectbox("Scegli taglia:", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"], key="sel_tg")
        if st.button("SALVA", key="s_tg"): st.session_state.user_data["taglia"] = nuova; st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU ---
with st.sidebar:
    st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci", key="logout"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (COME NELLE FOTO) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    if st.session_state.user_data["ha_ordinato"]:
        g = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo</h4><h2>Giorno {g} de 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="text-align: center; margin-bottom: 20px;"><span class="savings-badge">💰 Risparmio stimato: € 1.240 / anno</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente <b>0-24 mesi</b>. Box da 19,90€ o 29,90€ con 10 capi e trasporto incluso al Locker.</p>
        <hr>
        <p>🛡️ <b>Qualità Controllata:</b><br>Ogni capo è verificato singolarmente dal Team LoopBaby per garantire igiene e qualità TOP.</p>
        <p>🤝 <b>Il Patto del 10:</b><br>Ricevi 10, rendi 10. Se un capo si rompe, sostituiscilo con uno simile (Jeans x Jeans).</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10+ capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b> a casa!</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(st.session_state.iscritti / 50)
    st.toast("Mamma Elena ha appena attivato un Loop Luna! 🌙")

# --- 8. PROFILO (MODIFICABILE) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_p"):
        u = st.session_state.user_data
        n = st.text_input("Nome", u['nome'])
        cg = st.text_input("Cognome", u['cognome'])
        em = st.text_input("Email", u['email'])
        b = st.text_input("Bimbo/a", u['bimbo'])
        tel = st.text_input("Telefono", u['cellulare'])
        tg_opzioni = ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"]
        tg_idx = tg_opzioni.index(u["taglia"]) if u["taglia"] in tg_opzioni else 0
        tg = st.selectbox("Taglia", tg_opzioni, index=tg_idx)
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": n, "cognome": cg, "email": em, "bimbo": b, "cellulare": tel, "taglia": tg})
            st.success("Dati aggiornati!")

# --- 9. BOX STANDARD (SCELTA STILI) ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("Scegli lo stile dei 10 capi per la taglia attuale:")
    for s, d in [("🌙 LUNA", "Neutri"), ("☀️ SOLE", "Vivaci"), ("☁️ NUVOLA", "Casual")]:
        with st.expander(s):
            st.write(d)
            st.write("(Caricheremo qui le 10 foto reali della box)")
            if st.button(f"Scegli {s}", key=f"btn_{s}"):
                st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now(), "tipo_box": s})
                st.success(f"Box {s} ordinata!")

# --- 10. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.write("Box esclusiva con 10 vestiti di Grandi Firme. Caricheremo qui le 10 foto reali.")
    if st.button("ORDINA PREMIUM", key="btn_prem"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now(), "tipo_box": "Premium"})
        st.success("Premium ordinata!")

# --- 11. VETRINA (ATTIVA) ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("Capi che rimangono a te. Gratis > 50€ o con una Box attiva!")
    # Lista prodotti
    capi = [("Body Bio", 15.0), ("Tutina Felpata", 25.0), ("Giacchino", 22.0)]
    for n, p in capi:
        st.markdown(f"<div class='card'><b>{n}</b> - <span class='price-tag'>{p}€</span></div>", unsafe_allow_html=True)
        if st.button(f"Acquista {n}", key=f"v_{n}"): 
            st.session_state.carrello_vetrina.append(p)
            st.toast(f"{n} aggiunto!")
    
    tot = sum(st.session_state.carrello_vetrina)
    sped = 0 if (tot >= 50 or st.session_state.user_data["ha_ordinato"]) else 7.90
    st.markdown(f"<div class='tracker-box'><b>Totale: {tot}€</b><br>Spedizione: {'GRATIS' if sped == 0 else str(sped)+'€'}</div>", unsafe_allow_html=True)

# --- 12. ADMIN (ALLERT 10GG) ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        u = st.session_state.user_data
        if u['nome']:
            data_o = u['data_ordine'].strftime('%d/%m/%Y') if u['ha_ordinato'] else "Nessun ordine"
            g = (datetime.now() - u['data_ordine']).days if u['ha_ordinato'] else 0
            st.write(f"Utente: **{u['nome']} {u['cognome']}** | Loop: Giorno {g} de 90")
            if g >= 80:
                msg = urllib.parse.quote(f"Buongiorno {u['nome']}, mancano 10gg. Preparo una nuova box?")
                st.markdown(f'[![WA](https://shields.io)](https://wa.me{u["cellulare"]}?text={msg})', unsafe_allow_html=True)
    else: st.error("Solo Admin")
