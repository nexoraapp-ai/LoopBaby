import streamlit as st
from supabase import create_client, Client

# --- FORZATURA DATI (NON USARE SECRETS) ---
URL_CORRETTO = "https://supabase.co"
KEY_CORRETTA = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

# Inizializziamo il client ignorando tutto il resto
try:
    if "supabase" not in st.session_state:
        st.session_state.supabase = create_client(URL_CORRETTO, KEY_CORRETTA)
    sb = st.session_state.supabase
except Exception as e:
    st.error(f"Errore di connessione: {e}")

st.title("LoopBaby - Test Registrazione Manuel")

with st.form("test_reg"):
    email = st.text_input("Tua Email")
    password = st.text_input("Scegli Password (min 6 car)", type="password")
    nome = st.text_input("Tuo Nome")
    submit = st.form_submit_button("REGISTRAMI ORA")
    
    if submit:
        try:
            # PROVA REGISTRAZIONE
            res = sb.auth.sign_up({"email": email, "password": password})
            # PROVA INSERIMENTO TABELLA PROFILI
            sb.table("profili").insert({"id": res.user.id, "email": email, "nome_genitore": nome}).execute()
            st.success("✅ EVVIVA! È ANDATA! Controlla l'email per confermare.")
        except Exception as err:
            st.error(f"C'è ancora un intoppo: {err}")
