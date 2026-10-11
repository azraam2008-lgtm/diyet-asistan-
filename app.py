import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Azra'nın Diyet Asistanı", page_icon="🌸", layout="wide")

# Oturum Durumu (Session State)
if "besin_veritabani" not in st.session_state:
    st.session_state.besin_veritabani = {
        "tavuk gogsu": {"kalori": 165, "protein": 31.0, "karb": 0.0, "yag": 3.6},
        "ton baligi": {"kalori": 110, "protein": 25.0, "karb": 0.0, "yag": 1.0},
        "marul": {"kalori": 15, "protein": 1.4, "karb": 2.9, "yag": 0.2},
        "salatalik": {"kalori": 15, "protein": 0.7, "karb": 3.6, "yag": 0.1},
        "domates": {"kalori": 18, "protein": 0.9, "karb": 3.9, "yag": 0.2},
        "dilim peynir": {"kalori": 320, "protein": 22.0, "karb": 1.5, "yag": 25.0},
        "kasar peyniri": {"kalori": 350, "protein": 25.0, "karb": 1.3, "yag": 27.0},
        "tam bugday ekmegi": {"kalori": 247, "protein": 13.0, "karb": 41.0, "yag": 3.4},
        "labne": {"kalori": 210, "protein": 6.0, "karb": 4.0, "yag": 20.0},
        "sut": {"kalori": 50, "protein": 3.4, "karb": 4.8, "yag": 1.5},
        "kahve": {"kalori": 2, "protein": 0.1, "karb": 0.3, "yag": 0.0},
        "pirinc pilavi": {"kalori": 150, "protein": 3.0, "karb": 28.0, "yag": 3.0}
    }

if "hazir_tarifler" not in st.session_state:
    st.session_state.hazir_tarifler = {
        "Tavuklu Salata": {"tavuk gogsu": 200, "marul": 30, "domates": 100, "salatalik": 100, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
        "Ton Balıklı Salata": {"ton baligi": 110, "marul": 30, "domates": 100, "salatalik": 100, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
        "Latte": {"sut": 250, "kahve": 30},
        "Pilav": {"pirinc pilavi": 150},
        "Tost": {"tam bugday ekmegi": 50, "kasar peyniri": 40, "domates": 40}
    }

if "gunluk_kayitlar" not in st.session_state:
    st.session_state.gunluk_kayitlar = []

st.title("🌸 Azra'nın Akıllı Diyet ve Aktivite Asistanı")

menu = st.sidebar.selectbox("Navigasyon", ["📅 Günlük Takip Paneli", "🍳 Yeni Tarif / Yemek Ekle", "⚖️ Haftalık Kilo & Tahmin Analizi"])

if menu == "📅 Günlük Takip Paneli":
    st.header("Günlük Öğün ve Aktivite Girişi")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍽️ Öğün Seçimi")
        ogun_turu = st.selectbox("Öğün Seç", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün / İçecek"])
        secilen_tarif = st.selectbox("Kütüphanedeki Tarifler", list(st.session_state.hazir_tarifler.keys()))
        
        if st.button("🍽️ Bu Öğüne Ekle"):
            malzemeler = st.session_state.hazir_tarifler[secilen_tarif]
            t_kalori, t_protein, t_karb, t_yag = 0, 0, 0, 0
            detaylar = []
            
            for m, gram in malzemeler.items():
                b = st.session_state.besin_veritabani[m]
                oran = gram / 100.0
                t_kalori += b["kalori"] * oran
                t_protein += b["protein"] * oran
                t_karb += b["karb"] * oran
                t_yag += b["yag"] * oran
                detaylar.append(f"{gram}g {m}")
                
            st.session_state.gunluk_kayitlar.append({
                "Öğün": ogun_turu, "Tarif": secilen_tarif, "İçerik": ", ".join(detaylar),
                "Kalori": round(t_kalori, 1), "Protein": round(t_protein, 1),
                "Karbonhidrat": round(t_karb, 1), "Yağ": round(t_yag, 1)
            })
            st.success(f"✅ {secilen_tarif} eklendi!")

    with col2:
        st.subheader("🚶‍♀️ Fiziksel Aktivite & Su")
        adim_sayisi = st.number_input("Günlük Adım Sayısı", min_value=0, max_value=50000, value=15000, step=500)
        su_miktari = st.slider("Su Tüketimi (Litre)", 0.0, 5.0, 2.0, 0.5)

    st.markdown("---")
    st.subheader("📊 Günlük Özet Tablosu")
    
    if st.session_state.gunluk_kayitlar:
        df_kayitlar = pd.DataFrame(st.session_state.gunluk_kayitlar)
        st.dataframe(df_kayitlar, use_container_width=True)
        
        toplam_alnan = df_kayitlar["Kalori"].sum()
        toplam_protein = df_kayitlar["Protein"].sum()
        toplam_karb = df_kayitlar["Karbonhidrat"].sum()
        toplam_yag = df_kayitlar["Yağ"].sum()
        
        bmr = (10 * 68.0) + (6.25 * 160) - (5 * 18) - 161
        adim_kalorisi = (adim_sayisi / 1000) * 45
        toplam_harcanan = bmr + adim_kalorisi
        net_denge = toplam_alnan - toplam_harcanan
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Alınan Kalori", f"{toplam_alnan:.1f} kcal")
        m2.metric("Harcanan Kalori", f"{toplam_harcanan:.1f} kcal")
        m3.metric("Net Kalori Dengesi", f"{net_denge:.1f} kcal")
        st.info(f"🥩 Protein: {toplam_protein:.1f}g | 🍞 Karbonhidrat: {toplam_karb:.1f}g | 🥑 Yağ: {toplam_yag:.1f}g | 💧 Su: {su_miktari}L")

elif menu == "🍳 Yeni Tarif / Yemek Ekle":
    st.header("🍳 Kendi Tarifini Oluştur")
    yeni_tarif_adi = st.text_input("Tarif Adı")
    secilen_malzemeler = {}
    
    cols = st.columns(3)
    mevcut_malzemeler = list(st.session_state.besin_veritabani.keys())
    
    for i, m in enumerate(mevcut_malzemeler):
        with cols[i % 3]:
            if st.checkbox(f"{m.title()}", key=f"chk_{m}"):
                gram = st.number_input(f"{m.title()} (Gram/ml)", min_value=5, max_value=1000, value=100, step=5, key=f"gram_{m}")
                secilen_malzemeler[m] = gram

    if st.button("✨ Bu Tarifi Kaydet"):
        if yeni_tarif_adi and secilen_malzemeler:
            st.session_state.hazir_tarifler[yeni_tarif_adi] = secilen_malzemeler
            st.success(f"🎉 '{yeni_tarif_adi}' kütüphaneye eklendi!")
        else:
            st.warning("⚠️ Lütfen tarif adı yazın ve en az bir malzeme seçin.")

elif menu == "⚖️ Haftalık Kilo & Tahmin Analizi":
    st.header("🗓️ Haftalık Kilo Takibi ve Tahmin")
    yeni_kilo = st.number_input("Güncel Tartı Ölçümün (kg)", min_value=30.0, max_value=150.0, value=68.0, step=0.1)
    if st.button("🔮 Haftalık Analizi Çalıştır"):
        st.success(f"Kilo {yeni_kilo} kg olarak güncellendi ve kaydedildi!")