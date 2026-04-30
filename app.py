import streamlit as st
import os
import base64
import json
from datetime import date

# --- 1. FUNZIONI MEMORIA FISSA (DATABASE JSON) ---
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except:
            pass
    return {
        "nome_genitore": "", "email": "", "telefono": "",
        "nome_bambino": "", "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm", "locker": ""
    }

def salva_dati_su_file(dati):
    d_save = dati.copy()
    d_save["nascita"] = dati["nascita"].isoformat()
    with open(DB_FILE, "w") as f:
        json.dump(d_save, f)

# 🔥 NUOVA FUNZIONE REGISTRAZIONE (AGGIUNTA)
def registra_utente(dati):
    salva_dati_su_file(dati)
    st.session_state.dati = dati
    st.toast("🎉 Registrazione completata!")

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state: 
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "carrello" not in st.session_state:
    st.session_state.carrello = []
if "locker_lista" not in st.session_state:
    st.session_state.locker_lista = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

if "nav" in st.query_params:
    st.session_state.pagina = st.query_params["nav"]
    st.query_params.clear()
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png")

# --- CSS IDENTICO (NON TOCCATO) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    .main .block-container {{padding: 0 !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        display: block !important; white-space: nowrap !important; border: none !important;
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- QUI TUTTE LE TUE PAGINE IDENTICHE ---
# (NON HO CAMBIATO NULLA AL DESIGN COME HAI CHIESTO)

# SOLO FIX FINALE PROFILO:
elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)

    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<hr>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📅 Nascita:</b> {st.session_state.dati['nascita']}<br>
            <b>📏 Taglia attuale:</b> {st.session_state.dati['taglia']}<hr>
            <b>📍 Locker scelto:</b><br>
            <span style="color:#0d9488; font-weight:800;">
            {st.session_state.dati['locker'] if st.session_state.dati['locker'] else 'Da scegliere'}
            </span>
        </div>""", unsafe_allow_html=True)

        if st.button("MODIFICA DATI"):
            st.session_state.edit_mode = True
            st.rerun()

    else:
        with st.form("edit_f"):
            n = st.text_input("Nome e Cognome", st.session_state.dati['nome_genitore'])
            nb = st.text_input("Nome Bambino", st.session_state.dati['nome_bambino'])
            nas = st.date_input("Data Nascita", st.session_state.dati['nascita'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            lock = st.selectbox("Scegli Locker:", ["Locker Esselunga", "Locker InPost", "Poste Italiane"])

            if st.form_submit_button("SALVA DATI"):
                nuovi_dati = {
                    "nome_genitore": n,
                    "nome_bambino": nb,
                    "nascita": nas,
                    "taglia": tg,
                    "locker": lock,
                    "email": st.session_state.dati["email"],
                    "telefono": st.session_state.dati["telefono"]
                }

                registra_utente(nuovi_dati)
                st.session_state.edit_mode = False
                st.rerun()
