import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Diyet ve Aktivite Asistanı", layout="wide")

# Oturum Durumu Başlatma
if "besin_veritabani" not in st.session_state:
    st.session_state.besin_veritabani = {
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
    }

if "hazir_tarifler" not in st.session_state:
    st.session_state.hazir_tarifler = {
        "Tavuklu Salata": {"tavuk gogsu": 200, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
        "Köfteli Salata": {"kofte": 150, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
        "Ton Balıklı Salata": {"ton baligi": 110, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
        "Latte (Orta Boy)": {"sut": 250, "kahve": 30},
        "Americano (Orta Boy)": {"kahve": 20},
        "Kefir Karışımı": {"kefir": 200, "x-lim toz": 5},
        "Badem (1 Avuç)": {"badem": 30},
        "Mandalina (3 Adet)": {"mandalina": 300},
        "Meyveli Soda": {"meyveli soda": 200}
    }

if "gunluk_kayitlar" not in st.session_state:
    st.session_state.gunluk_kayitlar = []

if "profil" not in st.session_state:
    st.session_state.profil = {
        "cinsiyet": "Kadın", "yas": 20, "boy": 165, "kilo": 58.0, 
        "hedef_kalori": 1800, "hedef_protein": 90, "hedef_karb": 200, "hedef_yag": 60
    }

st.title("Diyet ve Aktivite Takip Asistanı")

menu = st.sidebar.selectbox(
    "Menü", 
    [
        "Günlük Takip Paneli", 
        "Haftalık Program & Değerlendirme", 
        "Tarif ve Malzeme Yönetimi", 
        "Pilates & Yürüyüş Detayları", 
        "Makro & Hedef Sihirbazı"
    ]
)

# ----------------------------------------------------
# 1. GÜNLÜK TAKİP PANELİ
# ----------------------------------------------------
if menu == "Günlük Takip Paneli":
    st.header("Günlük Öğün ve Aktivite Girişi")
    
    secilen_tarih = st.date_input("Kayıt Tarihi", datetime.date.today())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Öğün Ekle")
        ogun_turu = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
        secilen_tarif = st.selectbox("Mevcut Tarifler", list(st.session_state.hazir_tarifler.keys()))
        
        if st.button("Öğüne Ekle"):
            malzemeler = st.session_state.hazir_tarifler[secilen_tarif]
            t_kalori, t_protein, t_karb, t_yag = 0, 0, 0, 0
            detaylar = []
            
            for m, gram in malzemeler.items():
                if m in st.session_state.besin_veritabani:
                    b = st.session_state.besin_veritabani[m]
                    oran = gram / 100.0
                    t_kalori += b["kalori"] * oran
                    t_protein += b["protein"] * oran
                    t_karb += b["karb"] * oran
                    t_yag += b["yag"] * oran
                    detaylar.append(f"{gram}g {m}")
            
            st.session_state.gunluk_kayitlar.append({
                "Tarih": str(secilen_tarih),
                "Öğün": ogun_turu, 
                "Tarif": secilen_tarif, 
                "İçerik": ", ".join(detaylar),
                "Kalori": round(t_kalori, 1), 
                "Protein": round(t_protein, 1),
                "Karbonhidrat": round(t_karb, 1), 
                "Yağ": round(t_yag, 1)
            })
            st.success(f"'{secilen_tarif}' öğüne başarıyla eklendi.")

    with col2:
        st.subheader("Su Tüketimi")
        su_miktari = st.slider("Günlük Su (Litre)", 0.0, 5.0, 2.0, 0.5)

    st.markdown("---")
    st.subheader("Seçilen Tarihe Ait Günlük Özet")
    
    if st.session_state.gunluk_kayitlar:
        df_tum = pd.DataFrame(st.session_state.gunluk_kayitlar)
        df_bugun = df_tum[df_tum["Tarih"] == str(secilen_tarih)]
        
        if not df_bugun.empty:
            st.dataframe(df_bugun[["Öğün", "Tarif", "İçerik", "Kalori", "Protein", "Karbonhidrat", "Yağ"]], use_container_width=True)
            
            toplam_kalori = df_bugun["Kalori"].sum()
            toplam_protein = df_bugun["Protein"].sum()
            toplam_karb = df_bugun["Karbonhidrat"].sum()
            toplam_yag = df_bugun["Yağ"].sum()
            
            hedef_k = st.session_state.profil["hedef_kalori"]
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Alınan Kalori", f"{toplam_kalori:.1f} kcal", f"Hedef: {hedef_k}")
            m2.metric("Su Tüketimi", f"{su_miktari} Litre")
            m3.metric("Protein / Karb / Yağ", f"{toplam_protein:.1f}g / {toplam_karb:.1f}g / {toplam_yag:.1f}g")
        else:
            st.info("Bu tarih için henüz öğün kaydı girilmedi.")
    else:
        st.info("Henüz hiç kayıt bulunmuyor.")

# ----------------------------------------------------
# 2. HAFTALIK PROGRAM & DEĞERLENDİRME
# ----------------------------------------------------
elif menu == "Haftalık Program & Değerlendirme":
    st.header("Haftalık Program ve Kalori Değerlendirmesi")
    
    if st.session_state.gunluk_kayitlar:
        df_tum = pd.DataFrame(st.session_state.gunluk_kayitlar)
        haftalik_ozet = df_tum.groupby("Tarih")[["Kalori", "Protein", "Karbonhidrat", "Yağ"]].sum().reset_index()
        haftalik_ozet = haftalik_ozet.sort_values("Tarih", ascending=False)
        
        st.subheader("Gün Bazlı Geçmiş Dökümü")
        st.dataframe(haftalik_ozet, use_container_width=True)
        
        st.subheader("Haftalık Kalori Trendi")
        if len(haftalik_ozet) > 0:
            st.line_chart(haftalik_ozet.set_index("Tarih")["Kalori"])
            
            ortalama_kalori = haftalik_ozet["Kalori"].mean()
            hedef_k = st.session_state.profil["hedef_kalori"]
            
            st.markdown(f"**Haftalık Ortalama Alınan Kalori:** {ortalama_kalori:.1f} kcal")
            if ortalama_kalori > hedef_k:
                st.warning("Haftalık ortalamanız hedef kalorinin üzerinde seyrediyor.")
            else:
                st.success("Haftalık ortalamanız hedef aralığında ilerliyor.")
    else:
        st.info("Değerlendirme yapabilmek için günlük kayıtlar sekmesinden veri eklemelisiniz.")

# ----------------------------------------------------
# 3. TARİF VE MALZEME YÖNETİMİ
# ----------------------------------------------------
elif menu == "Tarif & Malzeme Yönetimi":
    st.header("Tarif ve Malzeme Yönetim Paneli")
    
    sekme1, sekme2 = st.tabs(["Yeni Ham Malzeme Ekle", "Gramajlı Yeni Tarif Oluştur"])
    
    with sekme1:
        st.subheader("Veritabanına Yeni Malzeme Tanımla (100g Üzerinden)")
        m_ad = st.text_input("Malzeme Adı (Örn: Lor Peyniri)")
        m_kal = st.number_input("100 gramdaki Kalori (kcal)", min_value=0.0, value=100.0)
        m_pro = st.number_input("100 gramdaki Protein (g)", min_value=0.0, value=10.0)
        m_kar = st.number_input("100 gramdaki Karbonhidrat (g)", min_value=0.0, value=5.0)
        m_yag = st.number_input("100 gramdaki Yağ (g)", min_value=0.0, value=3.0)
        
        if st.button("Malzemeyi Veritabanına Kaydet"):
            if m_ad:
                temiz_ad = m_ad.strip().lower()
                st.session_state.besin_veritabani[temiz_ad] = {
                    "kalori": m_kal, "protein": m_pro, "karb": m_kar, "yag": m_yag
                }
                st.success(f"'{m_ad}' başarıyla veritabanına eklendi.")
            else:
                st.warning("Lütfen bir malzeme adı girin.")

    with sekme2:
        st.subheader("Gramaj Esaslı Yeni Tarif Oluştur")
        t_ad = st.text_input("Tarif Adı (Örn: Özel Sandviç)")
        
        secilen_malzemeler = st.multiselect("Malzeme Seçimi", list(st.session_state.besin_veritabani.keys()))
        tarif_malzeme_gramajlari = {}
        
        for m in secilen_malzemeler:
            gr = st.number_input(f"{m} için miktar (Gram / ml)", min_value=1.0, value=50.0, step=5.0, key=f"tarif_gr_{m}")
            tarif_malzeme_gramajlari[m] = gr
            
        if st.button("Tarifi Kütüphaneye Kaydet"):
            if t_ad and tarif_malzeme_gramajlari:
                st.session_state.hazir_tarifler[t_ad] = tarif_malzeme_gramajlari
                st.success(f"'{t_ad}' tarifi başarıyla oluşturuldu ve kütüphaneye eklendi.")
            else:
                st.warning("Lütfen tarif adı yazın ve en az bir malzeme seçin.")

# ----------------------------------------------------
# 4. PİLATES & YÜRÜYÜŞ DETAYLARI
# ----------------------------------------------------
elif menu == "Pilates & Yürüyüş Detayları":
    st.header("Pilates ve Yürüyüş Aktivite Analizi")
    
    col_p, col_y = st.columns(2)
    
    with col_p:
        st.subheader("Pilates Seansı")
        p_tur = st.selectbox("Pilates Türü", ["Mat Pilates", "Reformer Pilates", "Yoğun / Klinik Pilates"])
        p_sure = st.number_input("Süre (Dakika)", min_value=10, value=50, step=5)
        
        met_p = {"Mat Pilates": 3.0, "Reformer Pilates": 4.0, "Yoğun / Klinik Pilates": 5.0}
        kilo_degeri = st.session_state.profil["kilo"]
        yakilan_pilates = (met_p[p_tur] * 3.5 * kilo_degeri / 200) * p_sure
        
        st.write(f"Tahmini Yakılan Kalori: **{yakilan_pilates:.1f} kcal**")

    with col_y:
        st.subheader("Yürüyüş Seansı")
        y_tur = st.selectbox("Yürüyüş Temposu", ["Hafif Tempo (4 km/s)", "Orta Tempo (5 km/s)", "Tempolu / Eğimli (6.5 km/s)"])
        y_sure = st.number_input("Yürüme Süresi (Dakika)", min_value=10, value=45, step=5)
        
        met_y = {"Hafif Tempo (4 km/s)": 2.9, "Orta Tempo (5 km/s)": 3.5, "Tempolu / Eğimli (6.5 km/s)": 5.0}
        yakilan_yuruyus = (met_y[y_tur] * 3.5 * kilo_degeri / 200) * y_sure
        
        st.write(f"Tahmini Yakılan Kalori: **{yakilan_yuruyus:.1f} kcal**")

# ----------------------------------------------------
# 5. MAKRO & HEDEF SİHİRBAZI
# ----------------------------------------------------
elif menu == "Makro & Hedef Sihirbazı":
    st.header("Kişiselleştirilmiş Hedef ve Makro Hesaplama Sihirbazı")
    
    c1, c2, c3 = st.columns(3)
    cinsiyet = c1.selectbox("Cinsiyet", ["Kadın", "Erkek"], index=0 if st.session_state.profil["cinsiyet"] == "Kadın" else 1)
    yas = c2.number_input("Yaş", min_value=15, max_value=80, value=st.session_state.profil["yas"])
    boy = c3.number_input("Boy (cm)", min_value=120, max_value=210, value=st.session_state.profil["boy"])
    
    c4, c5 = st.columns(2)
    kilo = c4.number_input("Kilo (kg)", min_value=35.0, max_value=160.0, value=st.session_state.profil["kilo"])
    aktivite = c5.selectbox("Aktivite Düzeyi", ["Hareketsiz / Masa Başı", "Hafif Aktif (Haftada 1-3 gün)", "Orta Aktif (Haftada 3-5 gün)", "Çok Aktif"])

    if st.button("Hedeflerimi Hesapla"):
        if cinsiyet == "Kadın":
            bmr = (10 * kilo) + (6.25 * boy) - (5 * yas) - 161
        else:
            bmr = (10 * kilo) + (6.25 * boy) - (5 * yas) + 5
            
        carpanlar = {
            "Hareketsiz / Masa Başı": 1.2,
            "Hafif Aktif (Haftada 1-3 gün)": 1.375,
            "Orta Aktif (Haftada 3-5 gün)": 1.55,
            "Çok Aktif": 1.725
        }
        
        tdee = bmr * carpanlar[aktivite]
        
        st.session_state.profil["cinsiyet"] = cinsiyet
        st.session_state.profil["yas"] = yas
