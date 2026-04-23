import streamlit as st

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

# --- 2. CSS TOTALE (COPIA ESATTA) ---
st.markdown("""
    <style>
    /* Nascondi tutto lo sporco di Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {display: none !important;}
    .stApp {background-color: #FFFFFF !important; max-width: 450px !important; margin: 0 auto !important;}
    
    @import url('https://googleapis.com');
    * { font-family: 'Lexend', sans-serif !important; }

    /* Container Home */
    .app-container { padding: 20px; text-align: left; }
    
    /* Logo */
    .logo-h { font-size: 35px; font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 10px; margin-bottom: 0; }
    .heart { color: #f43f5e; }
    .slogan { font-size: 14px; color: #64748b; margin-bottom: 30px; }

    /* Layout a due colonne che NON CROLLA */
    .main-grid {
        display: grid;
        grid-template-columns: 1.6fr 1fr;
        gap: 10px;
        align-items: start;
    }

    .ciao { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .headline { font-size: 15px; font-weight: 600; color: #334155; line-height: 1.3; margin-bottom: 15px; }
    
    /* Lista icone */
    .list-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; margin-bottom: 10px; font-weight: 500; }

    /* Immagine Bimbo */
    .baby-img { width: 100%; border-radius: 25px; object-fit: cover; }

    /* PULSANTE ROSA IDENTICO ALLA FOTO */
    .btn-rosa {
        background-color: #f43f5e;
        color: white;
        text-align: center;
        padding: 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 18px;
        text-decoration: none;
        display: block;
        margin-top: 30px;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
        border: none;
        width: 100%;
        cursor: pointer;
    }

    .footer-text { text-align: center; color: #94a3b8; font-size: 12px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. COSTRUZIONE HOME (UNICO BLOCCO HTML) ---
# Inserisco il link alla foto del bimbo direttamente qui così carica sicuramente
st.markdown("""
    <div class="app-container">
        <!-- Logo -->
        <div class="logo-h"><span class="heart">💗</span> LoopBaby</div>
        <div class="slogan">Vestiamo il tuo bambino, rispettiamo il futuro.</div>

        <!-- Layout Colonne -->
        <div class="main-grid">
            <!-- Sinistra: Testo -->
            <div class="col-left">
                <div class="ciao">Ciao Mamma! 👋</div>
                <div class="headline">Vestiamo il tuo bambino con amore e qualità, senza sprechi e senza stress.</div>
                
                <div class="list-item">👕 Capi di qualità selezionati</div>
                <div class="list-item">🔄 Cambi quando cresce</div>
                <div class="list-item">💰 Risparmi più di 1000€ l'anno</div>
                <div class="list-item">📍 Scegli il locker più vicino</div>
                <div class="list-item">✨ Zero stress per te</div>
            </div>
            
            <!-- Destra: Immagine -->
            <div class="col-right">
                <img src="https://unsplash.com" class="baby-img">
            </div>
        </div>

        <!-- Pulsante Rosa (HTML così è largo e perfetto) -->
        <form action="/">
            <button class="btn-rosa" type="submit" name="scelta" value="box">Scegli la tua Box</button>
        </form>

        <!-- Footer -->
        <div class="footer-text">❤️ Creato da genitori, per genitori.</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. LOGICA PER CAMBIARE PAGINA ---
# Questo serve per far funzionare il tasto HTML sopra
if st.query_params.get("scelta") == "box":
    st.toast("Caricamento Box...")
    # Qui metterai il codice per la pagina delle Box
