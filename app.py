import requests
import streamlit as st
import os
import base64
import json
from datetime import date

SHEETDB_API = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def salva_su_sheetdb(dati):
    payload = {
        "data": [{
            "email": dati["email"],
            "password": "",
            "nome_genitore": dati["nome_genitore"],
            "nome_bambino": dati["nome_bambino"],
            "taglia": dati["taglia"],
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": dati["locker"]
        }]
    }
    requests.post(SHEETDB_API, json=payload)


st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = {
        "nome_genitore": "",
        "email": "",
        "telefono": "",
        "nome_bambino": "",
        "nascita": date(2024, 1, 1),
        "taglia": "50-56 cm",
        "locker": ""
    }

if "utente" not in st.session_state:
    st.session_state.utente = None

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

# ---------------- CSS (INVARIATO) ----------------
st.markdown(f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
.stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
.main .block-container {{padding: 0 !important;}}
* {{ font-family: 'Lexend', sans-serif !important; }}

.header-custom {{
    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
    background-size: cover;
    background-position: center;
    height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 35px;
    border-radius: 0 0 30px 30px;
}}

.header-text {{
    color: white;
    font-size: 32px;
    font-weight: 800;
}}

.card {{
    border-radius: 25px;
    padding: 20px;
    margin: 10px 20px;
    background-color: #fff;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# ---------------- Pagine ----------------

if st.session_state.pagina == "Home":
    st.write("HOME")

elif st.session_state.pagina == "Profilo":
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)

    if not st.session_state.edit_mode:
        st.markdown(f"""<div class="card">
            <b>👤 Nome:</b> {st.session_state.dati['nome_genitore']}<br>
            <b>📧 Email:</b> {st.session_state.dati['email']}<br>
            <b>📞 Tel:</b> {st.session_state.dati['telefono']}<br>
            <b>👶 Bambino:</b> {st.session_state.dati['nome_bambino']}<br>
            <b>📏 Taglia:</b> {st.session_state.dati['taglia']}<br>
            <b>📍 Locker:</b> {st.session_state.dati['locker'] or 'Da scegliere'}
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
                st.session_state.dati.update({
                    "nome_genitore": n,
                    "nome_bambino": nb,
                    "nascita": nas,
                    "taglia": tg,
                    "locker": lock
                })

                salva_su_sheetdb(st.session_state.dati)

                st.session_state.edit_mode = False
                st.success("Dati salvati ✅")
                st.rerun()
