import streamlit as st
import os
import base64
import json
from datetime import date

# --- DATABASE LOCALE (fallback temporaneo) ---
DB_FILE = "db_loopbaby.json"

def carica_dati():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                d = json.load(f)
                if "nascita" in d:
                    d["nascita"] = date.fromisoformat(d["nascita"])
                return d
        except:
            pass
    return {
        "nome_genitore": "",
        "nome_bambino": "",
        "nascita": date(2024,1,1),
        "taglia": "50-56 cm",
        "locker": ""
    }

def salva_dati(d):
    x = d.copy()
    x["nascita"] = d["nascita"].isoformat()
    with open(DB_FILE,"w") as f:
        json.dump(x,f)

# --- CONFIG ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "dati" not in st.session_state:
    st.session_state.dati = carica_dati()
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "carrello" not in st.session_state:
    st.session_state.carrello = []

def vai(p):
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    if not any(i["nome"] == nome for i in st.session_state.carrello):
        st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
        st.toast(f"✅ {nome} aggiunto!")
    else:
        st.toast("⚠️ Già nel carrello")

def get_base64(path):
    if os.path.exists(path):
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img = get_base64("bimbo.jpg")
logo = get_base64("logo.png")

# --- CSS ---
st.markdown(f"""
<style>
[data-testid="stHeader"], #MainMenu {{display:none;}}
.stApp {{max-width:450px; margin:auto; background:#FDFBF7; padding-bottom:120px;}}
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;800&display=swap');
* {{font-family:'Lexend',sans-serif;}}

.header {{
background-image:url("data:image/png;base64,{logo}");
height:130px; display:flex; align-items:center; justify-content:center;
border-radius:0 0 30px 30px;
}}
.title {{color:white; font-size:30px; font-weight:800;}}

.card {{
background:white; padding:20px; margin:15px;
border-radius:25px; box-shadow:0 5px 20px rgba(0,0,0,0.05);
}}

.prezzo {{color:#ec4899; font-size:22px; font-weight:900;}}

.box-luna {{background:#f1f5f9;}}
.box-sole {{background:#FFD600;}}
.box-nuvola {{background:#94A3B8; color:white;}}

.badge {{
background:#f43f5e; color:white; padding:6px 14px;
border-radius:20px; font-size:12px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><div class="title">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- HOME ---
if st.session_state.pagina == "Home":
    nome = st.session_state.dati["nome_genitore"].split()[0] if st.session_state.dati["nome_genitore"] else ""
    saluto = f"Ciao {nome} 👋" if nome else "Ciao 👋"

    st.markdown(f"<h2 style='padding:0 20px'>{saluto}</h2>", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;"><span class="badge">🔥 Startup in lancio</span></div>', unsafe_allow_html=True)

    if img:
        st.image("bimbo.jpg", use_container_width=True)

    st.markdown("""
<div class="card">
✔ Risparmi fino a 1000€ anno<br>
✔ Cambi taglia quando vuoi<br>
✔ Zero sprechi ♻️
</div>
""", unsafe_allow_html=True)

    if st.button("Inizia ora"):
        vai("Box")

# --- INFO ---
elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona 🔄</h2>', unsafe_allow_html=True)

    st.markdown("""
<div style="padding:20px; font-size:14px;">
<b>Prezzo iniziale:</b><br>
19,90€ Standard / 29,90€ Premium + spedizione<br><br>

<b>Durata:</b><br>
90 giorni utilizzo<br><br>

<b>Cambio taglia:</b><br>
Se cresce prima → ci contatti<br><br>

<b>Reso:</b><br>
• Richiedi etichetta<br>
• Porti al locker<br><br>

<b>Nuova box:</b><br>
GRATUITA spedizione<br><br>

<b>Stop servizio:</b><br>
Paghi solo spedizione
</div>
""", unsafe_allow_html=True)

# --- BOX ---
elif st.session_state.pagina == "Box":
    tg = st.session_state.dati["taglia"]

    for nome, css in [("LUNA 🌙","box-luna"),("SOLE ☀️","box-sole"),("NUVOLA ☁️","box-nuvola")]:
        st.markdown(f"""
<div class="card {css}">
<h3>{nome}</h3>
<p class="prezzo">19.90€</p>
<p style="font-size:12px">✔ 10 capi inclusi</p>
</div>
""", unsafe_allow_html=True)

        if st.button(f"Scegli {nome}"):
            aggiungi(f"Box {nome} ({tg})",19.90)

# --- PROFILO ---
elif st.session_state.pagina == "Profilo":
    d = st.session_state.dati

    if not st.session_state.edit_mode:
        st.markdown(f"""
<div class="card">
<b>{d["nome_genitore"]}</b><br>
{d["nome_bambino"]}<br>
{d["taglia"]}
</div>
""", unsafe_allow_html=True)

        if st.button("Modifica"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        with st.form("f"):
            n = st.text_input("Nome", d["nome_genitore"])
            nb = st.text_input("Bimbo", d["nome_bambino"])
            tg = st.selectbox("Taglia", ["50-56 cm","62-68 cm","74-80 cm"])

            if st.form_submit_button("Salva"):
                st.session_state.dati.update({
                    "nome_genitore": n,
                    "nome_bambino": nb,
                    "taglia": tg
                })
                salva_dati(st.session_state.dati)
                st.session_state.edit_mode = False
                st.rerun()

# --- CARRELLO ---
elif st.session_state.pagina == "Carrello":
    if not st.session_state.carrello:
        st.write("Vuoto")
    else:
        tot = sum(i["prezzo"] for i in st.session_state.carrello)

        for i in st.session_state.carrello:
            st.write(f"{i['nome']} - {i['prezzo']}€")

        st.markdown(f"### Totale: {tot:.2f}€")

        if st.button("Procedi"):
            st.success("🚧 Pagamenti in arrivo!")

# --- CHI SIAMO ---
elif st.session_state.pagina == "ChiSiamo":
    st.markdown("""
<h2 style="text-align:center;">Non è solo un'app ❤️</h2>
<p style="text-align:center;">È il modo più intelligente di vestire tuo figlio.</p>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
Vestiti usati poche settimane.<br>
Soldi sprecati.<br><br>

LoopBaby cambia tutto.<br><br>

Risparmi.<br>
Zero sprechi.<br>
Zero stress.
</div>
""", unsafe_allow_html=True)

# --- NAV ---
st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
cols = st.columns(5)

menu = ["Home","Info","Box","Profilo","Carrello"]

for i,m in enumerate(menu):
    with cols[i]:
        if st.button(m):
            vai(m)
