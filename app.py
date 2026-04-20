import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAZIONE CREDENZIALI ---
GMAIL_USER = "assistenza.loopbaby@gmail.com"
GMAIL_PASS = "sqpw gpto jovf dlox"
DESTINATARIO_ORDINI = "xxmanuelvalente@gmail.com"

# --- FUNZIONE INVIO MAIL ---
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
    except Exception as e:
        return False

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Loop Baby - Shop", page_icon="🍼")

# --- MENU LATERALE (NAVIGAZIONE) ---
st.sidebar.title(f"Ciao {st.session_state.get('username', '!')} 🧸")
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

if scelta == "🏠 Home":
    st.title("Benvenuta! ✨")
    st.write("---")
    st.info("**Chi Siamo?** Siamo genitori che capiscono la necessità di cambiare i vestiti ogni mese. Abbiamo creato LoopBaby per eliminare lo stress e i costi eccessivi.")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.success("I capi acquistati qui rimarranno a te!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placeholder.com", caption="Cappottino Firmato")
        prezzo_capo = "45.00€"
        st.write(f"**Prezzo:** {prezzo_capo}")

    with col2:
        taglia = st.selectbox("Seleziona Taglia", ["0-3 mesi", "3-6 mesi", "6-9 mesi"])
        consegna = st.radio("Metodo consegna", ["Locker (Gratis)", "Spedizione (+5€)"])
        nome = st.text_input("Nome per l'ordine")
        
        if st.button("ACQUISTA"):
            if nome:
                dati = {"cliente": nome, "prodotto": "Cappottino Firmato", "taglia": taglia, "prezzo": prezzo_capo, "consegna": consegna}
                if invia_email_ordine(dati):
                    st.success("Ordine inviato! Controlla la tua mail.")
                    st.balloons()
                else:
                    st.error("Errore nell'invio. Riprova.")
            else:
                st.warning("Inserisci il tuo nome.")

elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.write("Hai domande sui nostri capi o sul tuo ordine? Siamo qui per aiutarti!")
    
    # TASTO ROSSO MAILTO
    st.markdown(f"""
    <a href="mailto:{GMAIL_USER}" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px;">
            📩 Inviaci un'email ora
        </button>
    </a>
    <br><br>
    <p>Indirizzo email ufficiale: <b>{GMAIL_USER}</b></p>
    """, unsafe_allow_html=True)
    
    st.info("Servizio clienti attivo dal Lunedì al Venerdì.")

else:
    st.title(scelta)
    st.write("Sezione in fase di caricamento... A domani per i 50 capi! 🚀")
