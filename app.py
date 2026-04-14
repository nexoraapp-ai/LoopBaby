import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE E ICONA ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="🧸", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. BLOCCO ZOOM E STILE APP (Mobile First - Stile Instagram) ---
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* Nasconde elementi Streamlit per sembrare un'app reale */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Centratura e colori */
    .stApp { background-color: #f0fdfa; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti Moderni */
    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%; 
    }
    
    /* Box Passaggi */
    .step-box { 
        background-color: #ffffff; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; }
    
    /* Card Risparmio */
    .savings-card { 
        background-color: #d1fae5; padding: 20px; border-radius: 20px; 
        border: 2px dashed #059669; text-align: center; margin-bottom: 20px; 
        color: #065f46; 
    }
    
    /* Card Promozioni */
    .promo-card { 
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); 
        padding: 25px; border-radius: 20px; border-left: 10px solid #0369a1; 
        margin-bottom: 20px; color: #0c4a6e; 
    }
    
    /* Patto Qualità */
    .patto-card { 
        background-color: #fff1f2; padding: 20px; border-radius: 15px; 
        border: 2px solid #e11d48; color: #333; margin-bottom: 20px;
    }
    
    /* Sigillo Premium */
    .sigillo-oro { 
        background-color: #fef3c7; color: #92400e; padding: 5px 15px; 
        border-radius: 50px; font-weight: bold; font-size: 0.8em; 
        border: 2px solid #b45309; display: inline-block; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTIONE LOGIN ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown("<h1 style='text-align: center;'>🧸 LoopBaby</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>L'armadio del tuo bimbo a poco prezzo e sostenibile</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email", placeholder="tua@email.com")
        p = st.text_input("Password", type="password", placeholder="******")
        if st.button("ENTRA NELL'APP"):
            if e == "admin" and p == "baby2024":
                st.session_state.autenticato = "admin"
                st.rerun()
            elif e and p:
                st.session_state.autenticato = "utente"
                st.rerun()
    with tab2:
        st.write("### Diventa una Mamma Fondatrice")
        st.write("Iscriviti ora per bloccare la promo: Ritiro Locker Gratis + 1° Box Omaggio!")
        st.text_input("Inserisci Email")
        st.text_input("Crea una Password", type="password")
        if st.button("REGISTRATI GRATIS"):
            st.success("Registrazione completata! Ora effettua l'accesso.")
    st.stop()

# --- 4. POP-UP VALORI (Solo al primo accesso) ---
@st.dialog("Perché LoopBaby? 🌿")
def pop_up_valori():
    st.markdown("### Circolarità e Risparmio")
    st.write("Scegliere LoopBaby significa cura per il pianeta e per il tuo portafoglio:")
    st.info("🌍 **Ambiente:** Riduciamo i rifiuti tessili.\n\n💰 **Risparmio:** Oltre 1.000€ risparmiati ogni anno rispetto al nuovo.")
    if st.button("Ho capito, iniziamo! ✨"):
        st.session_state.mostra_valori = False
        st.rerun()

if "mostra_valori" not in st.session_state:
    st.session_state.mostra_valori = True

# --- 5. MENU LATERALE ---
with st.sidebar:
    st.markdown("### 🧸 Menu LoopBaby")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina", "🔄 Restituisci Box"]
    if st.session_state.autenticato == "admin":
        menu.append("🔐 Area Admin")
    
    scelta = st.radio("Navigazione:", menu)
    st.write("---")
    if st.button("Esci dall'account"):
        st.session_state.autenticato = False
        st.rerun()

# --- 6. SEZIONI ---

# --- HOME ---
if scelta == "🏠 Home":
    if st.session_state.mostra_valori:
        pop_up_valori()
        
    st.title("🌿 Benvenuti nel Loop")
    
    st.markdown("""
    <div class="savings-card">
        <h3>💰 Risparmio Annuale: ~1.048 €</h3>
        <p>Vesti la crescita (0-24m) senza lo stress di dover ricomprare tutto ogni mese.</p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="step-box"><h1>📦</h1><h3>Inviaci i tuoi capi</h3></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="step-box"><h1>🚚</h1><h3>Ricevi la Box</h3></div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="step-box"><h1>🔄</h1><h3>Scambia</h3></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI (Max 50)</h2>
        <p><b>Ritiro Locker GRATIS</b> (paga LoopBaby) e <b>PRIMA BOX OMAGGIO</b> se spedisci i tuoi primi 10+ capi entro 30 giorni!</p>
    </div>
    """, unsafe_allow_html=True)

# --- BOX STANDARD ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19,00 €)")
    st.markdown("""
    <div style="background-color: #ecfdf5; padding: 15px; border-radius: 15px; border: 1px solid #10b981; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 24px;">💨</span> <b>SANIFICAZIONE A VAPORE</b><br>
        <small>Trattamento ad alta temperatura sicuro per i neonati.</small>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🛡️ Patto della Macchia (Garanzia)"):
        st.write("Sappiamo che i bimbi si sporcano! Le macchie d'uso quotidiano (pappa, erba) sono coperte da noi. Ti chiediamo cura, ma non ansia!")

    with st.form("ordine_std"):
        st.subheader("Personalizza la tua Box")
        genere = st.radio("Genere:", ["Maschietto", "Femminuccia", "Neutro"], horizontal=True)
        stagione = st.select_slider("Stagione:", options=["Invernale", "Mezza Stagione", "Estiva"])
        
        st.write("---")
        st.write("### Anteprima capi disponibili:")
        if os.path.exists("vestiti.jpg"): 
            st.image("vestiti.jpg", caption="Esempio capi per la tua taglia")
        else: 
            st.info("Qui appariranno le foto dei tuoi capi reali appena caricati su GitHub.")
        
        if st.form_submit_button("ORDINA BOX STANDARD (19€)"):
            st.balloons()
            st.success("Ordine ricevuto! Riceverai l'etichetta di reso su WhatsApp.")

# --- BOX PREMIUM ---
elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29,00 €)")
    st.markdown('<div class="sigillo-oro">✨ QUALITÀ ORO: Grandi Firme</div>', unsafe_allow_html=True)
    st.write("\nSelezione esclusiva di capi (es. Nike, Adidas, Ralph Lauren) sanificati a vapore.")
    
    with st.form("ordine_pre"):
        st.radio("Genere:", ["Maschietto", "Femminuccia", "Neutro"], horizontal=True)
        st.write("---")
        if os.path.exists("scarpe.jpg"): 
            st.image("scarpe.jpg", caption="Esempio capi Alta Gamma")
        if st.form_submit_button("ORDINA BOX PREMIUM (29€)"):
            st.balloons()
            st.success("Ordine Premium ricevuto!")

# --- VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("I capi acquistati in questa sezione non devono essere restituiti.")
    if os.path.exists("scarpe.jpg"):
        st.image("scarpe.jpg", caption="Scarpe Nike/Adidas - Prezzo in chat")
    if os.path.exists("vestiti.jpg"):
        st.image("vestiti.jpg", caption="Set coordinati")

# --- AREA ADMIN ---
elif scelta == "🔐 Area Admin":
    st.title("Pannello Gestione LoopBaby")
    st.write("Benvenuta! Qui vedrai chi ha ordinato e chi deve rendere la box.")
    # Caricamento database futuro
