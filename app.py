import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAZIONE CREDENZIALI (AGGIORNATE) ---
GMAIL_USER = "assistenza.loopbaby@gmail.com"
GMAIL_PASS = "sqpw gpto jovf dlox"
DESTINATARIO_ORDINI = "xxmanuelvalente@gmail.com"

def invia_email_ordine(dettagli_ordine):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = DESTINATARIO_ORDINI
    msg['Subject'] = f"NUOVO ORDINE - {dettagli_ordine['cliente']}"
    
    corpo = f"""
    Nuovo ordine ricevuto!
    
    Cliente: {dettagli_ordine['cliente']}
    Prodotto: {dettagli_ordine['prodotto']}
    Taglia: {dettagli_ordine['taglia']}
    Prezzo: {dettagli_ordine['prezzo']}
    Metodo Consegna: {dettagli_ordine['consegna']}
    """
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# --- INTERFACCIA APP LOOP BABY ---
st.set_page_config(page_title="Loop Baby - Shop", page_icon="🍼")

st.title("🍼 Loop Baby")
st.subheader("Selezione Capi Esclusivi")

# Esempio Prodotto nel magazzino
col1, col2 = st.columns(2)

with col1:
    st.image("https://placeholder.com", caption="Tutina Bio Cotton") # Qui andranno le tue foto
    prezzo = "29.90€"
    st.write(f"**Prezzo:** {prezzo}")

with col2:
    taglia = st.selectbox("Seleziona Taglia", ["0-3 mesi", "3-6 mesi", "6-9 mesi", "9-12 mesi"])
    consegna = st.radio("Metodo di consegna", ["Ritiro in Locker (Gratis)", "Spedizione a casa (+5€)"])
    nome_cliente = st.text_input("Il tuo Nome per l'ordine")

    if st.button("CONFERMA ORDINE"):
        if nome_cliente:
            dati = {
                "cliente": nome_cliente,
                "prodotto": "Tutina Bio Cotton",
                "taglia": taglia,
                "prezzo": prezzo,
                "consegna": consegna
            }
            if invia_email_ordine(dati):
                st.success(f"Grazie {nome_cliente}! Ordine inviato con successo.")
                st.balloons()
            else:
                st.error("Errore nell'invio dell'ordine. Riprova.")
        else:
            st.warning("Inserisci il tuo nome prima di confermare.")

st.divider()

# --- SEZIONE CONTATTI & ASSISTENZA ---
st.subheader("✉️ Contatti & Assistenza")
st.write("Hai bisogno di aiuto o vuoi informazioni sui capi?")

# Tasto Rosso Mailto (Cliccabile)
st.markdown(f"""
<a href="mailto:{GMAIL_USER}" style="text-decoration: none;">
    <button style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold;">
        📩 Inviaci un'email: {GMAIL_USER}
    </button>
</a>
""", unsafe_allow_html=True)

st.info("Servizio clienti Loop Baby attivo dal Lunedì al Venerdì.")
