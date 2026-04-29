import streamlit as st
from supabase import create_client, Client

# --- 1. DATI DI CONNESSIONE (SCRITTI DIRETTAMENTE) ---
# Non usare st.secrets, scriviamo le stringhe a mano qui
url_fissa = "https://supabase.co"
key_fissa = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

# --- 2. INIZIALIZZAZIONE FORZATA ---
# Creiamo il client passandogli i dati a mano, senza variabili esterne
try:
    supabase: Client = create_client(url_fissa, key_fissa)
except Exception as e:
    st.error(f"Errore inizializzazione: {e}")

# --- 3. TEST REGISTRAZIONE ---
st.title("LoopBaby - Test Finale 🚀")

with st.form("signup_form"):
    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")
    nome = st.text_input("Tuo Nome")
    btn = st.form_submit_button("REGISTRATI ORA")
    
    if btn:
        try:
            # Qui forziamo la chiamata all'URL corretto
            res = supabase.auth.sign_up({
                "email": email, 
                "password": pwd,
                "options": {"data": {"full_name": nome}}
            })
            st.success("✅ CE L'ABBIAMO FATTA! Controlla la mail (anche Spam)!")
        except Exception as e:
            # Se vedi ancora supabase.com qui, significa che Streamlit 
            # non sta aggiornando il file .py che hai salvato.
            st.error(f"Errore tecnico: {e}")
