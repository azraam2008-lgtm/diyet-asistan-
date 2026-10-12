import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Beslenme ve Aktivite Takip Portalı",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Yerel Veri Depolama Fonksiyonları
DATA_FILE = "diyet_verileri.json"

def veri_yukle():
    default_data = {
        "tarifler": {
            "Tavuklu Salata": {"kalori": 420, "protein": 38, "karb": 10, "yag": 22, "birim": "porsiyon"},
            "Köfteli Salata": {"kalori": 480, "protein": 34, "karb": 12, "yag": 28, "birim": "porsiyon"},
            "Ton Balıklı Salata": {"kalori": 390, "protein": 32, "karb": 12, "yag": 20, "birim": "porsiyon"},
            "Tost (Kaşarlı / Beyaz Peynirli)": {"kalori": 350, "protein": 15, "karb": 35, "yag": 16, "birim": "porsiyon"},
            "Kefir Karışımı (Kefir + X-Lim+)": {"kalori": 130, "protein": 11, "karb": 11, "yag": 5, "birim": "porsiyon"},
            "Badem (1 Avuç)": {"kalori": 160, "protein": 6, "karb": 6, "yag": 14, "birim": "porsiyon"},
            "Mandalina (3 Adet)": {"kalori": 120, "protein": 2, "karb": 30, "yag": 0, "birim": "porsiyon"},
            "Meyveli Soda": {"kalori": 90, "protein": 0, "karb": 22, "yag": 0, "birim": "şişe"},
            "Latte (Orta Boy)": {"kalori": 120, "protein": 6, "karb": 10, "yag": 6, "birim": "fincan"},
            "Americano (Orta Boy)": {"kalori": 15, "protein": 0, "karb": 2, "yag": 0, "birim": "fincan"}
        },
        "malzemeler": {
            "Tavuk Göğsü (Izgara)": {"kalori_100g": 165, "protein": 31, "karb": 0, "yag": 3.6},
            "Köfte (Izgara)": {"kalori_100g": 220, "protein": 24, "karb": 2, "yag": 13},
            "Ton Balığı (Konserve)": {"kalori_100g": 130, "protein": 28, "karb": 0, "yag": 2.0},
            "Akdeniz Yeşilliği": {"kalori_100g": 18, "protein": 1.5, "karb": 3.2, "yag": 0.2},
            "Zeytinyağı": {"kalori_100g": 884, "protein": 0, "karb": 0, "yag": 100},
            "Kefir": {"kalori_100g": 60, "protein": 3.5, "karb": 4.5, "yag": 3.0},
            "Badem": {"kalori_100g": 575, "protein": 21, "karb": 22, "yag": 49}
        },
        "gunluk_loglar": {},
        "profil": {"hedef_kalori": 1800, "hedef_protein": 90, "hedef_karb": 200, "hedef_yag": 60}
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in default_data["tarifler"].items():
                    if k not in data.get("tarifler", {}):
                        data.setdefault("tarifler", {})[k] = v
                for k, v in default_data["malzemeler"].items():
                    if k not in data.get("malzemeler", {}):
                        data.setdefault("malzemeler", {})[k] = v
                if "gunluk_loglar" not in data:
                    data["gunluk_loglar"] = {}
                if "profil" not in data:
                    data["profil"] = default_data["profil"]
                return data
        except:
            return default_data
    return default_data

def veri_kaydet(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = veri_yukle()

# Navigasyon
st.sidebar.title("Kontrol Paneli")
secim = st.sidebar.radio(
    "Menü",
    ["Günlük Öğün Takibi", "Haftalık Program & Değerlendirme", "Aktivite & Pilates", "Makro Sihirbazı", "Tarif & Malzeme Yönetimi"]
)

# ----------------------------------------------------
# 1. GÜNLÜK ÖĞÜN TAKİBİ
# ----------------------------------------------------
if secim == "Günlük Öğün Takibi":
    st.header("Günlük Beslenme Takibi")
    secilen_tarih = str(st.date_input("Tarih Seçin", date.today()))

    if secilen_tarih not in db["gunluk_loglar"]:
        db["gunluk_loglar"][secilen_tarih] = {"ogunler": []}

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Öğün Ekle")
        tarif_listesi = list(db["tarifler"].keys())
        secilen_tarif = st.selectbox("Tarif / Yiyecek Seç", tarif_listesi)
        porsiyon = st.number_input("Porsiyon / Miktar", min_value=0.1, value=1.0, step=0.5)

        if st.button("Öğüne Ekle"):
            t_bilgi = db["tarifler"][secilen_tarif]
            eklenen = {
                "ad": secilen_tarif,
                "porsiyon": porsiyon,
                "kalori": t_bilgi["kalori"] * porsiyon,
                "protein": t_bilgi["protein"] * porsiyon,
                "karb": t_bilgi["karb"] * porsiyon,
                "yag": t_bilgi["yag"] * porsiyon
            }
            db["gunluk_loglar"][secilen_tarih]["ogunler"].append(eklenen)
            veri_kaydet(db)
            st.success(f"{secilen_tarif} günlüğe eklendi.")

    with col2:
        st.subheader("Günlük Özet")
        bugun_ogun
