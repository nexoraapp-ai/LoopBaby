import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- CONFIGURAZIONE PROFESSIONALE ---
st.set_page_config(page_title="LoopBaby - Moda Circolare", page_icon="🧸", layout="wide")

# --- FUNZIONE POP-UP VALORI ---
@st.dialog("Perché scegliere LoopBaby? 🌿")
def pop_up_valori():
    st.markdown("### Il nostro principio: Circolarità e Risparmio")
    st.write("Entrare in LoopBaby significa fare una scelta consapevole per te e per il pianeta:")
    st.info("""
    🌍 **Impatto Ambientale:** Riduciamo drasticamente i rifiuti tessili. Ogni capo rimesso in circolo risparmia migliaia di litri d'acqua.
    
    💰 **Risparmio Economico:** Vesti il tuo bimbo con capi di qualità a una frazione del costo del nuovo. Risparmi centinaia di euro ogni anno.
    """)
    if st.button("Ho capito, iniziamo! ✨"):
        st.session_state.mostra_valori = False
        st.rerun()

if "sessione_avviata" not in st.session_state:
    st.session_state.sessione_avviata = True
    st.session_state.mostra_valori = True

def salva_dati(nuovi_dati):
    file_nome = 'iscrizioni_loopbaby.csv'
    df = pd.DataFrame([nuovi_dati])
    if not os.path.isfile(file_nome):
        df.to_csv(file_nome, index=False)
    else:
        df.to_csv(file_nome, mode='a', header=False, index=False)

