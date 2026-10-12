import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(page_title="Diyet ve Aktivite Asistanı", layout="wide", initial_sidebar_state="expanded")

DATA_FILE = "diyet_verileri_kalici.json"

# Kalıcı Veri Saklama ve Yükleme Mekanizması
def verileri_yukle():
    default_data = {
        "besin_veritabani": {
            "tavuk gogsu": {"kalori": 165, "protein": 31.0, "karb": 0.0, "yag": 3.6},
            "kofte": {"kalori": 220, "protein": 24.0, "karb": 2.0, "yag": 13.0},
            "ton baligi": {"kalori": 110, "protein": 25.0, "karb": 0.0, "yag": 1.0},
            "marul": {"kalori": 15, "protein": 1.4, "karb": 2.9, "yag": 0.2},
            "salatalik": {"kalori": 15, "protein": 0.7, "karb": 3.6, "yag": 0.1},
            "domates": {"kalori": 18, "protein": 0.9, "karb": 3.9, "yag": 0.2},
            "zeytinyagi": {"kalori": 884, "protein": 0.0, "karb": 0.0, "yag": 100.0},
            "dilim peynir": {"kalori": 320, "protein": 22.0, "karb": 1.5, "yag": 25.0},
            "tam bugday ekmegi": {"kalori": 247, "protein": 13.0, "karb": 41.0, "yag": 3.4},
            "labne": {"kalori": 210, "protein": 6.0, "karb": 4.0, "yag": 20.0},
            "sut": {"kalori": 50, "protein": 3.4, "karb": 4.8, "yag": 1.5},
            "kahve": {"kalori": 2, "protein": 0.1, "karb": 0.3, "yag": 0.0},
            "kefir": {"kalori": 60, "protein": 3.5, "karb": 4.5, "yag": 3.0},
            "x-lim toz": {"kalori": 20, "protein": 0.0, "karb": 5.0, "yag": 0.0},
            "badem": {"kalori": 575, "protein": 21.0, "karb": 22.0, "yag": 49.0},
            "mandalina": {"kalori": 53, "protein": 0.8, "karb": 13.3, "yag": 0.3},
            "meyveli soda": {"kalori": 45, "protein": 0.0, "karb": 11.0, "yag": 0.0}
        },
        "hazir_tarifler": {
            "Tavuklu Salata": {"tavuk gogsu": 200, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Köfteli Salata": {"kofte": 150, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Ton Balıklı Salata": {"ton baligi": 110, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Latte (Orta Boy)": {"sut": 250, "kahve": 30},
            "Americano (Orta Boy)": {"kahve": 20},
            "Kefir Karışımı": {"kefir": 200, "x-lim toz": 5},
            "Badem (1 Avuç)": {"badem": 30},
            "Mandalina (3 Adet)": {"mandalina": 300},
            "Meyveli Soda": {"meyveli soda": 200}
        },
        "gunluk_kayitlar": [],
        "aktivite_loglari": {},
        "profil": {
            "cinsiyet": "Kadın", "yas": 20, "boy": 165, "kilo": 58.0, 
            "hedef_kalori": 1800, "hedef_protein": 90, "hedef_karb": 200, "hedef_yag": 60
        }
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def verileri_kaydet():
    data = {
        "besin_veritabani": st.session_state.besin_veritabani,
        "hazir_tarifler": st.session_state.hazir_tarifler,
        "gunluk_kayitlar": st.session_state.gunluk_kayitlar,
        "aktivite_loglari": st.session_state.aktivite_loglari,
        "profil": st.session_state.profil
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Session state başlatma
loaded_data = verileri_yukle()
if "besin_veritabani" not in st.session_state:
    st.session_state.besin_veritabani = loaded_data["besin_veritabani"]
if "hazir_tarifler" not in st.session_state:
    st.session_state.hazir_tarifler = loaded_data["hazir_tarifler"]
if "gunluk_kayitlar" not in st.session_state:
    st.session_state.gunluk_kayitlar = loaded_data["gunluk_kayitlar"]
if "aktivite_loglari" not in st.session_state:
    st.session_state.aktivite_loglari = loaded_data.get("aktivite_loglari", {})
if "profil" not in st.session_state:
    st.session_state.profil = loaded_data["profil"]

st.title("Diyet ve Aktivite Takip Asistanı")

menu = st.sidebar.selectbox(
    "Menü", 
    [
        "Günlük Takip Paneli", 
        "Haftalık Program & Değerlendirme", 
        "Tarif ve Malzeme Yönetimi", 
        "Makro & Hedef Sihirbazı"
    ]
)

# ----------------------------------------------------
# 1. GÜNLÜK TAKİP PANELİ
# ----------------------------------------------------
if menu == "Günlük Takip Paneli":
    st.header("Günlük Beslenme ve Aktivite Takip Paneli")
    
    secilen_tarih = str(st.date_input("Kayıt Tarihi", datetime.date.today()))
    
    if secilen_tarih not in st.session_state.aktivite_loglari:
        st.session_state.aktivite_loglari[secilen_tarih] = {
            "adim": 10000, "su": 2.0, "pilates_tur": "Mat Pilates", "pilates_sure": 45,
            "yuruyus_tur": "Orta Tempo (5 km/s)", "yuruyus_sure": 30
        }

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Öğün Girişi")
        ogun_turu = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
        secilen_tarif = st.selectbox("Mevcut Tarifler", list(st.session_state.hazir_tarifler.keys()))
        
        if st.button("Öğüne Ekle"):
            malzemeler = st.session_state.hazir_tarifler[secilen_tarif]
            t_kalori, t_protein, t_karb, t_yag = 0, 0, 0, 0
            detaylar = []
            
            for m, gram in malzemeler.items():
                if m in st.session_state.besin
