import streamlit as st
from supabase import create_client

# --- CONNESSIONE BLINDATA ---
URL = "https://supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

# Forza il client a usare il TUO endpoint specifico
supabase = create_client(URL, KEY)

if "user" not in st.session_state: st.session_state.user = None

st.title("👶 LOOPBABY - TEST REGISTRAZIONE")

if not st.session_state.user:
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        with st.form("login"):
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                    st.session_state.user = res.user
                    st.rerun()
                except: st.error("Errore")
                
    with tab2:
        with st.form("reg"):
            er = st.text_input("Email")
            pr = st.text_input("Password", type="password")
            if st.form_submit_button("CREA ACCOUNT"):
                try:
                    # Chiamata diretta al tuo URL .co
                    supabase.auth.sign_up({"email": er, "password": pr})
                    st.success("📩 CONTROLLA LA MAIL ORA!")
                except Exception as e:
                    st.error(f"Errore: {e}")
else:
    st.write(f"Sei dentro come: {st.session_state.user.email}")
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