# --- STILE GRAFICO AD ALTA LEGGIBILITÀ (VERDE/BLU) + LOGO ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdfa; }
    
    /* Logo Stilizzato Orsetto */
    .logo-container { text-align: center; padding: 10px; }
    .logo-text { font-family: 'Helvetica Neue', sans-serif; color: #0d9488; font-size: 38px; font-weight: 800; letter-spacing: -1px; margin-bottom: 0px; }
    .logo-sub { color: #0369a1; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: -5px; }

    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%;
    }
    .step-box { 
        background-color: #ffffff; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px;
        min-height: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .step-box h3 { color: #0d9488; font-weight: 900; margin-top: 10px; font-size: 1.3em; }
    .step-box p { color: #000000; font-weight: 600; font-size: 1.1em; line-height: 1.3; }

    .promo-card { 
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); 
        padding: 25px; border-radius: 20px; border-left: 10px solid #0369a1; 
        margin-bottom: 20px; color: #0c4a6e; 
    }
    .promo-card h2 { color: #0c4a6e; font-weight: 900; }
    .patto-card { background-color: #fff1f2; padding: 20px; border-radius: 15px; border: 3px solid #e11d48; color: #333; margin-bottom: 20px;}
    .sigillo { background-color: #ccfbf1; color: #0f766e; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 0.9em; border: 2px solid #0d9488; display: inline-block; }
    .sigillo-oro { background-color: #fef3c7; color: #92400e; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 0.9em; border: 2px solid #b45309; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERALE ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0d9488; margin-bottom: 0px;'>🧸</h1>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;"><p class="logo-text" style="font-size: 28px;">LoopBaby</p></div>', unsafe_allow_html=True)
    st.write("---")
    scelta = st.sidebar.radio("Navigazione:", 
                     ["🏠 Benvenuta", "📝 Profilo Bimbo (0-24m)", "📦 Ordina Box (15€)", "💎 Box Premium (25€)", "🛍️ Vetrina Acquisto", "🔐 Area Admin"],
                     key="nav_final_bear")
    st.write("---")
    st.success("✨ Iscrizione GRATUITA")

# --- SEZIONE 1: HOME ---
if scelta == "🏠 Benvenuta":
    st.markdown('<div class="logo-container"><p class="logo-text">LoopBaby</p><p class="logo-sub">L\'armadio del tuo bimbo a poco prezzo e in modo sostenibile</p></div>', unsafe_allow_html=True)
    st.write("---")
    
    if st.session_state.get("mostra_valori", False):
        pop_up_valori()
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="step-box"><h1 style="font-size:50px;margin:0;">📦</h1><h3>1. Inviaci i tuoi capi</h3><p>Svuota l\'armadio e spedisci <b>10 o più capi</b> via Locker.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="step-box"><h1 style="font-size:50px;margin:0;">🚚</h1><h3>2. Ricevi la Box</h3><p>Ottieni 10 capi <b>igienizzati e stirati</b> della tua taglia.</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="step-box"><h1 style="font-size:50px;margin:0;">🔄</h1><h3>3. Scambia</h3><p>Quando cresce, rendi i capi (Jeans x Jeans) e prendi la nuova taglia!</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="promo-card">
        <h2>🚀 RISERVATO AI PRIMI 50 ISCRITTI</h2>
        <p>Entra nel cerchio delle Mamme Fondatrici: <b>Ritiro Locker GRATIS</b> (Offerto da LoopBaby) e <b>PRIMA BOX OMAGGIO</b>!</p>
        <p>⚠️ <i>Valido se spedisci 10 o più capi entro 30 giorni.</i></p>
    </div>
    """, unsafe_allow_html=True)

# --- SEZIONE 2: PROFILO ---
elif scelta == "📝 Profilo Bimbo (0-24m)":
    st.title("📝 Crea il Profilo (0-24 mesi)")
    with st.form("form_iscrizione"):
        nome = st.text_input("Nome del bambino")
        peso = st.number_input("Peso attuale (kg)", 2.0, 15.0, 5.0)
        taglia_calcolata = "0-1m" if peso < 4.5 else "1-3m" if peso < 5.5 else "3-6m" if peso < 7.5 else "6-9m" if peso < 9.0 else "12-24m"
        st.info(f"📏 Calcolo della tua taglia in base al peso: **{taglia_calcolata}**")
        if st.form_submit_button("SALVA E ATTIVA"):
            salva_dati({"Data": datetime.now(), "Nome": nome, "Taglia": taglia_calcolata, "Stato": "Iscritto"})
            st.balloons()
            st.success("Profilo salvato correttamente!")

# --- SEZIONE 3: BOX STANDARD ---
elif scelta == "📦 Ordina Box (15€)":
    st.title("📦 Box Standard (15,00 €)")
    st.markdown("""
    <div class="patto-card">
        <h3>🤝 PATTO DI QUALITÀ E RESO</h3>
        <ul>
            <li>✨ <b>Lavati e stirati:</b> Mandali pronti all'uso (noi li sanifichiamo di nuovo).</li>
            <li>🔄 <b>Scambio Pari:</b> Se tieni o rovini un pezzo, rimpiazzalo (Jeans x Jeans).</li>
            <li>⚠️ <b>Penale 5,00€:</b> Per ogni capo <b>mancante</b>, macchiato o bucato.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    sigillo = '<div class="sigillo">✓ IGIENIZZATO</div>'
    with c1:
        st.image("https://unsplash.com", caption="🌙 BOX LUNA")
        st.write("*Toni pastello e tessuti morbidi*")
        st.markdown(sigillo, unsafe_allow_html=True)
        st.button("Scegli Luna", key="l1")
    with c2:
        st.image("https://unsplash.com", caption="☀️ BOX SOLE")
        st.write("*Colori vivaci e stampe allegre*")
        st.markdown(sigillo, unsafe_allow_html=True)
        st.button("Scegli Sole", key="s1")
    with c3:
        st.image("https://unsplash.com", caption="☁️ BOX NUVOLA")
        st.write("*I basic essenziali e colori neutri*")
        st.markdown(sigillo, unsafe_allow_html=True)
        st.button("Scegli Nuvola", key="n1")

# --- SEZIONE 4: PREMIUM ---
elif scelta == "💎 Box Premium (25€)":
    st.title("💎 Box Premium ORO (25,00 €)")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image("https://unsplash.com", caption="Grandi Firme Selezionate")
        st.markdown('<div class="sigillo-oro">✨ QUALITÀ ORO</div>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("### Selezione Alta Gamma\n- 10 capi premium\n- Sanificazione professionale a vapore\n- Priorità sulla spedizione")
        if st.button("ORDINA ORO (25€)", key="btn_oro"): st.balloons()

# --- SEZIONE 5: VETRINA ---
elif scelta == "🛍️ Vetrina Acquisto":
    st.title("🛍️ Vetrina: Compra e Tieni")
    st.info("I capi acquistati in questa sezione non devono essere restituiti.")
    v1, v2 = st.columns(2)
    v1.image("https://unsplash.com", caption="Maglione Orsetto - 9,00 €")
    v1.button("Acquista", key="acq1")
    v2.image("https://unsplash.com", caption="Giubbotto Jeans - 15,00 €")
    v2.button("Acquista", key="acq2")

# --- AREA ADMIN ---
elif scelta == "🔐 Area Admin":
    st.title("Pannello Gestione")
    pwd = st.text_input("Password", type="password")
    if pwd == "baby2024":
        if os.path.exists('iscrizioni_loopbaby.csv'):
            df = pd.read_csv('iscrizioni_loopbaby.csv')
            st.dataframe(df)
