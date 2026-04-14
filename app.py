import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE OTTIMIZZATA ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="🧸", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. STILE GRAFICO PERFEZIONATO (CSS) ---
st.markdown("""
    <style>
    /* Mostra testata e menu hamburger */
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Layout Mobile-First */
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti Moderni */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
        box-shadow: 0 4px 15px rgba(13,148,136,0.2);
    }
    
    /* Box Passaggi Home */
    .step-box { 
        background-color: white !important; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        min-height: 200px; display: flex; flex-direction: column; justify-content: center;
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 10px; }
    
    /* Card Promo Fondatrici */
    .promo-card { 
        background-color: #fef3c7 !important; padding: 25px; border-radius: 20px; 
        border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; 
    }
    
    /* Card Patto e Costi */
    .patto-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    
    /* Nota Rossa d'Impatto */
    .nota-rossa { 
        color: #e11d48; font-weight: 800; font-size: 1em; text-align: center; 
        margin-bottom: 25px; border: 3px solid #e11d48; padding: 15px; border-radius: 15px;
        background-color: #fff1f2;
    }
    
    /* Vision Card */
    .vision-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTIONE DATI ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now() - timedelta(days=82)}

# --- 4. ACCESSO BLOCCANTE ---
if not st.session_state.autenticato:
    st.markdown("<h1 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>L'armadio circolare per il tuo bimbo</p>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA NELL'APP"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa Mamma Fondatrice")
        nm = st.text_input("Il tuo Nome")
        nb = st.text_input("Nome del Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI E BLOCCA IL POSTO"):
            if nm: 
                st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}
                st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. NAVIGAZIONE ---
with st.sidebar:
    st.markdown(f"### Ciao {st.session_state.user_data['nome']}! 🧸")
    scelta = st.radio("Scegli dove andare:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"])
    st.write("---")
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE (IL CUORE DEL SITO) ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta nel Loop! ✨")
    
    # Alert Cambio Taglia (10 giorni)
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="promo-card" style="background:#fff1f2; border-color:#e11d48; color:#e11d48;">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg alla fine dei 3 mesi. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    # Cos'è LoopBaby
    st.markdown("""<div class="vision-card"><h4 style="color: #0d9488; margin-top:0;">Cos'è LoopBaby? 🌿</h4><p>È la scelta intelligente: <b>risparmi oltre 1.000€ l'anno</b>, liberi spazio in casa e aiuti il pianeta seguendo la crescita del tuo bambino senza sprechi.</p></div>""", unsafe_allow_html=True)

    # Passaggi Rapidi
    c1, c2 = st.columns(2)
    with c1: st.markdown('<div class="step-box"><h3>🚚 Ricevi Box</h3><p>10 capi igienizzati e stirati pronti all\'uso.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Usali e rendili entro 3 mesi per la nuova taglia!</p></div>', unsafe_allow_html=True)

    # PROMO FONDATRICI
    st.markdown(f"""
    <div class="promo-card">
        <h2 style="margin-bottom:10px;">🚀 PROMO FONDATRICI</h2>
        <p style="font-size:1.1em;"><b>Ritiro Locker GRATIS e 1° BOX OMAGGIO</b><br>per le prime 50 mamme che inviano 10 o più capi!</p>
        <div style="font-size:1.5em; font-weight:bold; margin: 15px 0;">{st.session_state.iscritti} / 50 posti occupati</div>
        <p style="text-transform: uppercase; font-weight: 800; font-size: 0.8em; border-top: 1px solid #d97706; padding-top: 10px;">
            Svuota l'armadio: spedisci 10+ capi dal Locker più vicino a te.<br>
            CI PENSA LOOPBABY PER ETICHETTA E COSTI DI SPEDIZIONE!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # PATTO DI QUALITÀ
    st.markdown("""
    <div class="patto-card">
        <h4 style="color: #0d9488; margin-top:0;">🤝 Il Patto del 10</h4>
        <ul style="margin-bottom:0; font-weight:500;">
            <li>📦 <b>Prendi 10, Ritorna 10:</b> La box va resa completa.</li>
            <li>👖 <b>Scambio Pari:</b> Se rompi/macchi un capo, cambialo (Jeans x Jeans).</li>
            <li>💰 <b>Penale:</b> Oppure 5,00 € per ogni capo mancante/danneggiato.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # TARIFFE
    st.markdown("""
    <div class="costi-card">
        <h4 style="color: #e11d48; margin-top:0;">💰 Tariffe e Spedizioni</h4>
        <ul style="margin-bottom:0; font-weight:600;">
            <li>🏷️ Box Standard: 19,00 € (Spedizione Inclusa)</li>
            <li>💎 Box Premium: 29,00 € (Spedizione Inclusa)</li>
            <li>🔄 Reso GRATIS se ordini una nuova Box</li>
            <li>🚛 Vetrina: Spedizione GRATUITA sopra i 50,00 €</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # NOTA ROSSA FINALE
    st.markdown("""<div class="nota-rossa">⚠️ RICORDA: i capi vanno resi entro un massimo di 3 mesi.<br><br>Se non ordini una nuova Box, il costo del reso è di 7,90 €. Invieremo noi l'etichetta: dovrai solo portarli al Locker.</div>""", unsafe_allow_html=True)

# --- ALTRE SEZIONI ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    st.write(f"Taglia attuale: **{st.session_state.user_data['taglia']}**")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"🔍 Vedi Foto {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Scegli {s}", key=s): st.success("Ottima scelta! Prepareremo il tuo pacco.")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium ORO (29€)")
    st.info("Selezione grandi firme: Nike, Adidas, Ralph Lauren...")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.success("✨ Capi da tenere per sempre: NO RESO!")
    st.info("🚚 Spedizione GRATIS sopra i 50,00 €")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra Scarpe")

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo Bimbo"); st.write(f"Nome: {st.session_state.user_data['bimbo']}"); st.write(f"Taglia: {st.session_state.user_data['taglia']}")
