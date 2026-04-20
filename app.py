import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAZIONE CREDENZIALI (UFFICIALI) ---
GMAIL_USER = "assistenza.loopbaby@gmail.com"
GMAIL_PASS = "sqpw gpto jovf dlox"
DESTINATARIO_ORDINI = "xxmanuelvalente@gmail.com"

# --- FUNZIONE LOGICA INVIO MAIL ---
def invia_email_ordine(dettagli_ordine):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = DESTINATARIO_ORDINI
    msg['Subject'] = f"NUOVO ORDINE - {dettagli_ordine['cliente']}"
    
    corpo = f"""
    Nuovo ordine ricevuto su Loop Baby!
    
    Cliente: {dettagli_ordine['cliente']}
    Prodotto: {dettagli_ordine['prodotto']}
    Taglia: {dettagli_ordine['taglia']}
    Prezzo: {dettagli_ordine['prezzo']}
    Metodo Consegna: {dettagli_ordine['consegna']}
    """
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('://gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Loop Baby - Shop", page_icon="🍼", layout="centered")

# --- MENU LATERALE (NAVIGAZIONE) ---
st.sidebar.title("🍼 Loop Baby")
scelta = st.sidebar.radio("Naviga:", [
    "🏠 Home", 
    "👤 Profilo", 
    "📦 Box Standard", 
    "💎 Box Premium", 
    "🛍️ Vetrina", 
    "🔐 Admin",
    "✉️ Contatti"
])

# --- LOGICA DELLE PAGINE ---

# 1. PAGINA HOME
if scelta == "🏠 Home":
    st.title("Benvenuta ! ✨")
    
    # Sezione Chi Siamo
    st.info("""
    ### Chi Siamo? 👥
    Siamo **genitori** che capiscono la necessità di cambiare i vestiti ogni mese. 
    Abbiamo creato **LoopBaby** per eliminare lo stress e i costi eccessivi.
    """)
    
    # Sezione Obiettivo
    st.success("""
    ### L'Obiettivo di LoopBaby 🌿
    **Risparmio di Tempo, Denaro e Spazio.**  
    Vestiti controllati con cura, con un occhio al prezzo e al pianeta.
    """)

# 2. PAGINA BOX STANDARD
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard")
    st.write("La soluzione ideale per la crescita quotidiana del tuo bambino.")
    st.image("https://placehold.co", caption="Esempio di Box Standard")
    st.write("---")
    st.write("**Cosa include:** 10 capi essenziali selezionati per il mese corrente.")
    st.write("**Prezzo:** 49.00€ / mese")
    if st.button("Abbonati alla Box Standard"):
        st.balloons()
        st.write("Richiesta inviata! Ti contatteremo per la taglia.")

# 3. PAGINA BOX PREMIUM
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium")
    st.write("Il meglio del fashion per neonati, con brand di alta gamma.")
    st.image("https://placehold.co", caption="Esempio di Box Premium")
    st.write("---")
    st.write("**Cosa include:** 8 capi firmati e accessori esclusivi.")
    st.write("**Prezzo:** 89.00€ / mese")
    if st.button("Abbonati alla Box Premium"):
        st.balloons()
        st.write("Benvenuto nel mondo Premium di Loop Baby!")

# 4. PAGINA VETRINA (ALTA GAMMA)
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.warning("I capi acquistati qui rimarranno a te per sempre!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placehold.co", caption="Cappottino Elegante")
        prezzo_v = "45.00€"
        st.write(f"### Prezzo: {prezzo_v}")

    with col2:
        taglia_v = st.selectbox("Seleziona Taglia", ["0-3 mesi", "3-6 mesi", "6-9 mesi", "9-12 mesi"])
        consegna_v = st.radio("Metodo consegna", ["Locker (Gratis)", "Spedizione (+5€)"])
        nome_v = st.text_input("Il tuo Nome per l'ordine")
        
        if st.button("CONFERMA ORDINE"):
            if nome_v:
                dati = {
                    "cliente": nome_v, 
                    "prodotto": "Cappottino Firmato", 
                    "taglia": taglia_v, 
                    "prezzo": prezzo_v, 
                    "consegna": consegna_v
                }
                if invia_email_ordine(dati):
                    st.success(f"Grazie {nome_v}! Ordine inviato correttamente.")
                    st.balloons()
                else:
                    st.error("Errore nell'invio mail. Riprova tra poco.")
            else:
                st.warning("Per favore, inserisci il tuo nome.")

# 5. PAGINA CONTATTI
elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.write("Hai domande o bisogno di supporto? Il nostro team è a tua disposizione.")
    
    # TASTO ROSSO MAILTO
    st.markdown(f"""
    <a href="mailto:{GMAIL_USER}" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; width: 100%;">
            📩 Inviaci un'email ora: {GMAIL_USER}
        </button>
    </a>
    """, unsafe_allow_html=True)
    
    st.info("Rispondiamo solitamente entro 24 ore lavorative (Lun-Ven).")

# 6. ALTRE PAGINE (PROFILO / ADMIN)
else:
    st.title(scelta)
    st.write("Sezione in fase di configurazione per il magazzino di domani. 🚀")
