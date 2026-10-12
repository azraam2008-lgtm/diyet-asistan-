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
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "tarifler": {
            "Köfteli Salata": {"kalori": 480, "protein": 34, "karb": 12, "yag": 28, "birim": "porsiyon"},
            "Kefir Karışımı (Kefir + X-Lim+)": {"kalori": 130, "protein": 11, "karb": 11, "yag": 5, "birim": "porsiyon"},
            "Badem (1 Avuç)": {"kalori": 160, "protein": 6, "karb": 6, "yag": 14, "birim": "porsiyon"},
            "Mandalina (3 Adet)": {"kalori": 120, "protein": 2, "karb": 30, "yag": 0, "birim": "porsiyon"},
            "Meyveli Soda": {"kalori": 90, "protein": 0, "karb": 22, "yag": 0, "birim": "şişe"},
            "Latte (Orta Boy)": {"kalori": 120, "protein": 6, "karb": 10, "yag": 6, "birim": "fincan"},
            "Americano (Orta Boy)": {"kalori": 15, "protein": 0, "karb": 2, "yag": 0, "birim": "fincan"}
        },
        "malzemeler": {
            "Köfte (Izgara)": {"kalori_100g": 220, "protein": 24, "karb": 2, "yag": 13},
            "Akdeniz Yeşilliği": {"kalori_100g": 18, "protein": 1.5, "karb": 3.2, "yag": 0.2},
            "Zeytinyağı": {"kalori_100g": 884, "protein": 0, "karb": 0, "yag": 100}
        },
        "gunluk_loglar": {},
        "profil": {"hedef_kalori": 1800, "hedef_protein": 90, "hedef_karb": 200, "hedef_yag": 60}
    }

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
        db["gunluk_loglar"][secilen_tarih] = {"ogunler": [], "su_lt": 0.0}

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
        bugun_ogunler = db["gunluk_loglar"][secilen_tarih]["ogunler"]
        toplam_kalori = sum(x["kalori"] for x in bugun_ogunler)
        toplam_protein = sum(x["protein"] for x in bugun_ogunler)
        toplam_karb = sum(x["karb"] for x in bugun_ogunler)
        toplam_yag = sum(x["yag"] for x in bugun_ogunler)

        st.metric("Alınan Kalori", f"{toplam_kalori:.0f} kcal / {db['profil']['hedef_kalori']} kcal")
        st.progress(min(toplam_kalori / max(db['profil']['hedef_kalori'], 1), 1.0))

        st.write(f"**Protein:** {toplam_protein:.1f}g")
        st.write(f"**Karbonhidrat:** {toplam_karb:.1f}g")
        st.write(f"**Yağ:** {toplam_yag:.1f}g")

    st.divider()
    st.subheader("Bugün Tüketilenler")
    if bugun_ogunler:
        df_bugun = pd.DataFrame(bugun_ogunler)
        st.dataframe(df_bugun[["ad", "porsiyon", "kalori", "protein", "karb", "yag"]], use_container_width=True)
    else:
        st.info("Henüz kayıt eklenmedi.")

# ----------------------------------------------------
# 2. HAFTALIK PROGRAM & DEĞERLENDİRME
# ----------------------------------------------------
elif secim == "Haftalık Program & Değerlendirme":
    st.header("Haftalık İlerleme ve Analiz Paneli")
    
    loglar = db["gunluk_loglar"]
    if loglar:
        ozet_veri = []
        for tarih, icerik in loglar.items():
            top_kalori = sum(x["kalori"] for x in icerik["ogunler"])
            top_prot = sum(x["protein"] for x in icerik["ogunler"])
            top_karb = sum(x["karb"] for x in icerik["ogunler"])
            top_yag = sum(x["yag"] for x in icerik["ogunler"])
            ozet_veri.append({
                "Tarih": tarih,
                "Kalori (kcal)": top_kalori,
                "Protein (g)": top_prot,
                "Karb (g)": top_karb,
                "Yağ (g)": top_yag
            })

        df_hafta = pd.DataFrame(ozet_veri).sort_values("Tarih", ascending=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Kalori Grafiği")
            st.line_chart(df_hafta.set_index("Tarih")["Kalori (kcal)"])

        with col2:
            st.subheader("Haftalık Ortalama")
            ort_kalori = df_hafta["Kalori (kcal)"].mean()
            st.metric("Ortalama Günlük Kalori", f"{ort_kalori:.0f} kcal")
            if ort_kalori > db["profil"]["hedef_kalori"]:
                st.warning("Haftalık ortalamanız belirlenen hedefin üzerinde.")
            else:
                st.success("Haftalık ortalamanız belirlenen hedef aralığında.")

        st.subheader("Gün Gün Geçmiş Dökümü")
        st.dataframe(df_hafta, use_container_width=True)
    else:
        st.info("Geçmiş verilere ulaşmak için günlük kayıt eklemelisiniz.")

# ------------------------------------------------
