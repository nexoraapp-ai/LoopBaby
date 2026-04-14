import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE GRAFICO (CSS) ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa; }
    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%; 
    }
    .step-box { 
        background-color: #ffffff; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        min-height: 270px; display: flex; flex-direction: column; justify-content: center;
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 10px; }
    .step-box p { color: #333; font-size: 0.95em; line-height: 1.3; font-weight: 600; }
    
    .promo-card { 
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
        padding: 20px; border-radius: 20px; border: 2px solid #d97706; 
        margin-bottom: 20px; color: #92400e; text-align: center;
    }
    .counter-badge { background-color: #d97706; color: white; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 1.2em; display: inline-block; margin-top: 10px; }
    .costi-card { background-color: #fff1f2; padding: 25px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .vetrina-card { background-color: #ffffff; padding: 15px; border-radius: 15px; border: 1px solid #0d9488; margin-bottom: 20px; text-align: center; }
    .free-ship-badge { background-color: #059669; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8em; display: inline-block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- STATO APPLICAZIONE ---
if "iscritti_totali" not in st.session_state: st.session_state.iscritti_totali = 12 
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire"}

# --- 1. SCHERMATA LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with tab2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Il tuo Nome")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        t = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
        if st.button("REGISTRATI E BLOCCA IL POSTO"):
            if n_m: 
                st.session_state.user_data = {"nome": n_m, "bimbo": n_b, "taglia": t}
                st.session_state.autenticato = "utente"
                st.session_state.iscritti_totali += 1
                st.rerun()
    st.stop()

# --- 2. MENU LATERALE ---
with st.sidebar:
    st.markdown(f"### Ciao, **{st.session_state.user_data['nome']}**! 🧸")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.radio("Naviga:", menu)
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 3. SEZIONI ---

if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    p_rimasti = 50 - st.session_state.iscritti_totali
    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e PRIMA BOX OMAGGIO!</p><div class="counter-badge">{st.session_state.iscritti_totali} / 50 posti</div><p style="margin-top:10px; font-weight:bold;">Restano solo {p_rimasti} posti!</p></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="costi-card">
        <h4>💰 Tariffe e Resi</h4>
        <ul>
            <li>🏷️ <b>Box Standard: 19,00 €</b> (Sped. Inclusa).</li>
            <li>💎 <b>Box Premium: 29,00 €</b> (Sped. Inclusa).</li>
            <li>🚛 <b>Vetrina:</b> Spedizione <b>OMAGGIO</b> se superi i 50,00 €!</li>
            <li>🔄 <b>Reso GRATIS:</b> Se rinnovi la box.</li>
            <li>🎟️ <b>Reso Singolo:</b> Ticket a <b>7,90 €</b>.</li>
            <li>⏳ <b>Durata:</b> Reso entro <b>3 mesi</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="step-box"><h3>📦 Inviaci i tuoi capi</h3><p>Svuota l\'armadio: spedisci 10 o più capi al Locker.</p></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>10 capi igienizzati: il fabbisogno settimanale ideale.</p></div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia! Reso gratis se rinnovi.</p></div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("👤 Profilo Bimbo")
    st.write(f"Nome: **{st.session_state.user_data['bimbo']}**")
    st.write(f"Taglia attuale: **{st.session_state.user_data['taglia']}**")

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    for s, d in {"🌙 LUNA": "Delicato e pastello", "☀️ SOLE": "Vivace e allegro", "☁️ NUVOLA": "Casual e pratico"}.items():
        st.markdown(f"### {s}")
        st.write(d)
        with st.expander(f"🔍 Vedi Foto {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): st.success(f"Ordine {s} inviato!")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29,00 €)")
    st.write("Grandi firme selezionate (Nike, Adidas, Ralph Lauren...)")
    with st.expander("🔍 Vedi Foto Premium"):
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"): st.balloons(); st.success("Richiesta Premium inviata!")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.markdown("""
    <div style="background-color: #e0f2fe; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: #0c4a6e; text-align: center;">
        ✨ <b>Compra e Tieni:</b> Questi capi sono tuoi per sempre!<br>
        🚚 <b style="color: #059669;">SPEDIZIONE GRATUITA per ordini superiori a 50,00 €</b>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="vetrina-card">', unsafe_allow_html=True)
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
        st.write("**Scarpe Sportive Firmate**")
        st.write("Prezzo: **14,90 €**")
        if st.button("Aggiungi al carrello", key="v1"): st.success("Aggiunto!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="vetrina-card">', unsafe_allow_html=True)
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.write("**Set Coordinato Invernale**")
        st.write("Prezzo: **19,50 €**")
        if st.button("Aggiungi al carrello", key="v2"): st.success("Aggiunto!")
        st.markdown('</div>', unsafe_allow_html=True)

elif scelta == "🔐 Area Admin":
    st.title("🔐 Admin")
    st.write(f"Iscritti: {st.session_state.iscritti_totali}")
