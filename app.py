import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAZIONE CREDENZIALI (BLINDATE) ---
GMAIL_USER = "assistenza.loopbaby@gmail.com"
GMAIL_PASS = "sqpw gpto jovf dlox"
DESTINATARIO_ORDINI = "xxmanuelvalente@gmail.com"

# --- FUNZIONE INVIO MAIL ---
def invia_email_ordine(dettagli_ordine):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = DESTINATARIO_ORDINI
    msg['Subject'] = f"NUOVO ORDINE - {dettagli_ordine['cliente']}"
    
    corpo = f"Nuovo ordine ricevuto!\n\nCliente: {dettagli_ordine['cliente']}\nProdotto: {dettagli_ordine['prodotto']}\nTaglia: {dettagli_ordine['taglia']}\nPrezzo: {dettagli_ordine['prezzo']}\nConsegna: {dettagli_ordine['consegna']}"
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
st.set_page_config(page_title="Loop Baby - Shop", page_icon="🍼")

# --- MENU LATERALE (SIDEBAR) ---
st.sidebar.title("Naviga: 🧸")
scelta = st.sidebar.radio("", [
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
    st.title("Benvenuta su Loop Baby! ✨")
    st.info("**Chi Siamo?** Siamo genitori che capiscono la necessità di cambiare i vestiti ogni mese. Abbiamo creato Loop Baby per eliminare lo stress e i costi eccessivi.")
    st.subheader("L'Obiettivo di Loop Baby 🌿")
    st.write("Risparmio di Tempo, Denaro e Spazio. Vestiti controllati con cura, con un occhio al prezzo e al pianeta.")

elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard")
    st.write("La soluzione ideale per l'uso quotidiano.")
    st.image("https://placehold.co", caption="Esempio Box Standard")
    st.write("**Prezzo Mensile:** 49.00€")
    if st.button("Sottoscrivi Box Standard"):
        st.success("Ottima scelta! Verrai ricontattato per i dettagli.")

elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium")
    st.write("Il meglio per il tuo bambino, con brand esclusivi.")
    st.image("https://placehold.co", caption="Esempio Box Premium")
    st.write("**Prezzo Mensile:** 89.00€")
    if st.button("Sottoscrivi Box Premium"):
        st.success("Benvenuto nel mondo Premium! Verrai ricontattato a breve.")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Alta Gamma")
    st.success("I capi acquistati qui rimarranno a te!")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://placehold.co", caption="Cappottino Firmato")
        prezzo_v = "45.00€"
        st.write(f"**Prezzo:** {prezzo_v}")
    with col2:
        taglia_v = st.selectbox("Taglia", ["0-3 mesi", "3-6 mesi", "6-9 mesi"])
        consegna_v = st.radio("Consegna", ["Locker (Gratis)", "Spedizione (+5€)"])
        nome_v = st.text_input("Inserisci il tuo Nome")
        if st.button("CONFERMA ORDINE"):
            if nome_v:
                dati = {"cliente": nome_v, "prodotto": "Cappottino Firmato", "taglia": taglia_v, "prezzo": prezzo_v, "consegna": consegna_v}
                if invia_email_ordine(dati):
                    st.success("Ordine inviato con successo!")
                    st.balloons()
                else:
                    st.error("Errore nell'invio mail.")

elif scelta == "✉️ Contatti":
    st.title("✉️ Contatti & Assistenza")
    st.write("Serve aiuto? Clicca il tasto rosso per scriverci direttamente.")
    st.markdown(f"""
    <a href="mailto:{GMAIL_USER}" style="text-decoration: none;">
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; width: 100%;">
            📩 Inviaci un'email: {GMAIL_USER}
        </button>
    </a>
    """, unsafe_allow_html=True)
    st.info("Assistenza clienti attiva Lun-Ven.")

else:
    st.title(scelta)
    st.write("Questa sezione verrà attivata con i dati reali.")
