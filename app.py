import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
API_URL = "https://sheetdb.io"

def carica_dati_nudi():
    # Aggiungiamo un numero casuale estremo per saltare la cache
    t = datetime.now().microsecond
    try:
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        return res.json()
    except:
        return []

# --- 2. SETUP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
st.title("👶 LOOPBABY - DEBUG")

# --- 3. COSA VEDE IL SERVER? ---
raw = carica_dati_nudi()

st.subheader("📡 Dati ricevuti da Excel:")
if not raw:
    st.error("ATTENZIONE: SheetDB sta inviando un database VUOTO [ ].")
    st.info("Sblocca premendo 'RELOAD SPREADSHEET' su SheetDB.io")
else:
    st.success(f"Trovati {len(raw)} utenti!")
    st.json(raw) # Ti mostra i dati reali qui!

# --- 4. TASTO DI REGISTRAZIONE EMERGENZA ---
st.divider()
st.write("Se sopra vedi [ ], prova a fare una registrazione qui sotto:")
with st.form("r"):
    e = st.text_input("Email")
    p = st.text_input("Password")
    if st.form_submit_button("REGISTRA E FORZA"):
        nuovo = {"email": e, "password": p, "nome": "Test"}
        res = requests.post(API_URL, json={"data": [nuovo]})
        if res.status_code == 201:
            st.success("Scrittura riuscita! Ora clicca il tasto sotto.")
        else:
            st.error(f"Errore scrittura: {res.text}")

if st.button("🔄 RICARICA TUTTO"):
    st.rerun()
